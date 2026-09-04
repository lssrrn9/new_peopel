# KK-5S Cold-Cut Flying Saw User Manual

Web edition of the **KK-5S Cold-Cut Flying Saw** operator manual (Shijiazhuang Aogang Machinery Co., Ltd., May 2019 V1.36). The control system is KaiKong KK-5S.

## Open the manual

Open [`index.html`](index.html) in a browser, or serve the repository root:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

| Page | Contents |
|---|---|
| [index.html](index.html) | Cover, quick-start sequence, chapter index |
| [safety.html](safety.html) | Mechanical and electrical safety |
| [parameters.html](parameters.html) | HMI map and every production / servo parameter |
| [functions.html](functions.html) | Modes, power, jog, homing, clamp/cut, memory |
| [operation.html](operation.html) | Power-on through automatic production and encoder sync |

HMI screenshots and diagrams are in [`assets/img/`](assets/img/). The original Word file is in [`original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx`](original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx).

Regenerate the HTML from [`tools/build_manual.py`](tools/build_manual.py) after content edits:

```bash
python3 tools/build_manual.py
```

## Source

*76 Cold-Cut Flying Saw User Manual*, Aogang Machinery / KaiKong, May 2019 V1.36.
