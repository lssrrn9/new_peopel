#!/usr/bin/env python3
"""Generate static HTML pages for the KK-5S operator manual."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT

NAV = """
      <div class="group">Manual</div>
      <a href="index.html">Cover &amp; quick start</a>
      <a href="safety.html">Safety precautions</a>
      <div class="group">Chapter 1</div>
      <a href="parameters.html">Parameter description</a>
      <a class="sub" href="parameters.html#screen-overview">1.1 Screen overview</a>
      <a class="sub" href="parameters.html#main-page">1.2.1 Main page</a>
      <a class="sub" href="parameters.html#length">1.2.2 Length scheduling</a>
      <a class="sub" href="parameters.html#tube">1.2.3 Tube type</a>
      <a class="sub" href="parameters.html#system">1.2.4 System parameters</a>
      <a class="sub" href="parameters.html#manual-params">1.2.5 Manual parameters</a>
      <a class="sub" href="parameters.html#motor">1.2.6 Motor parameters</a>
      <div class="group">Chapter 2</div>
      <a href="functions.html">System functions</a>
      <a class="sub" href="functions.html#modes">2.1 Operating modes</a>
      <a class="sub" href="functions.html#power">2.2 Power management</a>
      <a class="sub" href="functions.html#home">2.4 Homing</a>
      <div class="group">Chapter 3</div>
      <a href="operation.html">Operating instructions</a>
      <a class="sub" href="operation.html#power-on">3.1 Power-on</a>
      <a class="sub" href="operation.html#cut">3.6 Manual cutting</a>
      <a class="sub" href="operation.html#auto">3.8 Automatic mode</a>
      <a class="sub" href="operation.html#sync">3.12 Synchronization</a>
"""


def page(filename, title, crumb, body, extra_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — KK-5S Cold-Cut Flying Saw</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/manual.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <button class="menu-btn" type="button" aria-label="Open menu">☰</button>
  <aside class="sidebar">
    <div class="brand">
      <img src="assets/img/logo-aogang-header.jpeg" alt="AOGANG">
      <div class="model">KK-5S</div>
      <div class="sub">Cold-cut flying saw</div>
    </div>
    <div class="search-wrap">
      <input id="manual-search" type="search" placeholder="Search the manual…" autocomplete="off">
      <div id="search-results" class="search-results"></div>
    </div>
    <nav class="nav">{NAV}
    </nav>
    <div class="sidebar-foot">Shijiazhuang Aogang Machinery<br>May 2019 · V1.36</div>
  </aside>
  <div class="main">
    <div class="topbar">
      <div class="crumb">{crumb}</div>
      <div class="meta">KK-5S · User manual V1.36</div>
    </div>
    <article id="content" class="content {extra_class}">
{body}
      <footer class="page-foot">
        KK-5S Cold-Cut Flying Saw User Manual · Shijiazhuang Aogang Machinery Co., Ltd. · May 2019 V1.36.
        Control system: KaiKong KK-5S. This web edition is a structured conversion of the original instruction manual.
      </footer>
    </article>
  </div>
  <script src="assets/js/manual.js"></script>
</body>
</html>
"""


def fig(src, cap):
    return f"""      <figure>
        <img src="assets/img/{src}" alt="{cap}">
        <figcaption>{cap}</figcaption>
      </figure>"""


