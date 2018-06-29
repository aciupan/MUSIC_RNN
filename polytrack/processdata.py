from mido import MidiFile, Message, MidiTrack
import os
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
from constants import MELODY_DIR, CHORDS_DIR, DATA_X_NAME, DATA_Y_NAME,\
SEGMENT_SIZE, VELOCITY, TIMESTEP, CONTINUATION_CHORD
from functions import write_content_to_txt, total_time_duration, get_note,\
song_duration_difference, chord_seq_valid, song_numevents, song_to_chorddurlist,\
song_validchords, lastpos_in_chordlist,\
song_check, chorddurlists_to_soundlist, soundlist_split,\
dictionary_from_notes_chords, addtrack_to_midi, soundlist_to_midi,\
encoded_track_to_track_soundlist, encoded_sound_to_soundlist,\
monosoundlist_to_eventlist, soundlist_to_eventlist, soundlist_to_segmentlist,\
tuple_to_twohot, tuplesegment_to_twohotsegment,\
tuplesegmentlist_to_twohotsegmentlist, inputdata_to_xydata

# constants
ALLSONGNAMES            = set(os.listdir(MELODY_DIR)) & \
set(os.listdir(CHORDS_DIR))
DIFF_THRESH             = 4096
CHORDFREQ_THRESH        = 0.0001
NOTEFREQ_THRESH         = 0.0001
DUR_THRESH              = 2048

# Calculate differences in total duration between the melody 
# and the chord of a song
# Store these values
#diff_dictionary = {}
#num_songs       = 0
#coverage        = 0
#for f in ALLSONGNAMES:
#    num_songs +=1
#    diff = song_duration_difference(f, CHORDS_DIR, MELODY_DIR)
#    #print(diff)
#    if diff not in diff_dictionary:
#        diff_dictionary[diff] = 0
#    diff_dictionary[diff] +=1
##print(diff_dictionary)
#
##Calculate frequencies
#for k,v in diff_dictionary.items():
#    freq = int(v) * 1.0 / num_songs
#    if abs(k) < DIFF_THRESH:
#        #print(abs(k), freq)
#        coverage+= freq
#print(coverage)

# Keep songs with valid difference
#set_to_remove = set()
#for f in ALLSONGNAMES:
#    diff = song_duration_difference(f, CHORDS_DIR, MELODY_DIR)
#    if abs(diff) >= DIFF_THRESH:
#        set_to_remove.add(f)
#print(set_to_remove)

set_to_remove = {'jigs22.mid', 'morris20.mid', 'reelsh-l54.mid', 'jigs223.mid',\
 'jigs111.mid', 'reelsa-c44.mid', 'reelsr-t48.mid'}

ALLSONGNAMES = ALLSONGNAMES - set_to_remove

# Check every song has a valid successtion of note_on, note_off
# for every note event
#for f in ALLSONGNAMES:
#    a = chord_seq_valid(MELODY_DIR + '/' + f)
#    b = chord_seq_valid(CHORDS_DIR + '/' + f)
#    if a + b <2:
#        print(f, a, b)
#        print("ERROR")
#        quit()
# all songs have a valid succession note_on, note_off


# Get chord frequencies
chord_dictionary    = {}
set_chords          = set()
num_events          = 0
coverage            = 0

#Create the set of chords and a dictionary of chords and their frequencies
#for f in ALLSONGNAMES:
#    #f = 'ashover1.mid'
#    a = song_to_chordlist(CHORDS_DIR + '/' + f)
#    for chord in a:
#        #print(chord)
#        num_events += 1
#        if chord not in chord_dictionary:
#            set_chords.add(chord)
#            chord_dictionary[chord] = 0
#        chord_dictionary[chord] +=1
#print(num_events)
#print(chord_dictionary)
#print(set_chords)

