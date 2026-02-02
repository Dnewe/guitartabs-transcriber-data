import guitarpro as gp
import config
from typing import List,Dict,Tuple
from utils.gp_utils import convert_pitch_to_str, convert_note_to_pitch, pitch_to_note_octave


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

class GPFile:
    gp_file: gp.Song|None = None
    data_dicts: List[Dict]

    # trim data
    skipped: List
    string_distr = [[0 for _ in range(config.STRINGS)] for note in range(config.STRINGS)]
    fret_distr = [[0 for _ in range(config.FRETS+1)] for note in range(config.STRINGS)]

    def __init__(self, path) -> None:
        try:
            self.data_dicts = []
            self.skipped = []
            self.gp_file = gp.parse(path)
        except Exception as e:
            print(f"Error for {path} : {e}")
            return None

    def skip_beat(self, strings, frets) -> bool:
        exceeds_strdistr = False
        exceeds_fretdistr = False
        for i in range(len(strings)):
            if frets[i]>config.FRETS:
                return True
            # skip if string exceeds distr limit
            if sum(self.string_distr[i])>1000 : exceeds_strdistr = exceeds_strdistr or ((self.string_distr[i][strings[i]-1] / sum(self.string_distr[i])) > config.MAX_STRING_DISTR)
            # skip if fret exceeds distr limit
            if sum(self.fret_distr[i])>1000 : exceeds_fretdistr = exceeds_fretdistr or ((self.fret_distr[i][frets[i]] / sum(self.fret_distr[i])) > config.MAX_FRET_DISTR) 
        
        return exceeds_strdistr or exceeds_fretdistr

    def add_to_distr(self, strings, frets):
        for i in range(len(strings)):
            self.string_distr[i][strings[i]-1] +=1
            self.fret_distr[i][frets[i]] +=1


    def to_dict(self) -> None:
        if self.gp_file is None:
            return None

        self.skipped = []
        for track in self.gp_file.tracks:
            if (not valid_track(track)):
                continue
            for measure in track.measures:
                for voice in measure.voices:
                    for beat in voice.beats:
                        dict = {keys:0 for keys in config.DATACSV_HEADER}
                        strings = []
                        frets = []
                        total_pitches = 0
                        duration = beat.duration.value
                        for i, note in enumerate(beat.notes):
                            pitch = convert_note_to_pitch(note)
                            total_pitches += pitch
                            notenum, octave = pitch_to_note_octave(pitch)
                            #duration = round(note.durationPercent*100)
                            # effects
                            #letring = 1 if note.effect.letRing else 0
                            isharmonic = 1 if note.effect.isHarmonic else 0
                            string = note.string

                            dict[f'x_note_{i+1}'] = notenum
                            dict[f'x_octave_{i+1}'] = octave
                            dict[f'x_duration_{i+1}'] = duration
                            dict[f'x_isharmonic_{i+1}'] = isharmonic
                            dict[f'y_string_{string}'] = 1
                            dict[f'fret'] = note.value

                            # keep info (string & fret) to know if skip needed
                            strings.append(string)
                            frets.append(note.value)

                            # add note info to next beats
                            for a in range(config.BEATS_AFTER):
                                if len(self.data_dicts)>a:
                                    self.data_dicts[-(a+1)][f'x_note+{a+1}_{i+1}'] = notenum
                                    self.data_dicts[-(a+1)][f'x_octave+{a+1}_{i+1}'] = octave
                                    self.data_dicts[-(a+1)][f'x_duration+{a+1}_{i+1}'] = duration
                        if total_pitches ==0:
                            continue
    
                        for i in range(6):
                            for b in range(config.BEATS_BEFORE):
                                dict[f'x_note-{b+1}_{i+1}'] = self.data_dicts[-(b+1)][f'x_note_{i+1}'] if len(self.data_dicts)>b else 0
                                dict[f'x_octave-{b+1}_{i+1}'] = self.data_dicts[-(b+1)][f'x_octave_{i+1}'] if len(self.data_dicts)>b else 0
                                dict[f'x_duration-{b+1}_{i+1}'] = self.data_dicts[-(b+1)][f'x_duration_{i+1}'] if len(self.data_dicts)>b else 0
                        
                        if not self.skip_beat(strings, frets):
                            self.add_to_distr(strings, frets)
                        else:
                            self.skipped.append(dict)
                        self.data_dicts.append(dict)

    def trim(self):
        for i in self.skipped:
            self.data_dicts.remove(i)

    def process(self) -> List[Dict]:
        self.data_dicts = []
        self.to_dict()
        self.trim()
        return self.data_dicts

