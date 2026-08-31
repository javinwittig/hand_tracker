<div align="center">
<h1>Project: Hand Tracker</h1>
<h2>Overview</h2>
<p>This repository contains the implementation of a real-time hand-tracking laser turret. A camera mounted on a Raspberry Pi streams video to a PC, which uses MediaPipe to track the position of a hand and sends target coordinates back to the Pi, which then steers two servo motors to aim a laser pointer at the tracked hand.</p>
<h2>Approach</h2>
<p>To build a responsive, low-latency tracking system, the following steps were taken:</p>
<p>
  <b>1. Camera Pipeline:</b> Capturing video on the Raspberry Pi using rpicam-vid (YUV420, 640x480, 180° rotation).<br>
  <b>2. Video Streaming:</b> Streaming the camera feed from the Pi to a PC for processing.<br>
  <b>3. Hand Tracking:</b> Running MediaPipe HandLandmarker (Tasks API, LIVE_STREAM mode) on the PC to detect hand position in real time.<br>
  <b>4. Coordinate Transmission:</b> Sending the calculated target coordinates from the PC back to the Pi.<br>
  <b>5. Servo Control:</b> Using the coordinates on the Pi to drive two servo motors, aiming the laser pointer at the tracked hand.<br>
  <b>6. Live Preview:</b> Hosting a local website with an MJPEG live video stream via Flask.
</p>
<h2>Hardware</h2>
<p>Raspberry Pi 4 (4GB), 2x servo motor (pan/tilt), laser pointer, camera module, and a PC with an RTX 5070 for offloaded MediaPipe processing.</p>
<h1>My Project Website</h1>
<p>You can explore my project website via this link: <a href="https://javinwittig.github.io/hand_tracker_website/">https://javinwittig.github.io/hand_tracker_website/</a></p>
<p>This link leads to my GitHub repository where I built the website mentioned above: <a href="https://github.com/javinwittig/hand_tracker_website">https://github.com/javinwittig/hand_tracker_website</a></p>
<p>This link leads to the server / tracking backend repository: <a href="https://github.com/javinwittig/hantracking_server">https://github.com/javinwittig/hantracking_server</a></p>
<h2>Contributors</h2>
<p>Javin Wittig</p>
</div>
<div align="center">
<h3>Ai Usage</h3>
AI Declaration: Claude for some coding and OpenCode
</div>