num_events = 49982
chord_dictionary = {frozenset(): 834, frozenset({50, 43, 47}): 10342,\
frozenset({48, 42, 45, 38}): 3552,\
frozenset({48, 52, 45}): 2408, frozenset({40, 43, 36}): 3594,\
frozenset({49, 52, 45}): 4466, \
frozenset({40, 50, 44, 47}): 1629, frozenset({42, 45, 38}): 9829,\
frozenset({49, 42, 45}): 218,\
frozenset({50, 54, 47}): 1137, frozenset({40, 44, 47}): 560,\
frozenset({40, 43, 47}): 2881, frozenset({49, 52, 45, 55}): 3808,\
frozenset({57, 51, 54, 47}): 296, frozenset({48, 41, 45}): 1094,\
frozenset({50, 53, 46}): 501, frozenset({40, 43, 36, 46}): 308,\
frozenset({50, 43, 46}): 665, frozenset({51, 54, 47}): 33,\
frozenset({50, 43, 53, 47}): 506, frozenset({41, 45, 38}): 588,\
frozenset({49, 42, 52, 46}): 79, frozenset({48, 41, 51, 45}): 150,\
frozenset({40, 43, 37}): 3, frozenset({49, 43, 46}): 16,\
frozenset({43, 36, 39}): 205, frozenset({43, 46, 39}): 128,\
frozenset({57, 50, 54, 47}): 4,frozenset({48, 51, 44}): 1,\
frozenset({49, 52, 46}): 1, frozenset({40, 44, 37}): 22,\
frozenset({42, 36, 39}): 15, frozenset({40, 50, 43, 47}): 9,\
frozenset({50, 44, 47}): 1, frozenset({40, 43, 46}): 8,\
frozenset({56, 50, 53, 46}): 3, frozenset({42, 45, 39}): 7,\
frozenset({48, 41, 44}): 8, frozenset({41, 45, 38, 47}): 4,\
frozenset({38, 42, 45, 48, 51}): 2, frozenset({40, 44, 47, 50, 53}): 4,\
frozenset({46, 42, 38}): 2, frozenset({50, 43, 52, 47}): 6,\
frozenset({43, 36, 45, 39}): 2, frozenset({41, 51, 45, 49}): 2,\
frozenset({49, 42, 46}): 15, frozenset({40, 43, 36, 45}): 6,\
frozenset({48, 51, 45}): 7, frozenset({42, 45, 38, 47}): 3,\
frozenset({41, 44, 37}): 2, frozenset({41, 44, 37, 47}): 2,\
frozenset({48, 41, 45, 38}): 2, frozenset({48, 40, 44}): 1,\
frozenset({48, 52, 45, 55}): 8, frozenset({41, 44, 38}): 2,\
frozenset({48, 51, 44, 54}): 2, frozenset({41, 44, 47}): 1}

set_chords = {frozenset({41, 44, 37}), frozenset({50, 43, 52, 47}),\
frozenset({49, 52, 45, 55}), frozenset({49, 52, 46}),\
frozenset({38, 42, 45, 48, 51}), frozenset({41, 44, 37, 47}),\
frozenset({49, 42, 46}), frozenset({48, 41, 45, 38}),\
frozenset({41, 44, 38}), frozenset(), frozenset({48, 51, 44, 54}),\
frozenset({49, 42, 45}), frozenset({40, 50, 43, 47}),\
frozenset({42, 45, 38, 47}), frozenset({50, 43, 53, 47}),\
frozenset({40, 43, 36, 46}), frozenset({48, 41, 44}),\
frozenset({50, 43, 47}), frozenset({50, 54, 47}), frozenset({43, 36, 39}),\
frozenset({43, 36, 45, 39}), frozenset({43, 46, 39}), frozenset({50, 43, 46}),\
frozenset({48, 40, 44}), frozenset({48, 52, 45, 55}),\
frozenset({40, 44, 47, 50, 53}), frozenset({48, 51, 44}),\
frozenset({46, 42, 38}), frozenset({41, 45, 38, 47}),\
frozenset({42, 36, 39}), frozenset({40, 43, 36}), frozenset({48, 41, 51, 45}),\
frozenset({48, 42, 45, 38}), frozenset({49, 42, 52, 46}),\
frozenset({40, 44, 37}), frozenset({40, 43, 46}), frozenset({41, 44, 47}),\
frozenset({51, 54, 47}), frozenset({48, 51, 45}), frozenset({40, 43, 47}),\
frozenset({56, 50, 53, 46}), frozenset({42, 45, 39}), frozenset({49, 52, 45}),\
frozenset({48, 52, 45}), frozenset({40, 43, 36, 45}),\
frozenset({40, 50, 44, 47}), frozenset({40, 44, 47}),frozenset({50, 53, 46}),\
frozenset({40, 43, 37}), frozenset({57, 51, 54, 47}), frozenset({48, 41, 45}),\
frozenset({42, 45, 38}), frozenset({41, 51, 45, 49}), frozenset({49, 43, 46}),\
frozenset({50, 44, 47}),frozenset({41, 45, 38}), frozenset({57, 50, 54, 47})}

#Calculate frequencies and remove infrequent chords
#for k,v in chord_dictionary.items():
#    freq = int(v) * 1.0 / num_events
#    if freq > CHORDFREQ_THRESH:
#        #print(k, freq)
#        coverage+= freq
#    else:
#        set_chords.remove(k)
#print(coverage)
#print(set_chords)

