# AFFiNE native protocol

Read only for recovery or unsupported custom operations.

## Connection

- Native executable: newest `%LOCALAPPDATA%\AFFiNE\app-*\AFFiNE.exe`
- Launch arguments: `--remote-debugging-address=127.0.0.1 --remote-debugging-port=9222`
- Discovery: `http://127.0.0.1:9222/json`
- Connect to `webSocketDebuggerUrl` with no WebSocket `Origin` header.
- Renderer URLs contain `/workspace/`. Target IDs change after reloads; rediscover rather than caching across navigation.

## Stable selectors

```text
[data-testid="sidebar-new-page-button"]
[data-testid="switch-page-mode-button"]
[data-testid="switch-edgeless-mode-button"]
[data-testid="modal-close-button"]
[data-testid="confirm-modal-cancel"]
affine-page-root
affine-edgeless-root
```

## Compact inspection

```javascript
(() => {
  const e = document.querySelector('affine-edgeless-root');
  const p = document.querySelector('affine-page-root');
  const root = e || p;
  return {
    title: document.title,
    id: root?.std?.store?.id ?? null,
    mode: e ? 'edgeless' : p ? 'page' : null,
    count: e?.surfaceBlockModel?.getElementsByType('shape').length ?? 0,
    bounds: e?.gfx?.elementsBound ?? null,
    zoom: e?.gfx?.viewport?.zoom ?? null
  };
})()
```

## Edgeless API

```javascript
const root = document.querySelector('affine-edgeless-root');
const surface = root.surfaceBlockModel;

const id = surface.addElement({
  type: 'shape',
  shapeType: 'rect',
  shapeStyle: 'General',
  strokeStyle: 'solid',
  strokeWidth: 2,
  filled: true,
  fontFamily: 'blocksuite:surface:Inter',
  xywh: '[0,0,600,240]',
  text: 'Content',
  fillColor: '#F5F2EA',
  strokeColor: '#8C8678',
  color: '#292722',
  fontSize: 16,
  fontWeight: 400,
  padding: [22, 20],
  textHorizontalAlign: 'left',
  textVerticalAlign: 'top',
  textAlign: 'left',
  radius: 14
});

surface.updateElement(id, { text: 'Updated' });
```

List shapes compactly:

```javascript
surface.getElementsByType('shape').map(x => ({
  id: x.id,
  text: x.text?.toString().slice(0, 80),
  xywh: x.xywh
}));
```

## Persist title

Do not assign `store.meta.title`; that may be transient. Use collection metadata:

```javascript
const store = (document.querySelector('affine-edgeless-root') ||
  document.querySelector('affine-page-root')).std.store;
store.workspace.meta.setDocMeta(store.id, { title: 'Exact title' });
```

## Viewport

```javascript
const root = document.querySelector('affine-edgeless-root');
const fit = root.gfx.viewport.getFitToScreenData(root.gfx.elementsBound);
root.gfx.viewport.setViewport(fit.zoom, [fit.centerX, fit.centerY], false);
root.gfx.selection.clear();
root.std.selection.clear();
```

For a readable regional check, prefer a fixed zoom and center:

```javascript
root.gfx.viewport.setViewport(0.47, [1180, 650], false);
```

## Recovery

### Target disappeared

Refetch `/json`; choose the visible workspace renderer with an AFFiNE root.

### Page opened in Page mode

Click `[data-testid="switch-edgeless-mode-button"]`, wait, then rediscover the root.

### Sync/sign-in modal appeared

Click the close or cancel test ID. Never enter credentials or verification codes.

### New document has an old route

Trust the active root store ID, not `location.href`. AFFiNE may reuse a renderer and update document state before its route stabilizes.

### Screenshot hangs

Call `Page.bringToFront`, use `captureBeyondViewport: false` and `optimizeForSpeed: true`, then retry once. Capture a readable region instead of the entire dense board.

### Text clips

Reduce only the affected node font or increase its row height. Do not globally rebuild. Estimate line capacity before creation; the bundled helper auto-sizes rows.
