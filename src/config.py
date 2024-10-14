

# gp file filters
REQUIRED_TUNING = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
REQUIRED_STRINGSNUM = 6


# information on data csv file
NUM_NOTES_BEFORE = 4
NUM_NOTES_AFTER = 4


DATACSV_HEADER = ([f'string_{i+1}' for i in range(6)] + 
                  [f'fret_{i+1}' for i in range(6)] + 
                  [f'pitch_{i+1}' for i in range(6)] +
                  [f'pitch-{n+1}_{i+1}' for n in range(NUM_NOTES_BEFORE) for i in range(6)] +
                  [f'pitch+{n+1}_{i+1}' for n in range(NUM_NOTES_AFTER) for i in range(6)])



#NOTE_EFFECTS = ['rightHandFinger', 'slides','harmonic']

# information on report csv file
REPORTCSV_HEADER = ['filepath','success']