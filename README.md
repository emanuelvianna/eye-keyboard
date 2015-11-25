# eye-keyboard
Extending webcam-eyetracker for use a keyboard with pupils

## Purpose

A family friend suffered a cerebral vascular accident which paralyzed her body movements. She can communicate through a table given to her at the hospital like this:

| **1** | **A** | **B** | **C** | **D** | **E** | **F** | **G** | **H** | **I** |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **2** | **J** | **K** | **L** | **M** | **N** | **O** | **P** | **Q** | **R** |
| **3** | **S** | **T** | **U** | **V** | **X** | **W** | **Y** | **Z** |       |

An assistant read the numbers of the rows and my family friend moves her eyes up (yes) or down (no) to signalize her row choice. Then they move to the letters, where the assistant read letter by letter until reach the desired letter. They repeat this process until complete the desired word and move forward to next one. 

The idea of this software was to automate the assistant task. It relies on [webcam-eyetracker](https://github.com/esdalmaijer/webcam-eyetracker) an open source project that a calibrates a webcam to track the eye moviments. **eye-keyboard** use this calibrated webcam to enable users to type in a keyboard with their eyes.

I've recorded a video to ilustrate how it works:

[![Example](http://img.youtube.com/vi/vG-_wg6IxnY/0.jpg)](https://youtu.be/vG-_wg6IxnY)
