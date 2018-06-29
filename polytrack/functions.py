from mido import MidiFile, Message, MidiTrack
import os
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
import tensorflow as tf


# Output MIDI content of a song into a txt file
def write_content_to_txt(input, output):
    # create the file
    f = open(output, "w+")
    f.close()
    # empty the file
    open(output, 'w').close()
    # Write the song to the txt file
    mid = MidiFile(input)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            s = str(msg)
            with open(output, "a") as myfile:
                myfile.write(s + "\n")

# Total duration of a song. We have to divide by 2 since the 'time' input was
# encoded as double its actual length
def total_time_duration(input):
    dur = 0
    mid = MidiFile(input)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                dur += msg.time // 2
    return dur

# From a MIDI msg event, obtain the note
def get_note(msg):
    s = str(msg)
    j = s.find("note=")
    s = s[j:]
    note = int(s[5:s.find(" ")])
    return note

# Calculate the difference in duration between tracks
def song_duration_difference(name, chords_dir, melody_dir):
    output = total_time_duration(chords_dir + "/" + name) -\
    total_time_duration(melody_dir + "/" + name)
    return output

# Perform a few quality checks on a MIDI file
def chord_seq_valid(input):
    cur_notes_on = set()
    chord_succession = []
    mid = MidiFile(input)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                if msg.time >0:
                    chord_succession.append(cur_notes_on)
                note = get_note(msg)
                if msg.type == 'note_on':
                    if note not in cur_notes_on:
                        cur_notes_on.add(note)
                    else:
                        return 0
                        print("Note already on")
                if msg.type == 'note_off':
                    if note in cur_notes_on:
                        cur_notes_on.remove(note)
                    else:
                        return 0
                        print("Note not on before off")
                #print(cur_notes_on)
    return 1

# Number of sound events in a MIDI song
def song_numevents(input):
    num_events = 0
    mid = MidiFile(input)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                if msg.time >0:
                    num_events +=1
    return num_events

