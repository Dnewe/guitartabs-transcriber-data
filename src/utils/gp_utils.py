import guitarpro as gp
import config


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def convert_pitch_to_str(pitch: int) -> str:
    octave = pitch // 12 - 1
    note = NOTE_NAMES[pitch%12]
    return f"{note}{octave}"


def convert_str_to_pitch(notestr: str) -> int:
    octave= (int) (notestr[-1])
    note = notestr[0:-1]
    return (octave+1)*12 + NOTE_NAMES.index(note)
    

def convert_note_to_pitch(note: gp.Note) -> int:
    tuning = convert_str_to_pitch(config.TUNING[6 - note.string])
    fret_number = note.value
    return tuning + fret_number


def get_note_position(note: gp.Note) -> int:

    position = 0
    for s in range(-note.string+6):
        pitch_string = convert_str_to_pitch(config.TUNING[s])
        delta_pitch = (convert_note_to_pitch(note) - pitch_string)%12

        position += (config.FRETS_NUM - delta_pitch) // 12 + 1
    
    position += note.value//12 + 1
    
    return position