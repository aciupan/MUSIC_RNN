# Stores constants
MELODY_DIR 				= "data/melody"
CHORDS_DIR				= "data/chords"
DATA_X_NAME 			= 'x_data'
DATA_Y_NAME	 			= 'y_data'
SEGMENT_SIZE 			= 256
VELOCITY				= 90
TIMESTEP                = 128
CONTINUATION_CHORD      = frozenset({-1})

# Produced in processdata.py and used by composition.py
DICT_ALLCHORDS  = {1: frozenset(), 2: frozenset({84}), 3: frozenset({67, 71}),\
4: frozenset({74, 77}), 5: frozenset({67, 70}), 6: frozenset({79}),\
7: frozenset({73, 67, 69}), 8: frozenset({77}),\
9: frozenset({75}), 10: frozenset({72}), 11: frozenset({78}),\
12: frozenset({64, 60}), 13: frozenset({68}), 14: frozenset({63}),\
15: frozenset({59}), 16: frozenset({-1}), 17: frozenset({70}),\
18: frozenset({74}), 19: frozenset({74, 70}), 20: frozenset({81}),\
21: frozenset({82}), 22: frozenset({57}), 23: frozenset({65}),\
24: frozenset({76}), 25: frozenset({76, 79}), 26: frozenset({72, 76}),\
27: frozenset({60}), 28: frozenset({69}),\
29: frozenset({72, 69}), 30: frozenset({83}), 31: frozenset({80}),\
32: frozenset({86}), 33: frozenset({61}), 34: frozenset({73}),\
35: frozenset({62}), 36: frozenset({71}), 37: frozenset({67}),\
38: frozenset({64}), 39: frozenset({74, 71}), 40: frozenset({55}),\
41: frozenset({81, 73}), 42: frozenset({72, 81}), 43: frozenset({66}),\
44: frozenset(), 45: frozenset({50, 43, 52, 47}),\
46: frozenset({49, 52, 45, 55}), 47: frozenset({49, 42, 46}),\
48: frozenset({49, 42, 45}), 49: frozenset({40, 50, 43, 47}),\
50: frozenset({50, 43, 53, 47}), 51: frozenset({40, 43, 36, 46}),\
52: frozenset({-1}), 53: frozenset({50, 43, 47}),\
54: frozenset({50, 54, 47}), 55: frozenset({43, 36, 39}),\
56: frozenset({43, 46, 39}), 57: frozenset({50, 43, 46}),\
58: frozenset({48, 52, 45, 55}), 59: frozenset({42, 36, 39}),\
60: frozenset({40, 43, 36}), 61: frozenset({48, 51, 45}),\
62: frozenset({48, 41, 51, 45}), 63: frozenset({48, 42, 45, 38}),\
64: frozenset({49, 42, 52, 46}), 65: frozenset({40, 44, 37}),\
66: frozenset({40, 43, 46}), 67: frozenset({51, 54, 47}),\
68: frozenset({40, 43, 47}), 69: frozenset({42, 45, 39}),\
70: frozenset({49, 52, 45}), 71: frozenset({48, 52, 45}),\
72: frozenset({40, 43, 36, 45}), 73: frozenset({40, 44, 47}),\
74: frozenset({40, 50, 44, 47}),\
75: frozenset({50, 53, 46}), 76: frozenset({57, 51, 54, 47}),\
77: frozenset({48, 41, 45}), 78: frozenset({42, 45, 38}),\
79: frozenset({49, 43, 46}), 80: frozenset({48, 41, 44}),\
81: frozenset({41, 45, 38})}
DICT_MELODY     = {frozenset(): 1, frozenset({84}): 2, frozenset({67, 71}): 3,\
frozenset({74, 77}): 4, frozenset({67, 70}): 5,
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
frozenset({74, 71}): 39, frozenset({55}): 40, frozenset({81, 73}): 41,\
frozenset({72, 81}): 42, frozenset({66}): 43}
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
frozenset({40, 44, 47}): 73, frozenset({40, 50, 44, 47}): 74, \
frozenset({50, 53, 46}): 75, frozenset({57, 51, 54, 47}): 76,\
frozenset({48, 41, 45}): 77, frozenset({42, 45, 38}): 78,\
frozenset({49, 43, 46}): 79, frozenset({48, 41, 44}): 80,\
frozenset({41, 45, 38}): 81}

# Created in n1_processinput
DICT_SIZE               = 81
MELODYCHORDS_LEN        = 43
CHORDCHORDS_LEN         = 38