set_chords = {frozenset({50, 43, 52, 47}), frozenset({49, 52, 45, 55}),\
frozenset({49, 42, 46}), frozenset(),frozenset({49, 42, 45}),\
frozenset({40, 50, 43, 47}), frozenset({50, 43, 53, 47}),\
frozenset({40, 43, 36, 46}),frozenset({50, 43, 47}), frozenset({50, 54, 47}),\
frozenset({43, 36, 39}), frozenset({43, 46, 39}),frozenset({50, 43, 46}),\
frozenset({48, 52, 45, 55}), frozenset({42, 36, 39}), frozenset({40, 43, 36}),\
frozenset({48, 41, 51, 45}), frozenset({48, 42, 45, 38}),\
frozenset({49, 42, 52, 46}), frozenset({40, 44, 37}),frozenset({40, 43, 46}),\
frozenset({51, 54, 47}), frozenset({48, 51, 45}), frozenset({40, 43, 47}),\
frozenset({42, 45, 39}), frozenset({49, 52, 45}), frozenset({48, 52, 45}),\
frozenset({40, 43, 36, 45}), frozenset({40, 50, 44, 47}),\
frozenset({40, 44, 47}), frozenset({50, 53, 46}), frozenset({57, 51, 54, 47}),\
frozenset({48, 41, 45}), frozenset({42, 45, 38}), frozenset({49, 43, 46}),\
frozenset({48, 41, 44}), frozenset({41, 45, 38})}

#Do the same for melody: create the dictionary of notes playing.
# It's possible that more than one note is playing at the same time.

#set_melody           = set()
#notes_dictionary    = {}
#num_events          = 0
#for f in ALLSONGNAMES:
#    #f = 'ashover1.mid'
#    a = song_to_chordlist(MELODY_DIR + '/' + f)
#    for note in a:
#        num_events += 1
#        if note not in notes_dictionary:
#            set_melody.add(note)
#            notes_dictionary[note] = 0
#        notes_dictionary[note] +=1
#print(num_events)
#print(notes_dictionary)
#print(set_melody)

