#!/usr/bin/env python3
"""Compact native AFFiNE automation over local Electron CDP."""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

try:
    from websockets.sync.client import connect
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing Python package: websockets") from exc


HOST = "127.0.0.1"
PORT = 9222
BASE = f"http://{HOST}:{PORT}"


def http_json(path: str, timeout: float = 2.0):
    with urllib.request.urlopen(BASE + path, timeout=timeout) as response:
        return json.load(response)


def cdp(ws_url: str, method: str, params: dict | None = None):
    request = {"id": 1, "method": method}
    if params:
        request["params"] = params
    with connect(ws_url, max_size=None) as socket:
        socket.send(json.dumps(request))
        while True:
            message = json.loads(socket.recv())
            if message.get("id") != 1:
                continue
            if "error" in message:
                raise RuntimeError(message["error"].get("message", str(message["error"])))
            return message.get("result", {})


def evaluate(ws_url: str, expression: str):
    result = cdp(
        ws_url,
        "Runtime.evaluate",
        {"expression": expression, "returnByValue": True, "awaitPromise": True},
    )
    remote = result.get("result", {})
    if remote.get("subtype") == "error":
        raise RuntimeError(remote.get("description", "JavaScript error"))
    return remote.get("value")


INSPECT_JS = r"""(() => {
  const e = document.querySelector('affine-edgeless-root');
  const p = document.querySelector('affine-page-root');
  const root = e || p;
  const rect = root?.getBoundingClientRect();
  return {
    title: document.title,
    url: location.href,
    visibility: document.visibilityState,
    visibleRoot: !!rect && rect.width > 0 && rect.height > 0,
    id: root?.std?.store?.id ?? null,
    mode: e ? 'edgeless' : p ? 'page' : null,
    count: e?.surfaceBlockModel?.getElementsByType('shape').length ?? 0,
    bounds: e?.gfx?.elementsBound ?? null,
    zoom: e?.gfx?.viewport?.zoom ?? null,
    center: e?.gfx?.viewport?.center ?? null
  };
})()"""


def workspace_targets():
    targets = http_json("/json")
    return [
        target
        for target in targets
        if target.get("type", "page") == "page"
        and "/workspace/" in target.get("url", "")
        and target.get("webSocketDebuggerUrl")
    ]


def find_target(require_root: bool = True):
    candidates = []
    for target in workspace_targets():
        try:
            info = evaluate(target["webSocketDebuggerUrl"], INSPECT_JS)
        except Exception:
            continue
        if require_root and not info.get("id"):
            continue
        score = 0
        score += 20 if info.get("visibility") == "visible" else 0
        score += 10 if info.get("visibleRoot") else 0
        score += 5 if info.get("mode") == "edgeless" else 0
        score += 2 if info.get("title") not in ("AFFiNE", "") else 0
        candidates.append((score, target, info))
    if not candidates:
        raise RuntimeError("No active AFFiNE workspace renderer")
    _, target, info = max(candidates, key=lambda item: item[0])
    return target, info


def compact_print(value):
    print(json.dumps(value, ensure_ascii=True, separators=(",", ":")))


def port_ready():
    try:
        http_json("/json/version")
        return True
    except Exception:
        return False


def affine_process_ids():
    command = (
        "Get-Process -Name AFFiNE -ErrorAction SilentlyContinue | "
        "Select-Object -ExpandProperty Id"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip().isdigit()]


def latest_executable():
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "AFFiNE"
    matches = list(base.glob("app-*/AFFiNE.exe"))
    if not matches:
        raise RuntimeError(f"AFFiNE executable not found under {base}")

    def version_key(path: Path):
        raw = path.parent.name.removeprefix("app-")
        return tuple(int(part) if part.isdigit() else 0 for part in raw.split("."))

    return max(matches, key=version_key)


def ensure(relaunch: bool = False):
    if port_ready():
        target, info = find_target(require_root=False)
        return {"ready": True, "relaunched": False, "target": target["id"], **info}

    running = affine_process_ids()
    if running and not relaunch:
        raise RuntimeError("AFFiNE is running without CDP; rerun ensure --relaunch")

    if running:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-Process -Name AFFiNE -ErrorAction SilentlyContinue | "
                "ForEach-Object { [void]$_.CloseMainWindow() }",
            ],
            capture_output=True,
            check=False,
        )
        deadline = time.time() + 8
        while affine_process_ids() and time.time() < deadline:
            time.sleep(0.25)
        if affine_process_ids():
            raise RuntimeError("AFFiNE did not close gracefully; close it manually")

    executable = latest_executable()
    subprocess.Popen(
        [
            str(executable),
            f"--remote-debugging-address={HOST}",
            f"--remote-debugging-port={PORT}",
        ],
        close_fds=True,
    )
    deadline = time.time() + 20
    while not port_ready() and time.time() < deadline:
        time.sleep(0.25)
    if not port_ready():
        raise RuntimeError("AFFiNE CDP endpoint did not start")
    time.sleep(1)
    target, info = find_target(require_root=False)
    return {"ready": True, "relaunched": bool(running), "target": target["id"], **info}


