

# gp file filters
TUNING = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
STRINGS = 6
FRETS = 24 # must be >=12
CAPO = 0 # 0 means no capo

# data distribution
MAX_POSITION = 3
MAX_POSITION_DISTR = 0.5
MAX_STRING_DISTR = 0.25


# information on data csv file
NUM_NOTES_BEFORE = 3
NUM_NOTES_AFTER = 6


DATACSV_HEADER = ([f'string_{i+1}' for i in range(STRINGS)] +
                  [f'position_{i+1}' for i in range(STRINGS)] +      
                  [item for n in range(NUM_NOTES_BEFORE,0,-1) for i in range(STRINGS) for item in (f'note-{n}_{i+1}',f'octave-{n}_{i+1}')] +
                  [item for i in range(STRINGS) for item in (f'note_{i+1}',f'octave_{i+1}')] + 
                  [item for n in range(NUM_NOTES_AFTER) for i in range(STRINGS) for item in (f'note+{n+1}_{i+1}',f'octave+{n+1}_{i+1}')])


'''DATACSV_HEADER_OLD = ([f'string_{i+1}' for i in range(STRINGS)] +
                  [f'position_{i+1}' for i in range(STRINGS)] +
                  [item for i in range(STRINGS) for item in (f'note_{i+1}',f'octave_{i+1}')] + 
                  [item for n in range(NUM_NOTES_BEFORE) for i in range(STRINGS) for item in (f'note-{n+1}_{i+1}',f'octave-{n+1}_{i+1}')] +
                  [item for n in range(NUM_NOTES_BEFORE) for i in range(STRINGS) for item in (f'note+{n+1}_{i+1}',f'octave+{n+1}_{i+1}')])'''


#NOTE_EFFECTS = ['rightHandFinger', 'slides','harmonic']

# information on report csv file
REPORTCSV_HEADER = ['filepath','success']