# Transforms a MIDI song to its corresponding sequence of sounds and
# their durations
def song_to_chorddurlist(input):
    cur_notes_on = set()
    num_events = song_numevents(input)
    #print(num_events)
    chord_succession = [frozenset() for _ in range(num_events)]
    durations = []
    cur_succession = 0
    mid = MidiFile(input)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                if msg.time >0:
                    # we need to create a copy of cur_notes_on because it is modified
                    # inside these loops
                    q = frozenset(cur_notes_on) 
                    chord_succession[cur_succession] = q
                    durations.append(msg.time//2) # we divide by 2 in order to keep the correct time
                    cur_succession +=1
                note = get_note(msg)
                if msg.type == 'note_on':
                    if note not in cur_notes_on:
                        cur_notes_on.add(note)
                    else:
                        print("Note already on")
                        return 0
                if msg.type == 'note_off':
                    if note in cur_notes_on:
                        cur_notes_on.remove(note)
                    else:
                        print("Note not on before off")
                        return 0
                #print(cur_notes_on)
    #print(chord_succession[2])
    return chord_succession, durations

# Confirm if a MIDI song has all sound events from a set of
# predetermined chords
def song_validchords(input, set_chords):
    s = set(song_to_chorddurlist(input)[0])
    #print(s)
    #print(set_chords)
    if s.issubset(set_chords):
        return 1
    else:
        return 0

# Find the last position of a given chord in a list of chords
def lastpos_in_chordlist(chordlist, chord):
    lastpos = -1
    l = len(chordlist)
    for i in range(l):
        if chord == chordlist[i]:
            lastpos = i
    return lastpos

# Performs various checks on a MIDI file to ensure it can be processed
# subsequently
def song_check(input):
    cur_notes_on = set()
    num_events = song_numevents(input)
    #print(num_events)
    chord_succession = [frozenset() for _ in range(num_events)]
    cur_succession = 0
    moment = 0
    prev_event = 'initial'
    error_set = set()
    mid = MidiFile(input)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                if msg.time >0:
# we need to create a copy of cur_notes_on because it is modified
# inside these loops
                    q = frozenset(cur_notes_on) 
                    chord_succession[cur_succession] = q
                    cur_succession +=1
                    if msg.type == 'note_on' and moment !=0:
                        error_set.add(1)
                note = get_note(msg)
                if msg.type == 'note_on':
                    if prev_event == 'note_off':
                        if cur_notes_on != set():
                            print(cur_notes_on)
                            error_set.add(2)
                    if note not in cur_notes_on:
                        cur_notes_on.add(note)
                    else:
                        print("Note already on")
                        error_set.add(3)
                if msg.type == 'note_off':
                    if note in cur_notes_on:
                        cur_notes_on.remove(note)
                    else:
                        print("Note not on before off")
                        error_set.add(4)
                #print(cur_notes_on)
                prev_event = msg.type
                moment += 1    
    #print(chord_succession[2])
    return error_set

#def song_durlist(input):
#    durations = []
#    mid = MidiFile(input)
#    for i, track in enumerate(mid.tracks):
#        for msg in track:
#            if msg.type == 'note_on' or msg.type == 'note_off':
#                dur = msg.time
#                if dur >0:
#                    durations.append(dur)
#    return durations

# For two lists of durations, where each list can be interpreted as a list
# of segments, confirm that if two segments from the two lists overlap, 
# then one is a subset of the other.
def chorddurlists_to_soundlist(chorddurlist_a, chorddurlist_b):
    dur_a                           = chorddurlist_a[1]
    dur_b                           = chorddurlist_b[1]
    chords_a                        = chorddurlist_a[0]
    chords_b                        = chorddurlist_b[0]
    num_a                           = len(dur_a)
    num_b                           = len(dur_b)
    cur_a                           = 0
    cur_b                           = 0
    t                               = 0
    previous_cut                    = 'initial'
    currently_ate_from_segment_a    = 0
    currently_ate_from_segment_b    = 0
    err_1                           = 0
    err_2                           = 0
    moment                          = 0
    #indicates if chord played is new or continuation of previous time period
    a_new                           = 1 
    b_new                           = 1 
    sound_list                      = []
    # ignore pauses at the beginning of a song
    start_appending                 = 0 
    while(cur_a     < num_a and cur_b < num_b):
        moment +=1
        len_a               = dur_a[cur_a]
        len_b               = dur_b[cur_b]
        a_left              = len_a - currently_ate_from_segment_a
        b_left              = len_b - currently_ate_from_segment_b
        dur                 = min(a_left, b_left)
        a_current_chord     = chords_a[cur_a]
        b_current_chord     = chords_b[cur_b]
        sound_moment = (dur,(a_current_chord, a_new), (b_current_chord, b_new))
        if a_current_chord!= set() or b_current_chord != set():
            start_appending = 1
        if start_appending ==1:
            sound_list.append(sound_moment)
        if a_left < b_left:
            currently_ate_from_segment_b += a_left
            currently_ate_from_segment_a = 0
            cur_a +=1
            a_new = 1
            b_new = 0
            if previous_cut == 'b':
                err_1 = 1
                #print(moment)
            previous_cut = 'a'
        if b_left < a_left:
            currently_ate_from_segment_b  = 0
            currently_ate_from_segment_a += b_left
            cur_b +=1
            b_new = 1
            a_new = 0
            if previous_cut == 'a':
                err_2 = 1
                #print(moment)
            previous_cut = 'b'
        if a_left == b_left:
            currently_ate_from_segment_a = 0
            currently_ate_from_segment_b = 0
            cur_a +=1
            cur_b +=1
            a_new = 1
            b_new = 1
            previous_cut = 'tie'
    if err_1 + err_2 !=0:
        return (err_1, err_2)
    return sound_list

# Split a sound list into smaller time steps and produces a new sound list
# which is identical compositionally
def soundlist_split(soundlist, timestep):
    granular_soundlist = []
    for sound in soundlist:
        dur                 = sound[0]
        melody              = sound[1]
        chord               = sound[2]
        melody_chords       = melody[0]
        melody_neworcont    = melody[1]
        chord_chords        = chord[0]
        chord_neworcont     = chord[1]
        if dur % timestep != 0:
            print("Error. Song event has duration not divisible by the timestep")
            return 0
        else:
            n_ministeps = dur//timestep
            for i in range(n_ministeps):
                #time = (i+1)*timestep
                if i == 0:
                    cur_melody_neworcont    = melody_neworcont
                    cur_chord_neworcont     = chord_neworcont
                else:
                    cur_melody_neworcont    = 0
                    cur_chord_neworcont     = 0
                melody_info = (melody_chords, cur_melody_neworcont)
                chord_info  = (chord_chords, cur_chord_neworcont)
                granular_soundlist.append((timestep, melody_info, chord_info))
                #print((timestep, melody_info, chord_info))
    return granular_soundlist

# From the set of melody and chords sounds, create the dictionary of all events
def dictionary_from_notes_chords(set_melody, set_chords):
    list_melody = list(set_melody)
    list_melody.sort()
    list_chords = list(set_chords)
    list_chords.sort()

    dict_allchords  = {}
    dict_melody     = {}
    dict_chords     = {}
    eventid         = 0
    for melody_chord in list_melody:
        eventid +=1
        dict_allchords[eventid]     = melody_chord
        dict_melody[melody_chord]   = eventid
    for chord_chord in list_chords:
        eventid +=1
        dict_allchords[eventid]     = chord_chord
        dict_chords[chord_chord]    = eventid
    return  dict_allchords, dict_melody, dict_chords

# From the list of sounds and their durations, adds a track corresponding
# to that list, to an existing MIDI file
def addtrack_to_midi(onetrack_soundlist, track, midifile, velocity):
    midifile.tracks.append(track)
    track.append(Message('pitchwheel', channel=0, pitch=0, time=0))
    prev_chords = set()
    chord_time  = 0
    delay       = 0
    for event in onetrack_soundlist:
        duration    = event[0]
        cur_chords  = event[1][0]
        is_new      = event[1][1]

        if is_new ==0:
            chord_time += duration
        if is_new ==1:
            # turn off the old chords
            first_note_in_chord = 1
            for note in prev_chords:
                if first_note_in_chord ==1:
                    m = Message('note_off', note = note, \
                        velocity = velocity, time = chord_time)
                    track.append(m)
                    first_note_in_chord = 0
                else:
                    m = Message('note_off', note = note, \
                        velocity = velocity, time = 0)
                    track.append(m)
            # add the new chords
            first_note_in_chord = 1
            for note in cur_chords:
                if first_note_in_chord ==1:
                    if prev_chords == set():
                        m = Message('note_on', note = note, \
                            velocity = velocity, time =chord_time)
                        track.append(m)
                    else:
                        m = Message('note_on', note = note, \
                            velocity = velocity, time =0)
                        track.append(m)
                    first_note_in_chord = 0
                else:
                    m = Message('note_on', note = note, \
                        velocity = velocity, time = 0)
                    track.append(m)
            chord_time = duration
            prev_chords = cur_chords
    # Turn off the final notes
    first_note_in_chord = 1
    for note in prev_chords:
        if first_note_in_chord ==1:
            m = Message('note_off', note = note, \
                velocity = velocity, time = chord_time)
            track.append(m)
            first_note_in_chord = 0
        else:
            m = Message('note_off', note = note, \
                velocity = velocity, time = 0)
            track.append(m)

# Starting from a two-track list of sounds and their duration, creates
# the corresponding MIDI file
def soundlist_to_midi(soundlist, output, velocity):
    melody_sounds       = [(v[0], v[1]) for v in soundlist]
    chord_sounds        = [(v[0], v[2]) for v in soundlist]
    mid                 = MidiFile()
    track_melody        = MidiTrack()
    track_chord         = MidiTrack()
    addtrack_to_midi(melody_sounds, track_melody, mid, velocity)
    addtrack_to_midi(chord_sounds, track_chord, mid, velocity)
    mid.save(output)

# Starting from an encoded track, creates its corresponding list of sounds and
# durations
def encoded_track_to_track_soundlist(input, allchords_dict, continuation_chord):
    prev_chords = -1
    moment = 0
    soundlist = []
    for enc_chord in input:
        moment+=1
        #print(moment)
        chord = allchords_dict[enc_chord]
        if chord == continuation_chord:
            #print(moment)
            chord_tuple = (prev_chord, 0)
        else:
            chord_tuple = (chord, 1)
            prev_chord = chord
        #print(chord_tuple)
        soundlist.append(chord_tuple)
    return soundlist

# Transforms a sequence of encoded sounds into a list of sounds and durations
def encoded_sound_to_soundlist(input, allchords_dict, \
    continuation_chord, timestep):
    l = len(input)
    encoded_melody_track    = [x[0] for x in input]
    encoded_chord_track     = [x[1] for x in input]
    melody_track            = \
    encoded_track_to_track_soundlist(encoded_melody_track, \
        allchords_dict, continuation_chord)
    chord_track             = \
    encoded_track_to_track_soundlist(encoded_chord_track, \
        allchords_dict, continuation_chord)
    timesteps = [timestep] * l
    return list(zip(timesteps, melody_track, chord_track))

# Transforms a track into a list of encoded events
def monosoundlist_to_eventlist(soundlist, dictionary, continuation_chord):
    eventlist           = []
    is_initialsound     = 1
    for sound in soundlist:
        if is_initialsound ==1:
            eventlist.append(dictionary[sound[0]])
            is_initialsound = 0
        else:
            if sound[1] == 0:
                eventlist.append(dictionary[continuation_chord])
            else:
                eventlist.append(dictionary[sound[0]])
    return eventlist

# Transforms a list of sounds and durations into a list of encoded events
def soundlist_to_eventlist(soundlist, dict_melody, dict_chords, continuation_chord):
    melody_soundlist    = [x[1] for x in soundlist]
    chord_soundlist     = [x[2] for x in soundlist]
    melody_eventlist    = monosoundlist_to_eventlist(melody_soundlist, dict_melody, continuation_chord)
    chord_eventlist     = monosoundlist_to_eventlist(chord_soundlist, dict_chords, continuation_chord)
    eventlist           = list(zip(melody_eventlist, chord_eventlist))
    return eventlist

# Splits a list of sounds and durations into smaller segments
def soundlist_to_segmentlist(soundlist, dict_melody, dict_chords, continuation_chord, segment_size):
    l = len(soundlist)
    segmentlist = []
    if l < segment_size:
        return segmentlist
    num_cuts = l // segment_size
    for i in range(num_cuts):
        soundlist_subset    = soundlist[i*segment_size : (i+1)*segment_size]
        segment             = soundlist_to_eventlist(soundlist_subset, dict_melody, dict_chords,continuation_chord)
        segmentlist.append(segment)
    return segmentlist

# Transforms a tuple of integers into its two-hot format
def tuple_to_twohot(tuple, dict_size):
    v = np.zeros(dict_size)
    v[tuple[0]-1] = 1
    v[tuple[1]-1] = 1
    return v

# Tuple segment to two-hot segment
def tuplesegment_to_twohotsegment(input_list, dict_size):
    return [tuple_to_twohot(x, dict_size) for x in input_list]

# List of tuple segments to list of two-hot segments
def tuplesegmentlist_to_twohotsegmentlist(input_list, dict_size):
    return [tuplesegment_to_twohotsegment(x, dict_size) for x in input_list]

# Creates the final data by shifting each event by 1 in the y data
def inputdata_to_xydata(input):
    segment_size =input.shape
    y = input[:, 1:, :]
    x = input[:, :-1,:]
    return x, y

# Creates LSTM cells
def lstm_cell(n_lstm_cells):
    return tf.contrib.rnn.LSTMBlockCell(n_lstm_cells)

# Transforma a two-hot vector into a tuple with the locations of the 
# values equal to 1.
def twohot_to_tuple(twohot_input):
    #twohot_input.astype(int)
    a       = np.where(twohot_input == 1)[0]
    #print(a)
    first   = a[0] +1
    second  = a[1] +1
    return first, second

# Applies the above function to a list
def twohotlist_to_tuplelist(twohotlist_input):
    return [twohot_to_tuple(x) for x in twohotlist_input]

# Transforms a list to an array
def list_to_array(inputlist):
    x = np.asarray(inputlist)
    return x

