

# gp file filters
TUNING = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
STRINGS_NUM = 6
FRETS_NUM = 24 # must be >=12
CAPO = 0 # 0 means no capo


# information on data csv file
NUM_NOTES_BEFORE = 20
NUM_NOTES_AFTER = 20


DATACSV_HEADER = ([f'position_{i+1}' for i in range(6)] +
                  [f'pitch_{i+1}' for i in range(6)] +
                  [f'pitch-{n+1}_{i+1}' for n in range(NUM_NOTES_BEFORE) for i in range(6)] +
                  [f'pitch+{n+1}_{i+1}' for n in range(NUM_NOTES_AFTER) for i in range(6)])


NOTES_POSITIONS = {}


#NOTE_EFFECTS = ['rightHandFinger', 'slides','harmonic']

# information on report csv file
REPORTCSV_HEADER = ['filepath','success']