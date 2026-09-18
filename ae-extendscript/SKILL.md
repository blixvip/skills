---
name: ae-extendscript
description: Drive Adobe After Effects from an agent by writing and running ExtendScript (.jsx) — the result-file bridge that gives you real error feedback, the PNG frame-render loop that lets you see what you built, and the ES3 language traps that break AE scripts. Use whenever the task is to build, fix, keyframe, expression, render, or inspect anything inside After Effects, including "fix this comp", "the expression is broken", "keyframe these layers", "build this animation in AE", or "control After Effects with code".
---

# ae-extendscript

After Effects has no chat interface and no MCP by default. It has a scripting engine. You control it by **writing a `.jsx` file, running it, and reading a result file back** — a real feedback loop, not fire-and-forget.

Do not click. Do not describe steps for the user to perform. Write the script.

## One-time setup (tell the user, once)

**Enable file writing** — without it every result file silently fails:

> Edit → Preferences → Scripting & Expressions → tick **Allow Scripts to Write Files and Access Network** → OK

That is the only manual step. If a script "runs but nothing happened", this is the first thing to check.

## The bridge

Three files, every time:

```
work/
  ae/run.jsx        the script you generate
  ae/result.json    what AE writes back — you read this
```

### Run it

**Windows** (adjust the year to the installed version):

```bash
"/c/Program Files/Adobe/Adobe After Effects 2025/Support Files/AfterFX.exe" -r "C:/work/ae/run.jsx"
```

**macOS:**

```bash
osascript -e 'tell application "Adobe After Effects 2025" to DoScript "$.evalFile(\"/work/ae/run.jsx\")"'
```

`-r` runs the script in the already-open instance and leaves AE open. It returns immediately — **it does not wait, and it does not report errors**. That is exactly why the result file exists.

### The wrapper — never write a bare script

Every script you generate is wrapped like this. The wrapper is what converts a silent failure into a message you can act on.

```jsx
(function () {
    var LOG = [];
    var OUT = new File("C:/work/ae/result.json");
    function log(m) { LOG.push(String(m)); }
    function write(status, err) {
        OUT.encoding = "UTF-8";
        OUT.open("w");
        OUT.write('{"status":"' + status + '","error":' +
                  (err ? '"' + String(err).replace(/"/g, "'") + '"' : 'null') +
                  ',"log":["' + LOG.join('","') + '"]}');
        OUT.close();
    }

    app.beginUndoGroup("agent-run");
    try {

        // ---- work goes here ----
        log("started");

        write("ok", null);
    } catch (e) {
        write("error", e.toString() + " @line " + e.line);
    } finally {
        app.endUndoGroup();
    }
})();
```

Then read `result.json`. `status: "error"` gives you the message and the line — fix and re-run. Never assume it worked.

**`app.beginUndoGroup` / `endUndoGroup` is mandatory.** It makes the entire agent run a single Ctrl+Z for the user. Without it you have scattered their undo history and they cannot back out of your work.

## Seeing what you built

You are not blind. `CompItem.saveFrameToPng` renders a single frame to disk:

```jsx
comp.saveFrameToPng(comp.time, new File("C:/work/ae/preview.png"));
// or a specific time, in seconds:
comp.saveFrameToPng(1.5, new File("C:/work/ae/f_1500.png"));
```

Render 3–5 frames across the animation, then read them as images. This closes the loop: build → render frames → look → correct. Do this before telling the user anything is done. A composition that scripts cleanly can still be visually wrong.

## The ES3 traps that break AE scripts

The ExtendScript engine is ancient JavaScript. Modern syntax does not fail loudly — it fails at parse time, which means **the whole file does nothing**.

| Do not use | Use instead |
|---|---|
| `let` / `const` | `var` |
| Arrow functions | `function () {}` |
| Template literals | string concatenation with `+` |
| `JSON.parse` / `JSON.stringify` | build strings by hand (as in the wrapper above) |
| `Array.forEach` / `map` / `filter` | `for (var i = 0; i < a.length; i++)` |
| `String.trim`, `Array.indexOf` | write the helper yourself |
| Default / rest parameters | `arguments`, and explicit defaults |
| `class` | function constructors |

