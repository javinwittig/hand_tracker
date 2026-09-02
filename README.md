<div align="center">
<h1>Project: Hand Tracker</h1>
<div align="center">
<h2>Overview</h2>
  <div align="left">
<p>This repository contains a real-time hand-tracking system. A camera is mounted on a Raspberry Pi to stream video to a PC, which uses MediaPipe to track the position of a hand and sends target coordinates back to the Pi. The Pi then controls two servo motors to mimic my hand movement.</p>
<div align="center">
  <h2>Approach</h2>
    <div align="left">
<p>My Workflow:</p>
<p>
 <p>
  <b>1. Camera Pipeline:</b> Capturing video on the Raspberry Pi using <code>rpicam-vid</code> (YUV420, 640x480, 180° rotation).<br>
  <b>2. Video Streaming:</b> Streaming the camera feed from the Pi to a PC for processing.<br>
  <b>3. Hand Tracking:</b> Running MediaPipe HandLandmarker (Tasks API, <code>LIVE_STREAM</code> mode) on the PC to detect hand positions in real time.<br>
  <b>4. Coordinate Transmission:</b> Sending the calculated target coordinates from the PC back to the Pi.<br>
  <b>5. Servo Control:</b> Using the coordinates on the Pi to drive two servo motors who mimic my tracked hand.<br>
  <b>6. Live Preview:</b> Hosting a local website with an MJPEG live video stream via Flask.

</p>
<div align="center">
<h2>Hardware</h2>
    <div align="left">
<p>Raspberry Pi 4 (4GB), 2x servo motor (pan/tilt), camera module and a PC with an RTX 5070 for MediaPipe processing.</p>
<div align="center">
<h1>My Project Website</h1>
      <div align="left">
<p>You can explore my project website via this link: <a href="https://javinwittig.github.io/hand_tracker_website/">https://javinwittig.github.io/hand_tracker_website/</a></p>
<p>This link leads to my GitHub repository where I built the website mentioned above: <a href="https://github.com/javinwittig/hand_tracker_website">https://github.com/javinwittig/hand_tracker_website</a></p>
<p>This link leads to the server / tracking backend repository: <a href="https://github.com/javinwittig/hantracking_server">https://github.com/javinwittig/hantracking_server</a></p>

<h3>Ai Usage</h3>
AI Declaration: Claude for some coding and research and OpenCode
</div>
