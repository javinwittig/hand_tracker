<div align="center">
<h1>Project: Hand Tracker</h1>

<div align="center">
<h2>Overview</h2>
  <div align="left">

<p>This repository contains a real-time hand-tracking system. A camera is mounted on a Raspberry Pi to stream video to a PC, which uses MediaPipe to track the position of a hand and sends target coordinates back to the Pi. The Pi then drives two servo motors to mimic the tracked hand's movement — for example, if the hand bends forward, the servo-driven mechanism bends forward too.</p>

<p>The workload is split between the two devices by design: the Pi handles video capture, streaming, and servo control, while the computationally intensive hand-tracking runs on a PC with a dedicated GPU. This keeps the Pi's load low and allows the tracking loop to run fast enough for real-time use.</p>
<div align="center">
<h1>My Project Website</h1>
    <div align="left">

<p>You can explore my project website via this link: <a href="https://javinwittig.github.io/hand_tracker_website/">https://javinwittig.github.io/hand_tracker_website/</a></p>

<p>This link leads to my GitHub repository where I built the website mentioned above: <a href="https://github.com/javinwittig/hand_tracker_website">https://github.com/javinwittig/hand_tracker_website</a></p>

<p>This link leads to the server / tracking backend repository: <a href="https://github.com/javinwittig/hantracking_server">https://github.com/javinwittig/hantracking_server</a></p>


<div align="center">
<h2>Features</h2>
  <div align="left">

<p>
<b>Real-time hand tracking</b> using MediaPipe's HandLandmarker (Tasks API, <code>LIVE_STREAM</code> mode).<br>
<b>Video streaming</b> from the Raspberry Pi to a PC over the network.<br>
<b>Servo control</b> that mimics the tracked hand movement on two axes.<br>
<b>Live preview</b> via a local Flask website with an MJPEG stream, viewable from any browser on the network.<br>
<b>GPU-accelerated tracking</b>, offloaded to a PC with an RTX 5070 instead of running on the Pi.
</p>

<div align="center">
<h2>Approach</h2>
  <div align="left">

<p>My Workflow:</p>

<p>
<b>1. Camera Pipeline:</b> Capturing video on the Raspberry Pi using <code>rpicam-vid</code> (YUV420, 640x480, 180° rotation).<br>
<b>2. Video Streaming:</b> Streaming the camera feed from the Pi to a PC for processing.<br>
<b>3. Hand Tracking:</b> Running MediaPipe HandLandmarker (Tasks API, <code>LIVE_STREAM</code> mode) on the PC to detect hand positions in real time.<br>
<b>4. Coordinate Transmission:</b> Sending the calculated target coordinates from the PC back to the Pi.<br>
<b>5. Servo Control:</b> Using the coordinates on the Pi to drive two servo motors that mimic the tracked hand's movement.<br>
<b>6. Live Preview:</b> Hosting a local website with an MJPEG live video stream via Flask.
</p>

<div align="center">
<h2>Hardware</h2>
  <div align="left">

<p>Raspberry Pi 4 (4GB), 2x servo motor, camera module and a PC with an RTX 5070 for MediaPipe processing.</p>



<div align="center">
<h2>Getting Started</h2>
  <div align="left">

<p><b>Requirements:</b></p>

<p>
Raspberry Pi 4 (4GB or more) with camera module and <code>rpicam-vid</code>.<br>
Two servo motors wired to the Pi's GPIO pins.<br>
A PC with a CUDA-capable GPU for MediaPipe inference (see the <a href="https://github.com/javinwittig/hantracking_server">tracking backend repository</a>).<br>
Python 3 on both devices.
</p>

<p><b>Installation:</b></p>

<pre><code>git clone https://github.com/javinwittig/hand_tracker.git
cd hand_tracker
pip install -r requirements.txt</code></pre>

<p><b>Usage:</b></p>

<p>
1. Set up and run the <a href="https://github.com/javinwittig/hantracking_server">tracking backend</a> on the PC.<br>
2. Run <code>main.py</code> on the Raspberry Pi to start the camera pipeline and streaming.<br>
3. <code>servo.py</code> drives the servos to mimic the hand movement as tracking data arrives.<br>
4. Open the local Flask website in a browser to view the live preview.
</p>



<h3>Ai Usage</h3>

AI Declaration: Claude for some coding and research and OpenCode

</div>
