# webcam-eyekeyboard
Extending webcam-eyetracker for use a keyboard with pupils

## Purpose

A family friend suffered a cerebral vascular accident which paralyzed her body movements. She can communicate through a table given to her at the hospital as shown below:

[![Before](http://img.youtube.com/vi/euZO5IGGJ_0/0.jpg)](https://www.youtube.com/watch?v=euZO5IGGJ_0)

An assistant read the numbers of the rows and my family friend moves her eyes up (yes) or down (no) to signalize her row choice. Then they move to the letters, where the assistant read letter by letter until reach the desired letter. They repeat this process until complete the desired word and move forward to next one. 

The idea of this software was to automate the assistant task. It relies on [webcam-eyetracker](https://github.com/esdalmaijer/webcam-eyetracker) an open source project that a calibrates a webcam to track the eye moviments. **webcam-eyekeyboard** use this calibrated webcam to enable users to type in a keyboard with their eyes.

## Example

I've recorded a video to ilustrate how it works:

[![Example](http://img.youtube.com/vi/vG-_wg6IxnY/0.jpg)](https://youtu.be/vG-_wg6IxnY)

## Preliminar Test

We've made a first test with my family friend last week and the mechanism worked very well as shown below:

[![InitialTest](http://img.youtube.com/vi/GCCLfgFJNNU/0.jpg)](https://www.youtube.com/watch?v=GCCLfgFJNNU)

## Next Steps

- [ ] Change the keyboard layout to the same format that she uses today
- [ ] Build a predicting model to complete the words based on the vocabulary and her notebooks
- [ ] Change the duration of some timeintervals to be more confortable
- [ ] Test some text to speech APIs (e.g. http://www.oddcast.com/ - Raquel)
- [ ] Add some userful commands (bell, read, delete one, delete all, turn off)
- [ ] Add punctuation symbols (end of sentend, space and question mark)
