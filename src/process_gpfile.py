import guitarpro as gp
import config
from typing import List,Dict
from utils.gp_utils import convert_pitch_to_str, convert_note_to_pitch, get_note_position


def valid_track(track: gp.Track) -> bool:
    # filter out percussion
    if track.isPercussionTrack:
        return False
    
    # filter out guitar with too many frets
    if track.fretCount> config.FRETS_NUM:
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
    correct_stringsnum = (stringsnum == config.STRINGS_NUM)

    return correct_tuning and correct_stringsnum


def process_gpfile(filepath:str) -> List[Dict]|None:
    try:
        gp_file = gp.parse(filepath)
    except Exception as e:
        print(f"Error for {filepath} : {e}")
        return None
    
    data_dicts = []
    for track in gp_file.tracks:
        if (not valid_track(track)):
            continue
        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    dict = {keys:0 for keys in config.DATACSV_HEADER}
                    total_pitches = 0
                    for i, note in enumerate(beat.notes):
                        pitch = convert_note_to_pitch(note)
                        total_pitches += pitch
                        dict[f'pitch_{i+1}'] = pitch
                        dict[f'position_{i+1}'] = get_note_position(note)

                        for a in range(config.NUM_NOTES_AFTER):
                            if len(data_dicts)>a:
                                data_dicts[-(a+1)][f'pitch+{a+1}_{i+1}'] = pitch
                    if total_pitches ==0:
                        continue
  
                    for i in range(6):
                        for b in range(config.NUM_NOTES_BEFORE):
                            dict[f'pitch-{b+1}_{i+1}'] = data_dicts[-(b+1)][f'pitch_{i+1}'] if len(data_dicts)>b else 0

                    data_dicts.append(dict)

    return data_dicts

