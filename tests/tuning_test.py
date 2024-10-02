import guitarpro
from gp.gpfile_handler import check_track_validity

#gp_file = guitarpro.parse('h:\Documents\projets\GuitarTabsML\data\Guitar_Pro_Tabs\Tabs\A\ACDC\ACDC - Back in Black.gp3')
gp_file = guitarpro.parse('h:\Documents\projets\GuitarTabsML\data\Guitar_Pro_Tabs\Tabs\A\Acta\Acta - Ce Qui M_\'incombe.gp4')

for track in gp_file.tracks:
    if track.isPercussionTrack:
        continue
    
    for string in track.strings:
        tuning = string.value
        print(f"String {string.number}: {tuning} (MIDI pitch)")

        # Optionally convert the MIDI pitch number to a human-readable note
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = tuning // 12 - 1
        note = note_names[tuning % 12]
        print(f"Tuned to: {note}{octave}")

    print(f'Valid : {check_track_validity(track)}')
