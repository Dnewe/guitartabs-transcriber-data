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


def valid_track(track: gp.Track) -> bool:
    # filter out percussion
    if track.isPercussionTrack:
        return False 
    # filter out guitar with too many frets
    if track.fretCount> config.FRETS:
        return False
    # filter out guitar with a different capo
    if track.offset != config.CAPO:
        return False
    
    # count strings and determine tuning
    stringsnum = 0
    tuning = []
    for string in track.strings:
        stringsnum += 1
        tuning.append(string.value)
   
    # check tuning / number of strings according to config
    correct_tuning = (config.TUNING == [convert_pitch_to_str(pitch) for pitch in tuning][::-1])
    correct_stringsnum = (stringsnum == config.STRINGS)

    is_valid = correct_tuning and correct_stringsnum
    return is_valid