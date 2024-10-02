
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def convert_MIDIpitch(pitch: int) -> str:
    octave = pitch // 12 - 1
    note = NOTE_NAMES[pitch%12]
    return f"{note}{octave}"