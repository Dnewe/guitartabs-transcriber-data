

# gp file filters
REQUIRED_TUNING = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
REQUIRED_STRINGSNUM = 6


# information on data csv file
DATACSV_HEADER = ['strings', 
                  'frets', 
                  'pitches-2', 
                  'pitches-1', 
                  'pitches', 
                  'pitches+1', 
                  'pitches+2'] # will need to be flatten (for multiple notes)


#NOTE_EFFECTS = ['rightHandFinger', 'slides','harmonic']

# information on report csv file
REPORTCSV_HEADER = ['filepath','success']