num_events          = 192117
notes_dictionary    = {frozenset(): 1936, frozenset({73}): 9877,\
frozenset({76}): 19970, frozenset({71}): 22803,\
frozenset({69}): 25576, frozenset({78}): 12836, frozenset({81}): 6437,\
frozenset({74}): 26872, frozenset({64}): 6163,frozenset({62}): 5078,\
frozenset({61}): 310, frozenset({66}): 7728, frozenset({79}): 10101,\
frozenset({83}): 1588, frozenset({72}): 10378, frozenset({77}): 1665,\
frozenset({75}): 559, frozenset({67}): 15226, frozenset({70}): 1813,\
frozenset({67, 71}): 70, frozenset({74, 71}): 26, frozenset({65}): 1288,\
frozenset({63}): 100, frozenset({60}): 391, frozenset({68}): 935,\
frozenset({80}): 926, frozenset({57}): 169,frozenset({59}): 278, \
frozenset({82}): 192, frozenset({84}): 134, frozenset({79, 71}): 14,\
frozenset({74, 78}): 12, frozenset({74, 79}): 2, frozenset({55}): 34,\
frozenset({72, 76}): 40, frozenset({72, 79}): 6, frozenset({72, 81}): 21,\
frozenset({72, 65}): 3, frozenset({65, 74}): 5,frozenset({65, 69}): 16,\
frozenset({74, 77}): 38, frozenset({64, 69}): 4, frozenset({58}): 12,\
frozenset({85}): 8, frozenset({66, 74, 69, 78}): 1, frozenset({86}): 20,\
frozenset({64, 60}): 40, frozenset({65, 62}): 12, frozenset({64, 67}): 12,\
frozenset({72, 69}): 54, frozenset({76, 79}): 22, frozenset({81, 77}): 6,\
frozenset({68, 76}): 2, frozenset({69, 77}): 9,frozenset({64, 72}): 9,\
frozenset({62, 71}): 5, frozenset({60, 69}): 4, frozenset({67, 60, 69}): 1,\
frozenset({67, 76}): 1, frozenset({67, 59}): 2, frozenset({65, 57}): 1,\
frozenset({64, 55}): 1, frozenset({62, 55}): 2, frozenset({73, 76}): 18,\
frozenset({76, 71}): 6, frozenset({64, 61}): 8, frozenset({64, 59}): 3,\
frozenset({64, 57}): 3, frozenset({66, 69}): 6, frozenset({66, 69, 74}): 10,\
frozenset({73, 67, 69}): 24, frozenset({66, 69, 71}): 12,\
frozenset({70, 79}): 12, frozenset({77, 70}): 4, frozenset({76, 70}): 6,\
frozenset({74, 70}): 24, frozenset({69, 79}): 4, frozenset({72, 70}): 10,\
frozenset({81, 73}): 26, frozenset({67, 70}): 20, frozenset({72, 75}): 18,\
frozenset({75, 79}): 6, frozenset({72, 77}): 4, frozenset({72, 88}): 2,\
frozenset({72, 78}): 8, frozenset({73, 69}): 5, frozenset({81, 71}): 6,\
frozenset({83, 71}): 3, frozenset({73, 77}): 6, frozenset({88}): 2,\
frozenset({64, 66}): 1, frozenset({56}): 8, frozenset({69, 62}): 4,\
frozenset({68, 71}): 2, frozenset({69, 71}): 2}
set_melody = {frozenset({69, 71}), frozenset({84}), frozenset({77}),\
frozenset({73, 67, 69}), frozenset({78}), frozenset({64, 60}),\
frozenset({66, 74, 69, 78}), frozenset({76, 71}), frozenset({67, 59}),\
frozenset({70}), frozenset({64, 69}), frozenset({72, 88}),frozenset({73, 69}),\
frozenset({58}), frozenset({88}), frozenset({66, 69, 74}), frozenset({72, 76}),\
frozenset({83, 71}),frozenset({80}), frozenset({64, 72}), frozenset({65, 57}),\
frozenset({64, 67}), frozenset({73}), frozenset({81, 77}), frozenset({64}),\
frozenset({65, 62}), frozenset({81, 73}), frozenset({72, 81}), frozenset({66}),\
frozenset({69, 62}), frozenset({66, 69, 71}),frozenset({69, 77}),\
frozenset({65, 69}), frozenset({74, 79}), frozenset({59}), frozenset({81, 71}),\
frozenset({64, 59}), frozenset({69, 79}), frozenset({73, 76}),\
frozenset({72, 78}), frozenset({76, 79}), frozenset({60}), frozenset({85}),\
frozenset({64, 61}), frozenset({86}), frozenset({61}), frozenset({62}),\
frozenset({69}), frozenset({55}), frozenset({62, 55}), frozenset({60, 69}),\
frozenset({67, 71}), frozenset({74, 77}), frozenset({79, 71}),\
frozenset({67, 70}), frozenset({75}), frozenset({68}), frozenset({63}),\
frozenset({67, 60, 69}), frozenset({56}), frozenset({74, 70}), frozenset({81}),\
frozenset({67, 76}), frozenset({82}), frozenset({57}), frozenset({64, 66}),\
frozenset({65}), frozenset({76}), frozenset({76, 70}), frozenset({72, 75}),\
frozenset({77, 70}), frozenset({71}), frozenset({70, 79}), frozenset({74}),\
frozenset({65, 74}), frozenset({72, 70}), frozenset({79}), frozenset({73, 77}),\
frozenset(), frozenset({72}), frozenset({68, 71}), frozenset({72, 79}),\
frozenset({75, 79}), frozenset({66, 69}), frozenset({64, 55}), \
frozenset({62, 71}), frozenset({74, 78}), frozenset({72, 69}), frozenset({83}),\
frozenset({68, 76}), frozenset({67}), frozenset({74, 71}),\
frozenset({72, 65}), frozenset({64, 57}), frozenset({72, 77})}

#Calculate frequencies and remove infrequent notes
#coverage            = 0
#for k,v in notes_dictionary.items():
#    freq = int(v) * 1.0 / num_events
#    if freq > NOTEFREQ_THRESH:
#        print(k, freq)
#        coverage+= freq
#    else:
#        set_melody.remove(k)
#print(coverage)
#print(set_melody)

set_melody = {frozenset({84}), frozenset({77}), frozenset({73, 67, 69}),\
frozenset({78}), frozenset({64, 60}),frozenset({70}), frozenset({72, 76}),\
frozenset({80}), frozenset({73}), frozenset({64}), frozenset({73, 81}),\
frozenset({72, 81}), frozenset({66}), frozenset({59}), frozenset({76, 79}),\
frozenset({60}), frozenset({86}), frozenset({61}), frozenset({62}),\
frozenset({69}), frozenset({55}), frozenset({67, 71}), frozenset({74, 77}),\
frozenset({67, 70}), frozenset({75}), frozenset({68}), frozenset({63}),\
frozenset({74, 70}), frozenset({81}), frozenset({82}), frozenset({57}),\
frozenset({65}), frozenset({76}), frozenset({71}), frozenset({74}),\
frozenset({79}), frozenset(), frozenset({72}), frozenset({72, 69}),\
frozenset({83}), frozenset({67}), frozenset({74, 71})}