def table(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = []
    for row in rows:
        tds = []
        for i, cell in enumerate(row):
            if i == 3:
                cls = "dot-set" if cell == "●" else "dot-ro"
                tds.append(f'<td class="{cls}">{cell}</td>')
            else:
                tds.append(f"<td>{cell}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f"""      <div class="table-wrap">
        <table>
          <thead><tr>{head}</tr></thead>
          <tbody>
            {''.join(body)}
          </tbody>
        </table>
      </div>"""


def param(name, meta, text):
    metas = "".join(f"<span>{m}</span>" for m in meta)
    return f"""      <div class="param">
        <h4>{name}</h4>
        <div class="meta-row">{metas}</div>
        <p>{text}</p>
      </div>"""


INDEX = """
      <div class="hero">
        <div class="kicker" style="color:#f0b8b0">Operator manual</div>
        <h1>KK-5S Cold-Cut Flying Saw</h1>
        <p class="lede">Control-system user manual for the AOGANG mill-line flying saw. Covers HMI parameters, homing, simulation, automatic cutting, and synchronization.</p>
        <div class="hero-logos">
          <img src="assets/img/logo-aogang-header.jpeg" alt="AOGANG">
          <img src="assets/img/logo-kaikong.jpeg" alt="KaiKong">
        </div>
        <div class="badges">
          <span class="badge">Aogang Machinery</span>
          <span class="badge">KaiKong KK-5S</span>
          <span class="badge">May 2019 V1.36</span>
        </div>
      </div>
      <div class="callout danger">
        <strong>Read safety first</strong>
        Moving saw carriages, rotating blades, and live cabinet voltage can cause severe injury. Complete <a href="safety.html">Safety precautions</a> before power-up, homing, or production.
      </div>
      <h2>Quick start</h2>
      <p>Use this sequence after a cold start. Details and abort conditions are in <a href="operation.html">Chapter 3</a>.</p>
      <ol class="steps">
        <li>Close the main cabinet breaker, then press the control-panel power button. Wait until Drive, Feed, and Sawing power lamps are steady (~60 s). Do not operate during initialization.</li>
        <li>Confirm the mode selector is in <strong>Manual</strong>. If the clamp is hydraulic, start the hydraulic unit.</li>
        <li>Home the drag (saw-carriage) axis, then home the feed axis with material clamped in the fixture. Reset cancels either move.</li>
        <li>Enter length and tube/saw-blade parameters. Press <strong>Calculate</strong> and confirm maximum line speed is acceptable.</li>
        <li>Prove the cut with a manual static cut. The forming mill must be stationary.</li>
        <li>Run <strong>Simulation</strong> with an empty fixture to verify carriage motion, then switch to <strong>Automatic</strong> only after material is in the clamp and both axes are at home.</li>
      </ol>
      <h2>Contents</h2>
      <div class="cards">
        <a class="card" href="safety.html">
          <div class="num">00</div>
          <h3>Safety precautions</h3>
          <p>Mechanical and electrical rules that apply to every procedure in this manual.</p>
        </a>
        <a class="card" href="parameters.html">
          <div class="num">01</div>
          <h3>Parameter description</h3>
          <p>HMI map, factory defaults, and the meaning of every production and servo setting.</p>
        </a>
        <a class="card" href="functions.html">
          <div class="num">02</div>
          <h3>System functions</h3>
          <p>Modes, power, jog, homing, clamp/cut, short/long length, and length memory.</p>
        </a>
        <a class="card" href="operation.html">
          <div class="num">03</div>
          <h3>Operating instructions</h3>
          <p>Power-on through automatic production, schedules, memory points, and encoder sync.</p>
        </a>
      </div>
      <h2>About this edition</h2>
      <p>Source document: <em>76 Cold-Cut Flying Saw User Manual</em>, Shijiazhuang Aogang Machinery Co., Ltd., May 2019 V1.36. The HMI screenshots and diagrams are taken from that file. The original Word file is stored at <a href="original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx">original/Cold_Cutting_Flying_Saw_Instruction_Manual.docx</a>.</p>
      <p>On HMI tables, <span class="dot-set">●</span> means the operator can set the value; <span class="dot-ro">○</span> means display-only. Where the original English translation used inconsistent units, the detailed description is treated as the authority and the table unit is noted.</p>
"""

SAFETY = """
      <div class="kicker">Required reading</div>
      <h1>Safety precautions</h1>
      <p class="lede">These instructions are the minimum requirements for personal safety. All operations in later chapters must also comply with them.</p>
      <div class="callout danger">
        <strong>Consequence of operating error</strong>
        If an operating error occurs while the flying saw is connected to the mill, it can damage the machinery and cause personal injury.
      </div>
      <h2>Mechanical</h2>
      <ul>
        <li>Non-professionals must not set up, disassemble, or repair the equipment without supervision.</li>
        <li>Do not touch any moving parts of the equipment while it is in operation.</li>
        <li>When performing mechanical maintenance or troubleshooting, ensure that the saw carriage is in the <strong>disengaged</strong> position.</li>
        <li>Follow the steps and instructions in this user manual.</li>
      </ul>
      <h2>Electrical</h2>
      <ul>
        <li>Inspection, maintenance, and repair of the electrical system must be performed by personnel qualified to operate electrical systems.</li>
        <li>Before opening the main control cabinet, confirm that power has been completely shut off.</li>
        <li>Do not touch any internal electrical components or terminal blocks while power is on (when the green light on the main control cabinet panel is lit).</li>
        <li>Do not touch the terminal blocks inside the cabinet within <strong>5 minutes</strong> of turning off the power.</li>
        <li>Ground the grounding terminal inside the cabinet.</li>
        <li>Do not modify this product (including adding electrical components, using the power supply inside the cabinet, or adding wiring).</li>
      </ul>
      <div class="callout warn">
        <strong>Cabinet power</strong>
        Once the main circuit breaker is closed, the red power indicator on the cabinet door stays lit and the cabinet interior is energized. Unqualified personnel must stay away from the cabinet.
      </div>
      <h2>Process hazards called out later in this manual</h2>
      <ul>
        <li><a href="operation.html#cut">Manual cutting</a> — if the forming mill moves during a static cut, the saw blade can be destroyed.</li>
        <li><a href="operation.html#sim">Simulation</a> — material in the fixture, or mill motion during simulation, can overturn the saw carriage.</li>
        <li><a href="operation.html#torque">Feed homing on thin wall</a> — wall thickness under about 1 mm can bend and record a false origin.</li>
        <li><a href="operation.html#memory">Memory-point resume</a> — moving the strip after a stop makes the stored length wrong and can produce an over-length part.</li>
      </ul>
"""

PARAMS = f"""
      <div class="kicker">Chapter 1</div>
      <h1>Parameter description</h1>
      <p class="lede">The KK-5S touchscreen is the primary station for production settings and status. This chapter maps every page and documents each parameter.</p>

      <h2 id="screen-overview">1.1 Screen overview</h2>
      <p>On each screen there are two rows of switching buttons at the bottom. The bottom row is primary navigation and is shown on every page. The top row is secondary navigation and appears only for the active primary page.</p>
{fig("fig-1-1-topology.png", "Figure 1-1. Touchscreen topology for the KK-5S cold-cut flying saw control system")}
{fig("fig-1-2-main.png", "Figure 1-2. Main screen of the KK-5S cold-cut flying saw control system")}
      <ul>
        <li><strong>Production Status</strong> — Production Status, Length Settings, Pipe Type Parameters, and Simulation Status. Daily length, quantity, and material parameters live here.</li>
        <li><strong>System Settings</strong> — System Parameters, Manual Parameters, and Motor Parameters (plus Sync Parameters on the HMI).</li>
        <li><strong>Manual Operation</strong> — jog, home, clamp, cut, and axis power buttons.</li>
        <li><strong>System Diagnostics</strong> — inputs, outputs, and current.</li>
        <li><strong>Alarm Information</strong> — current alarms and historical alarms.</li>
        <li><strong>Company Information</strong> — manufacturer contact details.</li>
        <li><strong>Language</strong> — Chinese / English.</li>
      </ul>

      <h2 id="main-page">1.2.1 Main page</h2>
      <p>The main page is the production-status view shown in Figure 1-2. Values above the divider are also visible from other windows.</p>
{table(
    ["Parameter", "Description", "Unit", "Set", "Default"],
    [
        ["Production line speed", "Current mill speed in automatic mode; live display", "m/min", "○", "—"],
        ["Maximum line speed", "Maximum allowed speed for the current parameters", "m/min", "○", "—"],
        ["Current material length", "Distance this piece has already advanced", "mm", "○", "—"],
        ["Current cut length", "Cut-off length of the active job (see §3.9)", "mm", "○", "—"],
        ["Current saw-carriage position", "Carriage position relative to origin", "mm", "○", "—"],
        ["Current feed position", "Feed position relative to origin", "mm", "○", "—"],
        ["Quantity produced", "Pieces already produced on the current order; ±1 for tracking", "pieces", "○", "—"],
        ["Set production quantity", "Target quantity of the current schedule", "pieces", "○", "—"],
    ],
)}
      <p>When operating in automatic mode, keep mill speed at or below the displayed maximum line speed.</p>

      <h2 id="length">1.2.2 Length scheduling page</h2>
{fig("fig-1-3-length.png", "Figure 1-3. KK-5S length scheduling page")}
{table(
    ["Parameter", "Description", "Unit", "Set", "Default"],
    [
        ["Orders 1–10 set length", "Cut length for each order. Range 0–104,857.5. Selected order length must not be 0", "mm", "●", "6000"],
        ["Orders 1–10 set quantity", "Pieces for each order. Quantity 0 means unlimited", "pieces", "●", "6666"],
        ["Current production order number", "Currently selected order", "—", "○", "—"],
        ["Current production length", "Length of the selected order", "mm", "○", "—"],
        ["Current quantity", "Pieces produced so far on the selected order", "pieces", "○", "—"],
    ],
)}
      <div class="callout note">
        <strong>Scheduling</strong>
        If you do not need multi-order scheduling, use a single enabled order for the production length. The order’s <em>Select / ENB</em> state must be on, or that length is not executed.
      </div>

      <h2 id="tube">1.2.3 Tube type parameters</h2>
{fig("fig-1-4-tube.png", "Figure 1-4. KK-5S pipe / tube profile parameters page")}
{table(
    ["Parameter", "Description", "Unit", "Set", "Default"],
    [
        ["Feed distance", "Feed-axis travel during the cut. Round tube: enter diameter. Square / special: equivalent feed for a full cut", "mm", "●", "32"],
        ["Material wall thickness", "Shown when Round Tube is selected; sets slow-feed zones at both walls", "mm", "●", "2"],
        ["Slow-speed % first segment", "Square / special only: slow-feed zone at the start of the cut (typical 5–10%)", "%", "●", "10"],
        ["Slow-speed % final segment", "Square / special only: slow-feed zone at the end of the cut (typical 20–45%)", "%", "●", "20"],
        ["Tube type", "Round, square, or special-shaped", "—", "●", "—"],
        ["Feed per tooth, initial", "Low-speed tooth feed at the start of the cut", "mm", "●", "0.04"],
        ["Feed per tooth, high-speed", "Tooth feed in the high-speed portion of the cut", "mm", "●", "0.08"],
        ["Feed per tooth, final", "Low-speed tooth feed at the end of the cut", "mm", "●", "0.04"],
        ["Saw blade linear speed", "Peripheral speed at the tooth tip. Must satisfy: linear speed × 1000 × reduction / (diameter × π) &lt; saw-motor max speed", "m/min", "●", "200"],
        ["Number of saw-blade teeth", "Actual tooth count. Wrong value shortens blade life or blocks the cycle", "teeth", "●", "200"],
        ["Saw blade diameter", "Actual diameter. Re-measure after regrinding", "mm", "●", "350"],
        ["Recommended cutting time", "Calculated from current tube and blade data; a conservative blade-protection reference", "s", "○", "—"],
        ["Maximum production speed", "Maximum line speed at current parameters", "m/min", "○", "—"],
    ],
)}
{param("Wall thickness vs. slow-speed percentages",
       ["Round: wall thickness", "Square / special: first &amp; last %"],
       "During feed, zones that need more cutting force (tube walls) run at the low-speed tooth feed to protect the blade; after those zones the axis returns to high-speed tooth feed. Too large a slow zone costs cycle time; too small a zone can shatter the blade. For square tube, wall thickness and exit angle both change the percentages — inspect the cutting curve after material identification and trim the values.")}
{param("Feed per tooth (STFL)",
       ["Round typical: 0.03–0.05 mm slow / 0.08–0.12 mm high", "Square typical: 0.01–0.07 mm slow / 0.1–0.14 mm high"],
       "STFL is the feed-axis move per one tooth of blade rotation. Start from the blade manufacturer’s chart, then trim to the cut. Too high damages the blade; too low only slows the mill.")}

      <h2 id="system">1.2.4 System parameters</h2>
{fig("fig-1-12-system.png", "Figure 1-12. KK-5S system parameters page")}
{table(
    ["Parameter", "Description", "Unit", "Set", "Default"],
    [
        ["Saw-car forward acceleration", "Acceleration on the forward (tracking) segment", "m/s²", "●", "3"],
        ["Saw-car forward deceleration", "Deceleration on the forward segment", "m/s²", "●", "4"],
        ["Saw-car return acceleration", "Acceleration on the return segment", "m/s²", "●", "4"],
        ["Saw-car return deceleration", "Deceleration on the return segment", "m/s²", "●", "3"],
        ["Saw-car jerk", "Jerk of the drive feed motor on forward and return strokes", "m/s³", "●", "50"],
        ["Clamping delay", "After the carriage reaches the sync zone, wait this long before outputting clamp", "s", "●", "0.05"],
        ["Cut-off delay", "Time allotted for the clamp to actuate after the clamp command", "s", "●", "0.01"],
        ["Return delay", "After the blade is back at origin and unclamp is output, wait this long before decelerating the carriage", "s", "●", "0.01"],
        ["Slow-speed allowance (outer)", "Allowance outside the wall-thickness slow zone (covers mechanical error)", "mm", "●", "1 (HMI example 0.05)"],
        ["Slow-speed allowance (inner)", "Allowance inside the wall-thickness slow zone", "mm", "●", "1 (HMI example 0.10)"],
        ["Distance to feed origin", "After feed-home contact, the blade retracts this distance", "mm", "●", "5"],
        ["Feed acceleration", "Acceleration of the feed servo", "m/s²", "●", "2"],
        ["Real-time clock", "Controller clock set / read", "—", "●", "—"],
    ],
)}
      <div class="callout warn">
        <strong>Closed-loop carriage motion</strong>
        The carriage is closed-loop: acceleration/deceleration curves are built from these values while the drive shaft tracks strip speed. Too high → motor load and overshoot into the sync or zero-speed zones, which hurts position and settling time. Too low → slower mill speed. Set from the actual mechanical mass.
      </div>
      <p>Clamping delay exists because the carriage overshoots slightly when it enters the sync zone. Clamping during that overshoot can desynchronize the cut. Do not set the delay larger than needed — it reduces maximum line speed.</p>

      <h2 id="manual-params">1.2.5 Manual parameters</h2>
{fig("fig-1-12-manual-params.png", "Figure 1-12 (continued). KK-5S manual parameters page")}
{table(
    ["Parameter", "Description", "Unit", "Set", "Default"],
    [
        ["Driven servo jog speed", "Carriage speed during manual forward/reverse", "mm/s", "●", "100"],
        ["Drive servo home speed 1", "Speed while seeking the rear limit during drag-home", "mm/s", "●", "100 (table 50)"],
        ["Drive servo home speed 2", "Speed of the forward move after the rear limit is found", "mm/s", "●", "100"],
        ["Drag servo home distance", "Distance the carriage travels forward after the rear limit", "mm", "●", "50"],
        ["Lubrication pump run time", "On-time of each lube cycle", "s", "●", "15"],
        ["Lubrication pump stop time", "Off interval between lube cycles", "s", "●", "1200"],
        ["Hydraulic station pressure limit (max)", "Hydraulic high-pressure limit when a hydraulic clamp is fitted", "MPa", "●", "12"],
        ["Hydraulic station pressure limit (min)", "Hydraulic low-pressure limit", "MPa", "●", "15"],
        ["Feed servo jog speed", "Feed-axis speed in manual jog", "mm/s", "●", "10"],
        ["Feed servo home speed 1", "Speed retracting to the feed rear limit during feed-home", "mm/s", "●", "10"],
        ["Feed servo home speed 2", "Speed advancing to find the material after the rear limit", "mm/s", "●", "5"],
        ["Feed home distance", "Retract distance after the blade contacts the material", "mm", "●", "5"],
        ["Feed servo home torque limit", "Torque used to drive into the material during feed-home. Typical 5–15%", "%", "●", "5"],
    ],
)}
      <p>If home torque is high but the motor still cannot drive the load, the feed screw may be dry. Check that lubrication lines are open before raising torque further — excess torque can damage the strip and the blade.</p>
{fig("fig-3-2-torque.png", "Feed torque test controls on the manual-parameters / machine-learning page (see §3.4)")}

      <h2 id="motor">1.2.6 Motor parameters</h2>
{fig("fig-1-13-motor.png", "Figure 1-13. KK-5S motor parameters page")}
{table(
    ["Parameter", "Description", "Unit", "Set", "Default"],
    [
        ["Drive motor rated speed", "From the drive servo nameplate", "rpm", "●", "2000"],
        ["Drive gear diameter", "Pitch-circle diameter of the load-end drive gear", "mm", "●", "127.32"],
        ["Drive reduction ratio", "Drive-shaft reducer ratio from its nameplate", "—", "●", "6"],
        ["Maximum travel of the saw car", "Maximum effective carriage stroke on the rack", "mm", "●", "2700"],
        ["Feed servo rated speed", "From the feed servo nameplate", "rpm", "●", "2000"],
        ["Feed screw pitch", "Nut travel per revolution of the lead screw", "mm", "●", "10"],
        ["Feed reduction ratio", "Feed gearbox ratio; enter 1 if there is no gearbox", "—", "●", "1"],
        ["Feed origin distance", "Retract after feed-home contact (same idea as §1.2.4 / §1.2.5)", "mm", "●", "5"],
        ["Saw motor speed", "Rated speed from the sawing-motor nameplate", "rpm", "●", "1465"],
        ["Sawing reduction ratio", "Saw-shaft gearbox ratio from its nameplate", "—", "●", "9.3"],
        ["Maximum frequency of sawing inverter", "Upper limit of the saw inverter", "Hz", "●", "60"],
    ],
)}
{fig("fig-gear-pitch.png", "Figure 1-3. Gear pitch-circle schematic (diameter d, circular pitch P)")}
      <h3>Measuring maximum saw-carriage travel</h3>
      <ol class="steps">
        <li>Enter the correct drive gear diameter and reduction ratio, then power the machine again.</li>
        <li>Perform Return to Origin.</li>
        <li>After homing, jog the carriage forward until it reaches the front limit switch.</li>
        <li>Read the current saw-carriage position on the main screen. Reduce that value slightly and enter it as maximum travel.</li>
      </ol>

      <h2 id="manual-op">1.2.7 Manual operation screen</h2>
{fig("fig-1-7-manual-op.png", "Figure 1-7. Manual operation screen of the KK-5S cold-cut flying saw")}
      <p>This page duplicates the control-panel actions for drive, feed, cutting, clamp, hydraulic, lubrication, and reset. Status lamps next to each button show enable/home/run state. Use it together with the physical knobs; mode still comes from the panel selector.</p>
"""

FUNCTIONS = f"""
      <div class="kicker">Chapter 2</div>
      <h1>System function description</h1>
      <p class="lede">Modes, power, jogging, homing, clamp/cut, short and long length, length memory, and order scheduling.</p>

      <h2 id="modes">2.1 Operating modes</h2>
      <p>The system has three modes. Rotate the <strong>Operating Mode</strong> knob on the control panel: left = Simulation, center = Manual, right = Automatic.</p>
      <h3>2.1.1 Manual mode</h3>
      <p>Default mode. At power-up, leave the selector in Manual. All station operations can be done by hand: drag-axis jog, feed home, clamp, and sawing. Complete flying-saw preparation in Manual before entering Simulation or Automatic.</p>
      <h3>2.1.2 Simulation mode</h3>
      <p>Offline monitoring. The material encoder is disabled. A virtual axis inside the controller generates production-like motion. You can vary virtual-axis speed to watch carriage behavior and isolate electrical or mechanical faults.</p>
      <h3>2.1.3 Automatic operation mode</h3>
      <p>Online production. The saw follows length and speed from the material encoder and performs fixed-length cutting at the operator-set length while monitoring carriage status.</p>
{fig("fig-startup-flow.png", "Power-up, parameter set, homing, and mode-entry flow (drag home → feed home → check origins → auto or simulation)")}

      <h2 id="power">2.2 Power management</h2>
      <h3>2.2.1 Power supply system</h3>
      <div class="callout danger">
        <strong>Main breaker</strong>
        After the cabinet breaker is closed, the red door lamp stays lit and the cabinet is live. Unqualified personnel must stay away.
      </div>
      <h3>2.2.2 Power system</h3>
      <p>Press the power button on the control panel to turn main power on or off. On starts initialization; the power-button lamp and the door <strong>RUN</strong> lamp both light. Press again to drop main power.</p>
      <h3>2.2.3 Drive system</h3>
      <p>Servo power starts automatically after power-up. Hold Drive, Feed, or Sawing power for <strong>10 seconds</strong> to drop that servo. After the 20-second power-off protection, hold the same button 10 seconds to restore it. During start, lamps flash then go steady (~15 s) when that axis is in operating mode.</p>
      <h3>2.2.4 Enabling / disabling</h3>
      <p>Enable is applied automatically at power-up. A short press (~1 s) on Drive, Feed, or Sawing power disables that servo; another short press re-enables it. In operating mode the lamp is steady. A flashing lamp means powered but not in operating mode — the motor is de-energized and can be turned by hand. After a servo fault, press the power button to reset, then press again to return to operating mode.</p>
      <div class="callout note">
        <strong>Carriage out of mesh</strong>
        If the saw carriage is out of mesh, the drive servo cannot engage gear to rack while enabled. Disable the drive servo, push the carriage into mesh by hand, then re-enable.
      </div>
      <h3>2.2.5 Servo power-off protection</h3>
      <p>Holding Drive, Feed, or Cutting power more than 5 seconds in Manual drops that servo contactor. The axis cannot be powered again until 20 seconds have elapsed, to avoid damage from rapid start/stop cycles. Buttons are ignored during that window.</p>

      <h2 id="jog">2.3 Jog function</h2>
      <h3>2.3.1 Drag jog</h3>
      <p>In Manual, rotate the jog knob to move the saw carriage forward or reverse. At the front or rear limit the carriage stops and the screen reports the limit. Only the opposite direction remains available.</p>
      <div class="callout warn">
        <strong>Home lost</strong>
        After drag-jog, carriage home is lost. Perform Drag to Home again before run mode.
      </div>
      <h3>2.3.2 Feed jog</h3>
      <p>In Manual, rotate the feed jog knob to advance or retract the feed axis. Front/rear feed limits stop the axis and reverse-only motion applies. Feed origin is lost after feed jog — perform Feed Return to Origin before run mode.</p>

      <h2 id="home">2.4 Drag-to-origin / feed-home</h2>
      <p>After every power-up the KK-5S must complete drag-home and feed-home before Simulation or Automatic.</p>
      <h3>2.4.1 Drag-to-home</h3>
      <p>In Manual, press <strong>Drag to Home</strong> on the control panel. The drag-axis servo must be powered and enabled, and the carriage must sit between the limit switches.</p>
      <div class="seq">
        <strong>Sequence</strong>
        <ol>
          <li>Carriage moves toward home and decelerates to a stop on the rear limit.</li>
          <li>When speed is zero it moves forward 50 mm (the configured drag-home distance).</li>
          <li>That position becomes dragged home.</li>
        </ol>
      </div>
      <p>Press Reset on the panel to cancel the move. Home is also lost after manual carriage moves, emergency stop, or fault alarms — home again before run mode.</p>
      <h3>2.4.2 Manual home position dragging</h3>
      <p>On the touchscreen simulation-status (or manual) page, <strong>Drag Manual Home</strong> records the current carriage position as origin without using the limit switch. Use it when the rear limit has failed, or for debug. Place the carriage near the normal drag-home stop. Do not treat this as the standard home.</p>
      <h3>2.4.3 Feed home</h3>
      <p>In Manual, press <strong>Feed Home</strong>. The feed servo drives forward at a set torque percentage until the tooth tips contact the material; that contact is recorded. It affects cut quality and blade life. Mechanics, pneumatics/hydraulics, and clamp must be healthy, and the workpiece must be held.</p>
      <div class="seq">
        <strong>Sequence</strong>
        <ol>
          <li>Fixture clamps the material.</li>
          <li>Feed carriage retracts at low speed to the rear feed limit and stops.</li>
          <li>Feed advances at low speed until the blade contacts the material and stops.</li>
          <li>Feed motor retracts a fixed distance and stops — feed home is complete.</li>
        </ol>
      </div>
      <div class="callout warn">
        <strong>Thin wall and empty fixture</strong>
        Wall thickness under 1 mm can record a bent-wall origin — home on a thicker or solid piece of the same diameter. With no material, step 3 never finishes; press Reset. If the carriage reaches the front limit the system alarms and returns to the rear limit. If the blade never contacts, raise home torque (see §3.4).
      </div>
      <h3>2.4.4 Manual feed home</h3>
      <p><strong>Manual Feed Home</strong> on the simulation-status page stores the current feed position as origin without material or limits. Put the blade close to the material first. Not a standard home; useful when limits fail or no strip is present.</p>

      <h2 id="clamp-cut">2.5 Clamping and 2.6 cutting</h2>
      <p><strong>Clamp:</strong> in Manual, rotate the clamping knob. Use it to prove the mechanism and chase mechanical faults.</p>
      <p><strong>Cut:</strong> in Manual, with the feed axis at origin, press the manual cut button. This is a single static cut for watching the process and the cut face.</p>
      <div class="seq">
        <strong>Manual cut sequence</strong>
        <ol>
          <li>Fixture clamps.</li>
          <li>Saw motor starts; blade rotates.</li>
          <li>After a two-second delay, the feed motor feeds.</li>
          <li>Cut complete; feed returns to start.</li>
          <li>Fixture releases.</li>
          <li>Saw motor stops.</li>
        </ol>
      </div>

      <h2 id="short-long">2.7 Short-length and long-length</h2>
      <p>These functions cut a length other than the setpoint in Simulation or Automatic so scrap or weld-affected strip can be dropped without stopping the mill.</p>
      <h3>2.7.1 Short-length</h3>
      <p>The manual cut button becomes short-length in Simulation/Automatic when simulated or mill speed is ≤ 60% of maximum line speed. After sawing is complete (the function is inactive during the cut, and inactive above 60% speed):</p>
      <ol>
        <li>The system reads carriage direction.</li>
        <li>If going forward: decelerate to stop, return home at high speed, resume production.</li>
        <li>If returning: accelerate to maximum return speed, home, resume production.</li>
      </ol>
      <h3>2.7.2 Long-length</h3>
      <p>The manual clamp knob becomes long-length in Simulation/Automatic. Turn it to clamped to hold, then to unclamped to resume tracking:</p>
      <ol>
        <li>System reads carriage direction.</li>
        <li>Forward: decelerate, high-speed return home, wait.</li>
        <li>Return: accelerate to max return, home, wait.</li>
        <li>Turn the clamp knob to unclamped.</li>
        <li>Carriage resumes tracking and normal production.</li>
      </ol>

      <h2 id="memory">2.7 Length memory function</h2>
      <p>In Automatic, the controller records the current piece length. After a normal exit, power loss, or fault stop, the next entry to Automatic offers a choice to return to the last saved length.</p>
      <p>Press <strong>Yes / Continue</strong> and the carriage moves to the stored position. Encoder counts are ignored during that move — keep the strip still until the carriage arrives, then production continues. Press <strong>No / Restart</strong> (or start the mill) to skip; the window also closes when material length changes.</p>
      <div class="callout warn">
        <strong>Limits</strong>
        If the strip is moved after leaving Automatic or after a blackout, later encoder changes are not captured. Memory stores only the current piece; a very short length at exit is not saved and the next Automatic start goes straight to production.
      </div>

      <h2 id="scheduling">2.8 Order scheduling</h2>
      <p>Ten length schedules plus tube-type recipes cover mixed-length production. Setup is in <a href="operation.html#schedule">§3.9</a>.</p>
"""

OPERATION = f"""
      <div class="kicker">Chapter 3</div>
      <h1>Operating instructions</h1>
      <p class="lede">Field procedures from power-on through automatic production, including torque test, schedules, memory points, and encoder synchronization.</p>

      <h2 id="power-on">3.1 Power-on procedure</h2>
      <ol class="steps">
        <li>With external power connected, close the breaker in the main control cabinet. The front-panel power lamp lights. Press the control-panel power button to start the system. The cabinet power lamp stays on whenever the cabinet is supplied.</li>
        <li>Press the same power button again to shut the system down while it is powered.</li>
        <li>Initialization takes about <strong>60 seconds</strong>. Drive, Feed, and Sawing lamps flash, then go steady when ready. Do not operate before that, or behavior after start can be abnormal.</li>
        <li>If the clamp is hydraulic, start the hydraulic power unit after initialization.</li>
      </ol>

      <h2 id="jog">3.2 Manual forward and reverse feed</h2>
      <p>In Manual, the KK-5S lets you jog the saw carriage and the feed axis from the panel knobs or the Manual Operation page.</p>
      <ul>
        <li><strong>Carriage:</strong> hold the manual feed (drag) knob or hold Manual Feed Forward / Reverse on the HMI. Release to stop. Starts and stops are ramped to protect the motor.</li>
        <li><strong>Feed axis:</strong> hold the feed knob or Feed Forward / Feed Back on the HMI. Release to stop.</li>
      </ul>

      <h2 id="home">3.3 Dragging the feed axis to home</h2>
      <p>Both the drag axis and the feed axis must be at origin before Simulation or Automatic.</p>
      <h3>3.3.1 Dragging to home</h3>
      <p>Home is the position after the carriage finds the rear limit. If that switch is faulty, use manual drag-home.</p>
      <p><strong>Drive home:</strong> press Drive Home on the panel or on the Manual Operation page.</p>
      <div class="seq">
        <strong>Sequence</strong>
        <ol>
          <li>Carriage moves toward origin and decelerates to a stop on the rear limit.</li>
          <li>When speed is zero it moves forward by the configured drag-to-origin distance.</li>
          <li>Current position becomes dragged origin.</li>
        </ol>
      </div>
      <p><strong>Manual home:</strong> press Drag Manual Home on the Manual Operation page. The current position is used as home for later simulation/automatic cycles. Leave enough room for carriage travel.</p>
      <p>Reset stops a home in progress; the carriage stays where it is.</p>
      <h3>3.3.2 Feed home</h3>
      <p>Feed home is the contact point of blade on material. Material must be in the fixture; otherwise use Feed Manual Home.</p>
      <p>Press Feed Home on the panel or HMI.</p>
      <div class="seq">
        <strong>Sequence</strong>
        <ol>
          <li>Fixture clamps.</li>
          <li>Feed retracts to the rear feed limit and stops.</li>
          <li>Feed advances until the blade contacts the workpiece and stops.</li>
          <li>Feed returns to the feed-home offset; that position is feed home.</li>
        </ol>
      </div>
      <div class="callout warn">
        <strong>Thin wall</strong>
        A thin wall can bend during feed-home and record a false origin. Home on the same diameter with a thicker wall or a solid bar.
      </div>

      <h2 id="torque">3.4 Feed torque test</h2>
      <p>After long running, feed-home may need more torque. Run the torque test on the Machine Learning / Manual Parameters page so feed-home still works.</p>
{fig("fig-3-2-torque.png", "Figure 3-2. Feed torque test function")}
      <ol class="steps">
        <li>Press <strong>Feed Torque Test</strong>. When <em>Feed Torque Limit Enabled</em> turns green, press Manual Feed Forward.</li>
        <li>The feed axis moves at the home torque limit. If it hits excess resistance (dry lube circuit, or blade on material) it stops and <em>Feed Torque Limit Reached</em> turns green.</li>
        <li>Press Feed Torque Test again so the enable lamp goes red, jog the blade out of the fixture, load material, and run a normal home.</li>
      </ol>
      <p>Drive-torque for feed-home is typically <strong>1–15%</strong>. If a high value still cannot move the axis, inspect lubrication before raising it again.</p>

      <h2 id="clamp">3.5 Manual clamping</h2>
      <p>Use Manual clamping to test the fixture. Open air for a pneumatic clamp, or start the hydraulic unit for a hydraulic clamp. In Manual, turn the knob to Clamp or Release.</p>
      <ul>
        <li>After clamp, see whether the material still wobbles.</li>
        <li>After one manual cut, push the cut piece inward from both ends of the fixture and snug it. A stepped gap shows angular error in the fixture.</li>
      </ul>

      <h2 id="cut">3.6 Manual cutting</h2>
      <p>Manual mode performs one static cut. Use it for odd lengths and to judge cut quality.</p>
      <p><strong>Before the cut:</strong></p>
      <ol class="steps">
        <li>System is in Manual.</li>
        <li>Hydraulic clamp (if fitted) is on and at pressure.</li>
        <li>Feed axis has been homed and is at home.</li>
        <li>The forming mill will not move in any way. Forward or reverse mill motion during a static cut can destroy the blade.</li>
        <li>Pipe parameters are correct.</li>
        <li>Material is in the fixture.</li>
      </ol>
      <p>Press Manual Cut on the panel or HMI. Sequence is clamp → saw motor on → 2 s delay → feed → return → unclamp → saw motor off. If the fixture does not hold, the cut sounds wrong, or the mill starts, hit emergency stop to protect the blade.</p>

      <h2 id="sim">3.7 Enable simulation</h2>
      <p>Simulation drives the flying saw from a virtual axis with the material encoder off. Vary virtual speed to check carriage motion and to isolate electrical/mechanical faults.</p>
      <p><strong>Prepare:</strong></p>
      <ol class="steps">
        <li>Power-up complete; selector in Manual.</li>
        <li>Absolutely no material in the fixture (including strip from the mill).</li>
        <li>Drive axis homed and at home.</li>
        <li>Feed axis homed or manually homed and in a safe position.</li>
        <li>The forming mill will not move. Mill motion in simulation can overturn the saw carriage.</li>
        <li>Length and tube parameters are correct.</li>
        <li>Set simulation speed.</li>
      </ol>
      <p>Turn the mode selector to Simulation. The blade runs, the virtual axis ticks at the set speed, the carriage tracks, the feed cuts, then the carriage finishes its forward stroke and returns home for the next cycle. Turn the selector to Manual to exit; the carriage finishes the current cut and homes before leaving simulation.</p>

      <h2 id="auto">3.8 Enabling automatic mode</h2>
      <p>Automatic is online production: length and speed come from the material encoder.</p>
      <p><strong>Prepare:</strong></p>
      <ol class="steps">
        <li>Power-up complete; selector in Manual.</li>
        <li>Mill strip is in the clamping fixture.</li>
        <li>Air or hydraulic clamp is on and working.</li>
        <li>Drive axis homed and at home.</li>
        <li>Feed axis homed and at home.</li>
        <li>Length and tube parameters are correct.</li>
      </ol>
      <p>Turn the selector to Automatic. The blade starts, the encoder records strip position, and after the mill starts the carriage tracks, the feed cuts, the carriage finishes forward travel, then returns home for the next piece.</p>
      <div class="callout note">
        <strong>Exit</strong>
        First decelerate and stop the upstream mill. When the mill is still, turn the selector to Manual. The system stores carriage and material positions (see §3.10) and creeps to origin. Automatic ends when origin is reached.
      </div>

      <h2 id="schedule">3.9 Setting up production schedules</h2>
      <p>Length is set through ten built-in schedules. Each schedule has a length, a quantity, and an enable.</p>
{fig("fig-3-3-schedule.png", "Figure 3-3. Length batch / order settings (Order 1 selected and in process)")}
      <p>In automatic production the system runs enabled orders in ascending number. A lit <em>In Production</em> lamp marks the active order; a light-green background marks completed orders. Buttons above the list:</p>
      <ul>
        <li><strong>Calculate</strong> — computes maximum feasible mill speed from cutting time and the selected order’s length. Results appear on the main, tube-parameter, and simulation pages. In run mode this also lets you trim the current length without stopping.</li>
        <li><strong>Next Order</strong> — in Automatic or Simulation, jump to the next enabled order without stopping or changing the setpoint quantity.</li>
        <li><strong>Clear Production Quantity</strong> — zeroes pieces already produced.</li>
        <li><strong>Clear Completed Orders</strong> — Manual only; clears finished orders.</li>
      </ul>
      <div class="callout warn">
        <strong>Zero length / zero quantity</strong>
        Selected order length cannot be 0 — Calculate raises warning <em>[38] Warning: The set length of the selected order is 0</em>. Quantity 0 means unlimited production of that order; the controller does not check a target count.
      </div>

      <h2 id="memory">3.10 Memory points</h2>
      <p>In Automatic the controller records current piece length. After a normal exit, blackout, or fault, re-entering Automatic offers resume from the last stop or from home.</p>
{fig("fig-3-4-memory.png", "Figure 3-4. Return to memory point — Continue from MEMORY or Restart from HOME")}
      <div class="callout danger">
        <strong>Do not move the strip</strong>
        If the material is moved after leaving Automatic or after a power cut, the memory point is wrong and the next piece can be too long.
      </div>
      <p>Press <strong>Continue</strong>: the carriage creeps to the position saved at the last Automatic exit. Encoder counts are ignored until it arrives — keep strip position unchanged. Then start the mill. Press <strong>Restart</strong> (or start the mill) to skip; the popup closes when material length changes.</p>

      <h2 id="short-long">3.11 Short and long pieces</h2>
      <p>Cut a non-setpoint length in Simulation or Automatic to dump scrap or weld zones.</p>
      <h3>3.11.1 Short-length</h3>
      <p>Requirements: Simulation or Automatic; speed ≤ 60% of maximum line speed; press Manual Cut. Then:</p>
      <ol>
        <li>Controller reads carriage direction.</li>
        <li>Forward: decelerate, high-speed home, resume production.</li>
        <li>Return: accelerate to max return, home, resume production.</li>
      </ol>
      <h3>3.11.2 Long-length</h3>
      <p>Turn the manual clamp knob to clamped in Simulation or Automatic. Then:</p>
      <ol>
        <li>Controller reads carriage direction.</li>
        <li>Forward: decelerate, high-speed home, wait.</li>
        <li>Return: accelerate to max return, home, wait.</li>
        <li>Turn the knob to released.</li>
        <li>Carriage resumes tracking.</li>
      </ol>

      <h2 id="sync">3.12 Synchronization measurement</h2>
      <p>Carriage-to-strip sync is required for length accuracy and blade life. Wear after commissioning can desynchronize the two. Recheck periodically and correct with <strong>Material Speed Sensor Wheel Diameter</strong>.</p>
{fig("fig-3-5-sync.png", "Figure 3-5. Synchronization parameters (tube encoder wheel diameter and related fields)")}
      <ol class="steps">
        <li>Measure the speed-wheel diameter with a caliper and enter it as Material Speed Measurement Wheel Diameter (initial reference).</li>
        <li>Run a short length of material through the clamp, stop, and perform Feed to Home.</li>
        <li>Press Manual Cut. After the cut, current material length resets to zero.</li>
        <li>Start the mill and let about 2 m of strip travel.</li>
        <li>Press <strong>Material Cut</strong> on the HMI so it turns green — current material length will not reset after the next cut.</li>
        <li>Press Manual Cut again.</li>
        <li>Tape-measure the actual cut length. Enter it as Actual Material Length, and enter current blade thickness.</li>
        <li>Press <strong>Data Calculation</strong>. Wheel diameter is recomputed from the test.</li>
        <li>Repeat steps 4–7 until actual length plus blade thickness equals the displayed current material length.</li>
      </ol>
"""

PAGES = [
    ("index.html", "KK-5S Cold-Cut Flying Saw", "Aogang Machinery / KK-5S / Cover", INDEX),
    ("safety.html", "Safety precautions", "Manual / Safety precautions", SAFETY),
    ("parameters.html", "Chapter 1 · Parameter description", "Manual / Chapter 1 · Parameters", PARAMS),
    ("functions.html", "Chapter 2 · System functions", "Manual / Chapter 2 · Functions", FUNCTIONS),
    ("operation.html", "Chapter 3 · Operating instructions", "Manual / Chapter 3 · Operation", OPERATION),
]


def main():
    for name, title, crumb, body in PAGES:
        (OUT / name).write_text(page(name, title, crumb, body), encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