Other traps that cost real time:

- **Time is in seconds, not frames.** Convert with `comp.frameDuration` (`frame * comp.frameDuration`).
- **Collections are 1-indexed.** `comp.layer(1)` is the top layer; `app.project.item(1)` is the first item.
- **Colors are arrays of 0–1 floats**, not 0–255 and not hex. Write a `hex()` helper (see Appendix A).
- **Paths:** use forward slashes in `new File("C:/...")`. Backslashes need doubling and will bite you.
- **Text layers:** you cannot mutate the TextDocument in place. Read it into a var, change it, assign it back.
- **`$.writeln` goes nowhere useful** when run headless — log to the result file instead.
- **`app.project.file` is `null`** on an unsaved project. Guard before deriving paths from it.

## Discover, do not guess

Effect and property identifiers are `matchName` strings like `"ADBE Gaussian Blur 2"`. Guessing them wastes runs. Dump the real ones from a layer the user already set up:

```jsx
var L = app.project.activeItem.layer(1);
var fx = L.property("ADBE Effect Parade");
for (var i = 1; i <= fx.numProperties; i++) {
    log(fx.property(i).name + "  ->  " + fx.property(i).matchName);
}
```

Same pattern for any property group. When you need an effect you have not used before, ask the user to apply it once by hand to a scratch layer, dump its matchName and parameter names, then script it forever after.

## What to build in AE — and what not to

After Effects is the right engine when the graphic must **live on the footage**: tracked elements, plate integration, roto, real-camera 3D, particles, complex masks and mattes, and any fix to a project the user already has open.

It is the wrong engine for large programmatic sequences, data-driven charts, or anything you would rather express as code — those belong in Remotion or HyperFrames, rendered with alpha and imported. See `motion-pipeline` for the engine table.

## Fixing an existing project

When the user says a comp is broken:

1. **Inspect first, change nothing.** Script a walk of comps → layers → properties, logging expression errors, missing footage, and disabled layers. Read the result.
2. **Report what you found** before you fix it. The user often knows which of the four things they meant.
3. Fix inside one undo group.
4. Render frames and confirm.

The most common real breakages: an expression referencing a renamed layer, an effect whose parameter index shifted, footage relinked to a different frame rate, and a parent chain that lost its null.

## Rules

- Keyframes are worthless without easing. Every `setValueAtTime` is followed by `setTemporalEaseAtKey` — see Appendix A. Default linear keyframes are the AE equivalent of a flat background.
- Set `layer.startTime` / stagger entrances; never bring elements on together.
- Name every layer you create. `Shape Layer 7` is unmaintainable for the human who inherits the comp.
- Put related layers in a pre-comp or a labelled group. The user has to work in this project after you leave.
- Do not `app.project.save()` over the user's file without being asked. Use `saveWithDialog`, or save a copy alongside.

Appendix A has working code for comps, text, shapes, eased keyframes, expressions, 3D cameras, effects, imports, frame renders, and the render queue.

---

# Appendix A · ExtendScript recipes


All snippets assume they sit inside the wrapper from `SKILL.md` (undo group + try/catch + result file). ES3 only — `var`, no arrows, no template literals.

## Helpers — paste these at the top

```jsx
function hex(h) {                     // "#e8721f" -> [r,g,b] in 0..1
    h = h.replace("#", "");
    return [parseInt(h.substr(0,2),16)/255,
            parseInt(h.substr(2,2),16)/255,
            parseInt(h.substr(4,2),16)/255];
}
function f(comp, n) { return n * comp.frameDuration; }   // frames -> seconds

// Eased keyframes. inSpeed/outSpeed 0, influence 0..100.
// Big outgoing influence on the first key = "out-expo" feel.
function ease(prop, keyIndex, inInf, outInf) {
    var eIn  = new KeyframeEase(0, inInf  || 33);
    var eOut = new KeyframeEase(0, outInf || 33);
    var dim  = prop.propertyValueType === PropertyValueType.ThreeD_SPATIAL ||
               prop.propertyValueType === PropertyValueType.ThreeD ? 3 :
               (prop.propertyValueType === PropertyValueType.TwoD_SPATIAL ||
                prop.propertyValueType === PropertyValueType.TwoD ? 2 : 1);
    var aIn = [], aOut = [];
    for (var i = 0; i < dim; i++) { aIn.push(eIn); aOut.push(eOut); }
    prop.setInterpolationTypeAtKey(keyIndex,
        KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
    prop.setTemporalEaseAtKey(keyIndex, aIn, aOut);
}

// Two eased keys in one call — the move you will use most.
function animate(prop, t0, v0, t1, v1, inInf, outInf) {
    prop.setValueAtTime(t0, v0);
    prop.setValueAtTime(t1, v1);
    ease(prop, 1, 0,  outInf === undefined ? 85 : outInf);   // launch fast
    ease(prop, 2, inInf === undefined ? 75 : inInf, 0);      // settle slow
}
```