# Find the songs with valid notes and chords and remove the other songs. 
# Again notice that a note is the set of notes playing in the melody of a song, 
# and a chord is the set of notes playing in the chord of a song. Notice 
# the double use of 'chord', which we keep, for simplicity

#q = song_to_chorddurlist(CHORDS_DIR + "/" + 'reelsd-g72.mid')
#print(q)

#set_to_remove = set()
#num_validsongs = 0
#for f in ALLSONGNAMES:
#    if song_validchords(CHORDS_DIR + "/" + f, set_chords) +\
# song_validchords(MELODY_DIR + "/" + f, set_melody) !=2:
#        set_to_remove.add(f)
#print(len(set_chords), len(set_melody))
#print(set_to_remove)
#

set_to_remove = {'jigs115.mid', 'reelsd-g28.mid', 'reelsh-l62.mid',\
'reelsh-l55.mid', 'waltzes30.mid', 'jigs249.mid', 'reelsh-l84.mid',\
'reelsu-z3.mid', 'jigs254.mid', 'jigs74.mid', 'reelsd-g41.mid',\
'reelsd-g52.mid', 'reelsa-c66.mid', 'reelsh-l66.mid', 'jigs193.mid',\
'ashover43.mid', 'jigs281.mid', 'reelsd-g4.mid', 'jigs130.mid',\
'reelsd-g30.mid', 'jigs260.mid', 'reelsd-g83.mid', 'reelsh-l80.mid',\
'reelsu-z31.mid', 'reelsm-q25.mid', 'reelsm-q53.mid', 'jigs212.mid',\
'jigs197.mid', 'reelsm-q54.mid', 'reelsu-z6.mid', 'jigs104.mid',\
'reelsa-c30.mid', 'reelsh-l57.mid', 'xmas4.mid', 'reelsm-q29.mid',\
'jigs198.mid', 'reelsu-z15.mid', 'ashover19.mid', 'jigs230.mid',\
'reelsr-t3.mid', 'ashover41.mid', 'jigs339.mid', 'ashover46.mid',\
'reelsd-g9.mid', 'reelsa-c38.mid', 'reelsh-l88.mid', 'reelsm-q1.mid',\
'ashover9.mid', 'jigs86.mid'}

ALLSONGNAMES = ALLSONGNAMES - set_to_remove

# Check for pauses between chords

#num_songs_nofrozen = 0
#s = frozenset()
#for f in ALLSONGNAMES:
#    v       = CHORDS_DIR + "/" + f
#    q       = song_to_chordlist(v)
#    bigset  = set(q)
#    if lastpos_in_chordlist(q, s) >0:
#        print(f)
# No pauses for the chords!

# Check that notes in a chord always match perfectly in time
# i.e. chords change discretely, meaning all notes in a chord 
# are turned off before the notes in the next chord are turned on
# Check that melodies and chords are properly encoded

#for f in ALLSONGNAMES:
#    #f = 'ashover1.mid'
#    #v = CHORDS_DIR + "/" + f
#    q = song_check(MELODY_DIR + "/" + f)
#    if q != {1} and q != set():
#        print(f, q)
#    q = song_check(CHORDS_DIR + "/" + f)
#    if q != set():
#        print(f, q)

# True

# Check that song_durlist and duration_difference are consistent
#for f in ALLSONGNAMES:
#    #f = 'ashover1.mid'
#    c = song_to_chorddurlist(CHORDS_DIR + "/" + f)
#    c = c[1]
#    m = song_to_chorddurlist(MELODY_DIR + "/" + f)
#    m = m[1]
#    d = song_duration_difference(f)
#    if d != sum(c) - sum(m):
#        print(f, d, sum(c), sum(m))
## They are

#Remove songs with time intervals not divisible by TIMESTEP
#set_to_remove = set()
#set_durations = set()
#for f in ALLSONGNAMES:
#    melody  = set(song_to_chorddurlist(MELODY_DIR + "/" + f)[1])
#    chord   = set(song_to_chorddurlist(CHORDS_DIR + "/" + f)[1])
#    alldur  = melody | chord
#    alldur  = list(alldur)
#    remove_song = 0
#    s = set(alldur)
#    for dur in s:
#        if dur % TIMESTEP !=0:
#            remove_song = 1
#            #print(dur)
#        else:
#            set_durations.add(dur)
#    if remove_song ==1:
#        set_to_remove.add(f)
#print(set_durations)
#print(len(set_to_remove))
#print(set_to_remove)

