import guitarpro as gp
import config
from utils.gp_utils import convert_MIDIpitch


def check_track_validity(track: gp.Track) -> bool:
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
    correct_tuning = (config.REQUIRED_TUNING == [convert_MIDIpitch(pitch) for pitch in tuning][::-1])
    correct_stringsnum = (stringsnum == config.REQUIRED_STRINGSNUM)

    return correct_tuning and correct_stringsnum