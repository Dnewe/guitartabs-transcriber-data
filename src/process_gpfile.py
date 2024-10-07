import guitarpro as gp
import config
from typing import List,Dict
from utils.gp_utils import convert_pitch_to_str, convert_note_to_pitch


def valid_track(track: gp.Track) -> bool:
    # filter out percussion
    if track.isPercussionTrack:
        return False
    
    # count strings and determine tuning
    stringsnum = 0
    tuning = []
    for string in track.strings:
        stringsnum += 1
        tuning.append(string.value)
   
    # check tuning / number of strings according to config
    correct_tuning = (config.REQUIRED_TUNING == [convert_pitch_to_str(pitch) for pitch in tuning][::-1])
    correct_stringsnum = (stringsnum == config.REQUIRED_STRINGSNUM)

    return correct_tuning and correct_stringsnum


def process_gpfile(filepath:str) -> List[Dict]|None:
    try:
        gp_file = gp.parse(filepath)
    except Exception as e:
        print(f"Error for {filepath} : {e}")
        return None
    
    data_dicts = []
    num = 0
    for track in gp_file.tracks:
        if (not valid_track(track)):
            continue
        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    dict = {keys:[] for keys in config.DATACSV_HEADER}
                    for note in beat.notes:
                        num +=1
                        dict['strings'].append(note.string)
                        dict['frets'].append(note.value)
                        dict['pitches'].append(convert_note_to_pitch(note))    

                    dict['pitches-1'].extend(data_dicts[-1]['pitches'].copy()) if len(data_dicts)>0 else None
                    dict['pitches-2'].extend(data_dicts[-2]['pitches'].copy()) if len(data_dicts)>1 else None
                    data_dicts[-1]['pitches+1'].extend(dict['pitches'].copy()) if len(data_dicts)>0 else None
                    data_dicts[-2]['pitches+2'].extend(dict['pitches'].copy()) if len(data_dicts)>1 else None

                    data_dicts.append(dict)

    return data_dicts