set_to_remove = {'reelsh-l28.mid', 'jigs170.mid', 'hpps3.mid', 'ashover2.mid',\
'reelsr-t74.mid', 'morris14.mid', 'reelsd-g61.mid', 'reelsu-z26.mid',\
'hpps57.mid', 'hpps10.mid', 'reelsh-l32.mid', 'hpps23.mid', 'reelsm-q4.mid',\
'jigs234.mid', 'hpps49.mid', 'hpps41.mid', 'reelsd-g12.mid', 'reelsm-q24.mid',\
'jigs151.mid', 'jigs332.mid', 'reelsr-t62.mid', 'hpps54.mid', 'reelsh-l51.mid',\
'reelsh-l82.mid', 'reelsd-g71.mid', 'reelsd-g80.mid', 'reelsm-q38.mid',\
'hpps45.mid', 'hpps34.mid', 'hpps42.mid', 'reelsa-c79.mid', 'jigs328.mid',\
'reelsu-z22.mid', 'jigs168.mid', 'reelsu-z19.mid', 'ashover20.mid',\
'hpps12.mid', 'reelsd-g55.mid', 'hpps2.mid', 'slip5.mid', 'reelsu-z17.mid',\
'ashover17.mid', 'ashover33.mid', 'jigs287.mid','reelsa-c69.mid',\
'waltzes52.mid', 'reelsr-t70.mid', 'hpps8.mid', 'hpps15.mid', 'reelsr-t78.mid',\
'hpps48.mid', 'reelsa-c23.mid','hpps55.mid', 'ashover23.mid', 'hpps52.mid',\
'reelsr-t69.mid', 'reelsr-t24.mid', 'reelsa-c45.mid', 'reelsa-c65.mid',\
'jigs59.mid', 'hpps53.mid', 'jigs255.mid', 'reelsm-q37.mid', 'reelsu-z7.mid',\
'hpps47.mid', 'hpps63.mid', 'reelsm-q28.mid', 'hpps35.mid', 'jigs318.mid',\
'reelsh-l26.mid', 'reelsd-g79.mid', 'jigs308.mid', 'reelsr-t23.mid',\
'reelsd-g74.mid', 'hpps40.mid', 'hpps36.mid', 'waltzes1.mid','waltzes38.mid',\
'jigs311.mid', 'jigs153.mid', 'hpps31.mid', 'hpps29.mid', 'reelsr-t12.mid',\
'hpps19.mid', 'hpps30.mid', 'hpps60.mid', 'reelsr-t71.mid', 'reelsa-c28.mid',\
'jigs340.mid', 'reelsa-c62.mid', 'hpps59.mid', 'jigs107.mid', 'reelsh-l43.mid',\
'hpps46.mid', 'reelsa-c71.mid', 'reelsr-t64.mid', 'hpps13.mid', 'jigs227.mid',\
'morris15.mid', 'reelsm-q56.mid', 'reelsd-g54.mid', 'reelsd-g40.mid',\
'jigs285.mid', 'hpps43.mid', 'reelsm-q73.mid', 'jigs52.mid', 'hpps6.mid',\
'jigs242.mid', 'hpps16.mid', 'reelsa-c34.mid', 'hpps14.mid', 'reelsr-t75.mid',\
'reelsr-t22.mid', 'hpps4.mid', 'reelsu-z29.mid', 'morris25.mid',\
'reelsr-t51.mid', 'hpps18.mid', 'reelsr-t20.mid', 'jigs307.mid',\
'reelsd-g37.mid', 'reelsa-c29.mid', 'reelsa-c22.mid', 'hpps20.mid',\
'hpps5.mid', 'reelsh-l25.mid', 'reelsm-q27.mid','hpps64.mid', 'morris10.mid',\
'hpps39.mid'}


ALLSONGNAMES = ALLSONGNAMES - set_to_remove

# Remove songs which have nondivisible chord and melody lists
#set_to_remove = set()
#for f in ALLSONGNAMES:
#    a = song_to_chorddurlist(MELODY_DIR + "/" + f)
#    b = song_to_chorddurlist(CHORDS_DIR + "/" + f)
#    c = chorddurlists_to_soundlist(a, b)
#    if type(c) != list:
#        set_to_remove.add(f)
#        print(f) 
#print(set_to_remove)

set_to_remove = {'jigs161.mid', 'jigs182.mid', 'waltzes44.mid',\
'reelsh-l89.mid', 'reelsh-l30.mid', 'jigs263.mid', 'jigs295.mid'}

ALLSONGNAMES = ALLSONGNAMES - set_to_remove

