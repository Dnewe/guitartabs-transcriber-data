import guitarpro as gp
import config
from typing import Tuple


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def convert_pitch_to_str(pitch: int) -> str:
    note = NOTE_NAMES[pitch%12]
    octave = pitch // 12 - 1
    return f"{note}{octave}"


def pitch_to_note_octave(pitch: int) -> Tuple[int,int]:
    note = pitch%12 + 1
    octave = pitch // 12 - 1
    return note,octave


def convert_str_to_pitch(notestr: str) -> int:
    octave= (int) (notestr[-1])
    note = notestr[0:-1]
    return (octave+1)*12 + NOTE_NAMES.index(note)
    

def convert_note_to_pitch(note: gp.Note) -> int:
    tuning = convert_str_to_pitch(config.TUNING[6 - note.string])
    fret_number = note.value
    return tuning + fret_number