`animate(p, 0, 0, 0.6, 100)` with the defaults gives a strong ease-out — the premium feel. Symmetric influence (33/33) is the AE default and reads as generic.

## Composition

```jsx
var comp = app.project.items.addComp("SC01_hook", 1920, 1080, 1, 6, 30);
comp.bgColor = hex("#12100e");
comp.openInViewer();
```

Existing comp by name:

```jsx
function findComp(name) {
    for (var i = 1; i <= app.project.numItems; i++) {
        var it = app.project.item(i);
        if (it instanceof CompItem && it.name === name) return it;
    }
    return null;
}
var comp = findComp("SC01_hook") || app.project.activeItem;
```

## Text layer

```jsx
var t = comp.layers.addText("650M views");
t.name = "stat";

var src = t.property("Source Text");
var td  = src.value;              // read out
td.font       = "Inter-Bold";     // PostScript name, not the display name
td.fontSize   = 140;
td.fillColor  = hex("#faf8f5");
td.tracking   = -30;
td.justification = ParagraphJustification.LEFT_JUSTIFY;
src.setValue(td);                 // assign back — mutating td alone does nothing

t.property("Transform").property("Position").setValue([160, 620]);
```

Find PostScript font names by dumping them once: `for (var i=0;i<app.fonts.allFonts.length;i++) log(app.fonts.allFonts[i].postScriptName);`

## Shape, solid, null, camera, light

```jsx
var sh   = comp.layers.addShape();
var sol  = comp.layers.addSolid(hex("#1c1917"), "bg", comp.width, comp.height, 1, comp.duration);
var nul  = comp.layers.addNull(comp.duration);
var cam  = comp.layers.addCamera("cam", [comp.width/2, comp.height/2]);
var lit  = comp.layers.addLight("key", [comp.width/2, comp.height/2]);
lit.lightType = LightType.POINT;
lit.property("Intensity").setValue(120);
lit.property("Color").setValue(hex("#e8721f"));
```

## The signature entrance: pop-blur-fade, staggered

```jsx
function popIn(layer, t0) {
    var tr = layer.property("Transform");
    animate(tr.property("Opacity"),  t0, 0, t0 + 0.45, 100);
    animate(tr.property("Scale"),    t0, [92,92], t0 + 0.55, [100,100]);

    var p = tr.property("Position").value;
    animate(tr.property("Position"), t0, [p[0], p[1] + 40], t0 + 0.55, p);

    var fx = layer.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
    var b  = fx.property("ADBE Gaussian Blur 2-0001");   // Blurriness
    animate(b, t0, 24, t0 + 0.40, 0);
    fx.property("ADBE Gaussian Blur 2-0003").setValue(true); // repeat edge pixels
}

// stagger — never bring them on together
var layers = [l1, l2, l3];
for (var i = 0; i < layers.length; i++) popIn(layers[i], 0.2 + i * 0.09);
```

## Parenting and a 3D camera push

```jsx
child.parent = nul;               // null is now the rig

cam.threeDLayer = true;
var pos = cam.property("Transform").property("Position");
animate(pos, 0, [960, 540, -2600], comp.duration, [960, 540, -2050], 40, 40);
```

Slow, continuous, gently eased. A camera that stops moving makes the frame read as a slide.