# Remove songs with melody duration > DUR_THRESH
#set_to_remove = set()
#duration_dictionary = {}
#num_events          = 0
#for f in ALLSONGNAMES:
#    a = song_to_chorddurlist(MELODY_DIR + '/' + f)[1]
#    a = set(a)
#    for dur in a:
#        if dur > DUR_THRESH:
#            set_to_remove.add(f)
#print(set_to_remove)

set_to_remove = {'playford13.mid'}
ALLSONGNAMES = ALLSONGNAMES - set_to_remove




#Confirm the chords and duration lists have the same size
#for f in ALLSONGNAMES:
#    a = song_to_chorddurlist(MELODY_DIR + '/' + f)
#    b = song_to_chorddurlist(CHORDS_DIR + '/' + f)
#    if len(a[0]) != len(a[1]) or len(b[0])!= len(b[1]):
#        print(f)
# True

# Add the continuation event for set_melody and set_chords
# This indicates that the current chord playing is a continuation
# of the previous one
set_melody.add(CONTINUATION_CHORD)
set_chords.add(CONTINUATION_CHORD)

#DICT_ALLCHORDS, DICT_MELODY, DICT_CHORDS = \
#dictionary_from_notes_chords(set_melody, set_chords)
#print(DICT_ALLCHORDS)
#print(DICT_MELODY)
#print(DICT_CHORDS)

