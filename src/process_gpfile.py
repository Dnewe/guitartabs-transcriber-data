import guitarpro as gp
import config
from typing import List,Dict
from utils.gp_utils import convert_pitch_to_str, convert_note_to_pitch, get_noteposition, pitch_to_note_octave


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

    return correct_tuning and correct_stringsnum


position_distribution = [[0 for pos in range(config.POSITIONS)] for string in range(6)]
string_distribution = [[0 for str in range(config.STRINGS)] for string in range(6)]

def skip_beat(i, position, string) -> bool:
    # skip if position exceeds distribution limit
    exceeds_posdistr = ((position_distribution[i][position-1] / sum(position_distribution[i])) > config.MAX_POSITION_DISTR) if sum(position_distribution[i])>1000 else False
    #exceeds_posdistr = False
    exceeds_strdistr = ((string_distribution[i][string-1] / sum(string_distribution[i])) > config.MAX_STRING_DISTR) if sum(string_distribution[i])>1000 else False
    # skip if position is different than 1
    #diff_pos = position != 1
    
    return exceeds_posdistr or exceeds_strdistr


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
                    skip = False
                    for i, note in enumerate(beat.notes):
                        pitch = convert_note_to_pitch(note)
                        total_pitches += pitch
                        notenum, octave = pitch_to_note_octave(pitch)
                        string = note.string
                        position = get_noteposition(note)
                        dict[f'x_note_{i+1}'] = notenum
                        dict[f'x_octave_{i+1}'] = octave
                        dict[f'y_position_{i+1}'] = position
                        dict[f'y_string_{i+1}'] = string

                        skip = skip_beat(i, position, string)
                        position_distribution[i][position-1] +=1 if not skip else 0

                        for a in range(config.BEATS_AFTER):
                            if len(data_dicts)>a:
                                data_dicts[-(a+1)][f'x_note+{a+1}_{i+1}'] = notenum
                                data_dicts[-(a+1)][f'x_octave+{a+1}_{i+1}'] = octave
                    if total_pitches ==0:
                        continue
  
                    for i in range(6):
                        for b in range(config.BEATS_BEFORE):
                            dict[f'x_note-{b+1}_{i+1}'] = data_dicts[-(b+1)][f'x_note_{i+1}'] if len(data_dicts)>b else 0
                            dict[f'x_octave-{b+1}_{i+1}'] = data_dicts[-(b+1)][f'x_octave_{i+1}'] if len(data_dicts)>b else 0

                    if not skip:
                        data_dicts.append(dict)

    return data_dicts