## Effects, by matchName

```jsx
var parade = layer.property("ADBE Effect Parade");
var glow   = parade.addProperty("ADBE Glo2");     // Glow
var fill   = parade.addProperty("ADBE Fill");
fill.property("Color").setValue(hex("#e8721f"));
```

**Do not guess matchNames.** Apply the effect once by hand, then dump it:

```jsx
var fx = layer.property("ADBE Effect Parade");
for (var i = 1; i <= fx.numProperties; i++) {
    var e = fx.property(i);
    log(e.name + " -> " + e.matchName);
    for (var j = 1; j <= e.numProperties; j++)
        log("    " + e.property(j).name + " -> " + e.property(j).matchName);
}
```

## Expressions

```jsx
var p = layer.property("Transform").property("Position");
p.expression =
    "var lead = thisComp.layer('ball');\n" +
    "var q = lead.transform.position;\n" +
    "[q[0], 980];";
```

Rules that prevent the usual breakage:

- Reference layers **by name**, and make sure the name is one you set — renamed layers are the top cause of expression errors.
- Wrap anything that can fail: `try { ... } catch (e) { value }` so a missing layer degrades instead of erroring.
- Prefer expressions over hundreds of keyframes for follow, wiggle, loop, and rig behaviour — they survive a timing change; keyframes do not.
- To find existing errors, walk every property and read `prop.expressionError`.

Useful patterns:

```
// inertial follow
delay = 0.08; thisComp.layer("lead").transform.position.valueAtTime(time - delay)

// loop the last two keys
loopOut("cycle")

// eased, expression-driven entrance (no keyframes at all)
t = time - inPoint; d = 0.6;
ease(t, 0, d, 40, 0)
```

## Import footage and place it

```jsx
var io = new ImportOptions(new File("C:/work/06-renders/sc03.mov"));
if (io.canImportAs(ImportAsType.FOOTAGE)) io.importAs = ImportAsType.FOOTAGE;
var item  = app.project.importFile(io);
var layer = comp.layers.add(item);
layer.startTime = 2.4;
```

A ProRes 4444 render from Remotion or HyperFrames imports with alpha intact and drops straight onto the plate — the normal way to combine engines.

## Render a frame (your eyes)

```jsx
comp.saveFrameToPng(0.0,  new File("C:/work/ae/f000.png"));
comp.saveFrameToPng(1.0,  new File("C:/work/ae/f100.png"));
comp.saveFrameToPng(comp.duration - comp.frameDuration,
                    new File("C:/work/ae/fend.png"));
```

Then read the PNGs. Do this before reporting completion.

## Render queue

```jsx
var rq = app.project.renderQueue;
var it = rq.items.add(comp);
it.outputModule(1).applyTemplate("Lossless with Alpha");
it.outputModule(1).file = new File("C:/work/06-renders/" + comp.name + ".mov");
rq.render();
```

`rq.render()` **blocks** until done — unlike `-r`, so the run genuinely finishes before your result file is written. Template names must already exist in the user's AE; list them with `it.outputModule(1).templates`.

## Inspect a broken project

```jsx
for (var i = 1; i <= app.project.numItems; i++) {
    var it = app.project.item(i);
    if (it instanceof FootageItem && it.footageMissing) log("MISSING: " + it.name);
    if (!(it instanceof CompItem)) continue;
    log("COMP " + it.name + " " + it.width + "x" + it.height + " @" + it.frameRate);
    for (var L = 1; L <= it.numLayers; L++) {
        var lay = it.layer(L);
        if (!lay.enabled) log("  disabled: " + lay.name);
        scanProps(lay, "  " + lay.name);
    }
}
function scanProps(g, path) {
    for (var i = 1; i <= g.numProperties; i++) {
        var p = g.property(i);
        if (p.numProperties !== undefined && p.numProperties > 0) {
            scanProps(p, path + "/" + p.name);
        } else if (p.canSetExpression && p.expressionEnabled && p.expressionError) {
            log("EXPR ERROR " + path + "/" + p.name + ": " + p.expressionError);
        }
    }
}
```

Run this first on any "my project is broken" request. Report before repairing.