def current_ws():
    return find_target()[0]["webSocketDebuggerUrl"]


def switch_edgeless():
    target, info = find_target()
    if info.get("mode") == "edgeless":
        return target, info
    evaluate(
        target["webSocketDebuggerUrl"],
        "(() => { const b=document.querySelector('[data-testid=\"switch-edgeless-mode-button\"]'); if(!b) throw new Error('Edgeless switch unavailable'); b.click(); return true; })()",
    )
    time.sleep(1)
    return find_target()


def set_title(title: str):
    target, _ = find_target()
    expression = f"""(() => {{
      const root=document.querySelector('affine-edgeless-root') || document.querySelector('affine-page-root');
      if(!root) throw new Error('AFFiNE root unavailable');
      const store=root.std.store;
      store.workspace.meta.setDocMeta(store.id,{{title:{json.dumps(title)}}});
      return {{id:store.id,title:{json.dumps(title)}}};
    }})()"""
    return evaluate(target["webSocketDebuggerUrl"], expression)


def new_page(title: str):
    target, _ = find_target()
    evaluate(
        target["webSocketDebuggerUrl"],
        "(() => { const b=document.querySelector('[data-testid=\"sidebar-new-page-button\"]'); if(!b) throw new Error('New-page button unavailable'); b.click(); return true; })()",
    )
    time.sleep(1)
    switch_edgeless()
    result = set_title(title)
    time.sleep(0.25)
    _, info = find_target()
    return {**result, "mode": info.get("mode"), "count": info.get("count")}


STYLE = {
    "title": {"fill": "#171717", "stroke": "#171717", "color": "#FFF8E7", "size": 34, "weight": 700, "padding": [30, 25], "radius": 12},
    "section": {"fill": "#285F73", "stroke": "#285F73", "color": "#FFFFFF", "size": 24, "weight": 700, "padding": [28, 20], "radius": 12},
    "card": {"fill": "#F5F2EA", "stroke": "#8C8678", "color": "#292722", "size": 16, "weight": 400, "padding": [22, 20], "radius": 14},
    "note": {"fill": "#FFF1C7", "stroke": "#C9952B", "color": "#30240B", "size": 17, "weight": 500, "padding": [24, 22], "radius": 14},
    "warning": {"fill": "#FBE4E1", "stroke": "#C85A52", "color": "#5B211D", "size": 16, "weight": 600, "padding": [24, 22], "radius": 14},
    "quote": {"fill": "#EEEAF8", "stroke": "#7569A8", "color": "#2E2851", "size": 17, "weight": 500, "padding": [24, 22], "radius": 14},
    "flow": {"fill": "#DCEEE5", "stroke": "#4D8A70", "color": "#183E31", "size": 18, "weight": 700, "padding": [24, 20], "radius": 12, "align": "center"},
}


def estimated_height(text: str, width: float, kind: str):
    style = STYLE.get(kind, STYLE["card"])
    chars = max(18, int((width - 2 * style["padding"][0]) / (style["size"] * 0.54)))
    lines = 0
    for raw in (text or "").splitlines() or [""]:
        lines += max(1, math.ceil(len(raw) / chars))
    minimum = 100 if kind in ("title", "section", "flow") else 150
    return max(minimum, int(2 * style["padding"][1] + lines * style["size"] * 1.36 + 16))


def layout_rows(spec: dict):
    width = float(spec.get("width", 2360))
    x0 = float(spec.get("x", 0))
    y = float(spec.get("y", 0))
    row_gap = float(spec.get("rowGap", 30))
    nodes = []
    for row in spec.get("rows", []):
        items = row.get("items")
        if not items:
            items = [{key: value for key, value in row.items() if key not in ("items", "height", "gap", "after")}]
        gap = float(row.get("gap", 30))
        spans = [float(item.get("span", 1)) for item in items]
        usable = width - gap * (len(items) - 1)
        unit = usable / sum(spans)
        widths = [unit * span for span in spans]
        heights = [
            estimated_height(item.get("text", ""), item_width, item.get("kind", row.get("kind", "card")))
            for item, item_width in zip(items, widths)
        ]
        height = float(row.get("height", max(heights)))
        x = x0
        for item, item_width in zip(items, widths):
            node = dict(item)
            node["kind"] = node.get("kind", row.get("kind", "card"))
            node.update({"x": x, "y": y, "w": item_width, "h": height})
            nodes.append(node)
            x += item_width + gap
        y += height + float(row.get("after", row_gap))
    return nodes, y


