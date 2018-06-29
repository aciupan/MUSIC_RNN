# MUSIC_RNN
Composing music with RNNs

This project trains a recurrent neural network on a dataset of [folk tunes in MIDI format](https://github.com/jukedeck/nottingham-dataset) and composes new music.

A writeup, and examples, are available [here](https://aciupan.github.io/projects#rnn).

I produce two models, each in a different folder. polytrack is the more complex one. monotrack is the one described in section 8 of the writeup.

The code is structured as follows:

1) constants.py defines constants and precomputes the dictionary which is computed in processdata.py (see below)
2) functions.py defines (a lot of) functions which we need in this project: from data inspection and processing to encoding and decoding MIDI songs
3) processdata.py processed the input data and creates the relevant dictionary. It is precomputed, for speed. You can just uncomment the parts of the code where the computation is done in order to do the whole thing from scratch.
4) composition.py trains the RNN on the processed data and provides the function used for music composition. The output of the specific composition function is a MIDI song.
