

# gp file filters
TUNING = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
STRINGS = 6
FRETS = 24 # must be >=12
CAPO = 0 # 0 means no capo

# data distribution
MAX_STRING_DISTR = 0.35


# information on data csv file
BEATS_BEFORE = 7
BEATS_AFTER = 7


DATACSV_HEADER = ([f'y_string_{i+1}' for i in range(STRINGS)] +   
                  [item for n in range(BEATS_BEFORE,0,-1) for i in range(STRINGS) for item in (f'x_note-{n}_{i+1}',f'x_octave-{n}_{i+1}',f'x_duration-{n}_{i+1}')] +
                  [item for i in range(STRINGS) for item in (f'x_note_{i+1}',f'x_octave_{i+1}', f'x_duration_{i+1}', f'x_isharmonic_{i+1}')] + 
                  [item for n in range(BEATS_AFTER) for i in range(STRINGS) for item in (f'x_note+{n+1}_{i+1}',f'x_octave+{n+1}_{i+1}', f'x_duration+{n+1}_{i+1}')])


#NOTE_EFFECTS = ['rightHandFinger', 'slides','harmonic']

# information on report csv file
REPORTCSV_HEADER = ['filepath','success']