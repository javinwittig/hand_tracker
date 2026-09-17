# Hand Tracker
### overview:

I made a project which tracks my hand in real time and mimics my hand movement onto a hand placed on to two servo motors, which are controlled by a rasperry pi 

## My Project website and other important repos

You can explore my project website via this link:https://javinwittig.github.io/hand_tracker_website/

This link leads to my GitHub repository where 1 built the website mentioned above: [https://github.com/javinwittig/hand.tracker.website](https://github.com/javinwittig/hand_tracker_website)

This link leads to the repo where I have the backend of the project: https://github.com/javinwittig/hantracking_serve

## Features

The rasperry Pi tracks my hand and sends the stream to my PC, which uses Mediapipe to track the postion of the hand. After that, it sends back the target coordinates to the Pi which then drives the two servo motors to mimic the tracked hand's movement

## Workflow

1. Capturing the video on the Raspberry Pi#

2. Stream the video to your backend, in my case my Pc

3. Using Mediapipe to track the hand#s position

4. Sending the calculated target coordinates from the PC back to the Pi

5. Using the coordinates on the Pi to drive two servo motors that mimic the tracked hand's movement.

6. Hosting a local website which then streams the video off the tracked hand


## Hardware

Rasperry Pi 4 (4GB), 2x servo motors, a camera module and a PC which can handle Mediapipe