DICT_ALLCHORDS  = {1: frozenset(), 2: frozenset({84}), 3: frozenset({67, 71}),\
4: frozenset({74, 77}), 5: frozenset({67, 70}),\
6: frozenset({79}), 7: frozenset({73, 67, 69}), 8: frozenset({77}),\
9: frozenset({75}), 10: frozenset({72}), 11: frozenset({78}),\
12: frozenset({64, 60}), 13: frozenset({68}), 14: frozenset({63}),\
15: frozenset({59}), 16: frozenset({-1}), 17: frozenset({70}),\
18: frozenset({74}), 19: frozenset({74, 70}), 20: frozenset({81}),\
21: frozenset({82}), 22: frozenset({57}), 23: frozenset({65}),\
24: frozenset({76}), 25: frozenset({76, 79}), 26: frozenset({72, 76}),\
27: frozenset({60}), 28: frozenset({69}),29: frozenset({72, 69}),\
30: frozenset({83}), 31: frozenset({80}), 32: frozenset({86}),\
33: frozenset({61}), 34: frozenset({73}),35: frozenset({62}),\
36: frozenset({71}), 37: frozenset({67}), 38: frozenset({64}),\
39: frozenset({74, 71}), 40: frozenset({55}),41: frozenset({81, 73}),\
42: frozenset({72, 81}), 43: frozenset({66}), 44: frozenset(),\
45: frozenset({50, 43, 52, 47}),46: frozenset({49, 52, 45, 55}),\
47: frozenset({49, 42, 46}), 48: frozenset({49, 42, 45}),\
49: frozenset({40, 50, 43, 47}),50: frozenset({50, 43, 53, 47}),\
51: frozenset({40, 43, 36, 46}), 52: frozenset({-1}),\
53: frozenset({50, 43, 47}), 54: frozenset({50, 54, 47}),\
55: frozenset({43, 36, 39}), 56: frozenset({43, 46, 39}),\
57: frozenset({50, 43, 46}),58: frozenset({48, 52, 45, 55}),\
59: frozenset({42, 36, 39}), 60: frozenset({40, 43, 36}),\
61: frozenset({48, 51, 45}), 62: frozenset({48, 41, 51, 45}),\
63: frozenset({48, 42, 45, 38}), 64: frozenset({49, 42, 52, 46}),\
65: frozenset({40, 44, 37}),66: frozenset({40, 43, 46}),\
67: frozenset({51, 54, 47}), 68: frozenset({40, 43, 47}),\
69: frozenset({42, 45, 39}), 70: frozenset({49, 52, 45}),\
71: frozenset({48, 52, 45}), 72: frozenset({40, 43, 36, 45}),\
73: frozenset({40, 44, 47}), 74: frozenset({40, 50, 44, 47}),\
75: frozenset({50, 53, 46}), 76: frozenset({57, 51, 54, 47}),\
77: frozenset({48, 41, 45}), 78: frozenset({42, 45, 38}),\
79: frozenset({49, 43, 46}), 80: frozenset({48, 41, 44}),\
81: frozenset({41, 45, 38})}
DICT_MELODY     = {frozenset(): 1, frozenset({84}): 2, frozenset({67, 71}): 3,\
frozenset({74, 77}): 4, frozenset({67, 70}): 5,\
frozenset({79}): 6, frozenset({73, 67, 69}): 7, frozenset({77}): 8,\
frozenset({75}): 9, frozenset({72}): 10, frozenset({78}): 11,\
frozenset({64, 60}): 12, frozenset({68}): 13, frozenset({63}): 14,\
frozenset({59}): 15, frozenset({-1}): 16, frozenset({70}): 17,\
frozenset({74}): 18, frozenset({74, 70}): 19, frozenset({81}): 20,\
frozenset({82}): 21, frozenset({57}): 22, frozenset({65}): 23,\
frozenset({76}): 24, frozenset({76, 79}): 25, frozenset({72, 76}): 26,\
frozenset({60}): 27, frozenset({69}): 28, frozenset({72, 69}): 29,\
frozenset({83}): 30, frozenset({80}): 31, frozenset({86}): 32,\
frozenset({61}): 33, frozenset({73}): 34, frozenset({62}): 35,\
frozenset({71}): 36, frozenset({67}): 37, frozenset({64}): 38,\
frozenset({74, 71}): 39, frozenset({55}): 40,\
frozenset({81, 73}): 41, frozenset({72, 81}): 42, frozenset({66}): 43}
DICT_CHORDS     = {frozenset(): 44, frozenset({50, 43, 52, 47}): 45,\
frozenset({49, 52, 45, 55}): 46, frozenset({49, 42, 46}): 47,\
frozenset({49, 42, 45}): 48, frozenset({40, 50, 43, 47}): 49,\
frozenset({50, 43, 53, 47}): 50, frozenset({40, 43, 36, 46}): 51,\
frozenset({-1}): 52, frozenset({50, 43, 47}): 53, frozenset({50, 54, 47}): 54,\
frozenset({43, 36, 39}): 55, frozenset({43, 46, 39}): 56,\
frozenset({50, 43, 46}): 57, frozenset({48, 52, 45, 55}): 58,\
frozenset({42, 36, 39}): 59, frozenset({40, 43, 36}): 60,\
frozenset({48, 51, 45}): 61, frozenset({48, 41, 51, 45}): 62,\
frozenset({48, 42, 45, 38}): 63, frozenset({49, 42, 52, 46}): 64,\
frozenset({40, 44, 37}): 65, frozenset({40, 43, 46}): 66,\
frozenset({51, 54, 47}): 67, frozenset({40, 43, 47}): 68,\
frozenset({42, 45, 39}): 69, frozenset({49, 52, 45}): 70,\
frozenset({48, 52, 45}): 71, frozenset({40, 43, 36, 45}): 72,\
frozenset({40, 44, 47}): 73, frozenset({40, 50, 44, 47}): 74,\
frozenset({50, 53, 46}): 75, frozenset({57, 51, 54, 47}): 76,\
frozenset({48, 41, 45}): 77, frozenset({42, 45, 38}): 78,\
frozenset({49, 43, 46}): 79, frozenset({48, 41, 44}): 80,\
frozenset({41, 45, 38}): 81}
DICT_SIZE           = len(DICT_ALLCHORDS)
MELODYCHORDS_LEN    = len(DICT_MELODY)
CHORDCHORDS_LEN     = len(DICT_CHORDS)
#print(MELODYCHORDS_LEN, CHORDCHORDS_LEN)

# Parse all songs. Split each into a segment of size SEGMENTSIZE.
# Shuffle the segments and store the data
list_allsegments         = []
for f in ALLSONGNAMES:
    melody_chorddurlist     = song_to_chorddurlist(MELODY_DIR +\
     '/' + f)
    chord_chorddurlist      = song_to_chorddurlist(CHORDS_DIR +\
     '/' + f)
    soundlist               = chorddurlists_to_soundlist(melody_chorddurlist,\
     chord_chorddurlist)
    granular_soundlist      = soundlist_split(soundlist, TIMESTEP)
    song_segmentlist        = soundlist_to_segmentlist(granular_soundlist,\
     DICT_MELODY, DICT_CHORDS, CONTINUATION_CHORD, SEGMENT_SIZE)
    list_allsegments        = list_allsegments + song_segmentlist

shuffle(list_allsegments)
list_allsegments_twohot = tuplesegmentlist_to_twohotsegmentlist(\
    list_allsegments, DICT_SIZE)
data                    = np.asarray(list_allsegments_twohot)

# Create x and y data
x_dat, y_dat            = inputdata_to_xydata(data)
print(x_dat.shape, y_dat.shape)
np.save(DATA_X_NAME, x_dat)
np.save(DATA_Y_NAME, y_dat)