def apply_board(spec: dict):
    if spec.get("newPage"):
        new_page(spec.get("title", "Untitled"))
    target, _ = switch_edgeless()
    nodes, total_height = layout_rows(spec)
    payload = []
    for node in nodes:
        style = dict(STYLE.get(node.get("kind"), STYLE["card"]))
        style.update(node.get("style", {}))
        payload.append({**node, "style": style})
    expression = f"""(() => {{
      const root=document.querySelector('affine-edgeless-root');
      if(!root) throw new Error('Edgeless root unavailable');
      const surface=root.surfaceBlockModel;
      const nodes={json.dumps(payload, ensure_ascii=True)};
      if({str(bool(spec.get('clearExisting'))).lower()}) {{
        for(const item of surface.getElementsByType('shape')) root.gfx.deleteElement(item.id);
      }}
      const ids=[];
      for(const n of nodes) {{
        const s=n.style;
        ids.push(surface.addElement({{
          type:'shape',shapeType:'rect',shapeStyle:'General',strokeStyle:'solid',strokeWidth:2,filled:true,
          fontFamily:'blocksuite:surface:Inter',xywh:'['+n.x+','+n.y+','+n.w+','+n.h+']',text:n.text||'',
          fillColor:s.fill,strokeColor:s.stroke,color:s.color,fontSize:s.size,fontWeight:s.weight,
          padding:s.padding,textHorizontalAlign:s.align||'left',textVerticalAlign:'top',textAlign:s.align||'left',radius:s.radius
        }}));
      }}
      const store=root.std.store;
      const title={json.dumps(spec.get('title'))};
      if(title) store.workspace.meta.setDocMeta(store.id,{{title}});
      const centerY=Math.min(650,{total_height}/2);
      root.gfx.viewport.setViewport(0.47,[{float(spec.get('width', 2360)) / 2},centerY],false);
      root.gfx.selection.clear();root.std.selection.clear();
      return {{id:store.id,title:title||store.meta?.title,added:ids.length,total:surface.getElementsByType('shape').length,bounds:root.gfx.elementsBound}};
    }})()"""
    return evaluate(target["webSocketDebuggerUrl"], expression)


def load_spec(path: str):
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def screenshot(path: str, y: float | None, zoom: float):
    target, info = switch_edgeless()
    ws_url = target["webSocketDebuggerUrl"]
    if y is not None:
        bounds = info.get("bounds") or {"w": 2360}
        x = float(bounds.get("x", 0)) + float(bounds.get("w", 2360)) / 2
        evaluate(
            ws_url,
            f"document.querySelector('affine-edgeless-root').gfx.viewport.setViewport({zoom},[{x},{y}],false)",
        )
        time.sleep(0.35)
    cdp(ws_url, "Page.bringToFront")
    result = cdp(
        ws_url,
        "Page.captureScreenshot",
        {"format": "png", "captureBeyondViewport": False, "optimizeForSpeed": True},
    )
    output = Path(path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(base64.b64decode(result["data"]))
    return {"path": str(output)}


def close_modals():
    target, _ = find_target(require_root=False)
    return evaluate(
        target["webSocketDebuggerUrl"],
        "(() => { const q='[data-testid=\"modal-close-button\"],[data-testid=\"confirm-modal-cancel\"]'; const xs=[...document.querySelectorAll(q)]; xs.forEach(x=>x.click()); return {closed:xs.length}; })()",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    ensure_parser = commands.add_parser("ensure")
    ensure_parser.add_argument("--relaunch", action="store_true")

    commands.add_parser("info")

    new_parser = commands.add_parser("new")
    new_parser.add_argument("--title", required=True)

    title_parser = commands.add_parser("title")
    title_parser.add_argument("title")

    board_parser = commands.add_parser("board")
    board_parser.add_argument("--spec", required=True)

    eval_parser = commands.add_parser("eval")
    source = eval_parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--expr")
    source.add_argument("--file")

    shot_parser = commands.add_parser("screenshot")
    shot_parser.add_argument("--path", required=True)
    shot_parser.add_argument("--y", type=float)
    shot_parser.add_argument("--zoom", type=float, default=0.47)

    commands.add_parser("close-modals")
    args = parser.parse_args()

    try:
        if args.command == "ensure":
            result = ensure(args.relaunch)
        elif args.command == "info":
            _, result = find_target()
        elif args.command == "new":
            result = new_page(args.title)
        elif args.command == "title":
            result = set_title(args.title)
        elif args.command == "board":
            result = apply_board(load_spec(args.spec))
        elif args.command == "eval":
            expression = args.expr if args.expr is not None else Path(args.file).read_text(encoding="utf-8")
            result = evaluate(current_ws(), expression)
        elif args.command == "screenshot":
            result = screenshot(args.path, args.y, args.zoom)
        elif args.command == "close-modals":
            result = close_modals()
        else:  # pragma: no cover
            raise RuntimeError("Unknown command")
        compact_print(result)
    except Exception as exc:
        compact_print({"error": str(exc)})
        raise SystemExit(2)


if __name__ == "__main__":
    main()
