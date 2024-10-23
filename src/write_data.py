import os
import config
from utils.fs_io import combine_csvfiles, remove_dir, write_json


def combine_data(outdir: str, tempdir: str):
    datacsv_path = os.path.join(outdir,f"data.csv")
    combine_csvfiles(datacsv_path, [os.path.join(tempdir,csvname) for csvname in os.listdir(tempdir) if csvname.startswith("data")])


def combine_report(outdir: str, tempdir: str):
    reportcsv_path = os.path.join(outdir, f"report.csv")
    combine_csvfiles(reportcsv_path, [os.path.join(tempdir,csvname) for csvname in os.listdir(tempdir) if csvname.startswith("report")])


def write_metadata(outdir:str):
    metadata = {'tuning': config.TUNING,
                'strings': config.STRINGS,
                'frets': config.FRETS,
                'max_pos': config.MAX_POSITION,
                'capo': config.CAPO,
                'notes_before': config.NUM_NOTES_BEFORE,
                'notes_after': config.NUM_NOTES_AFTER,
                'max_pos_distr':config.MAX_POSITION_DISTR,
                'max_str_distr':config.MAX_STRING_DISTR}
    write_json(os.path.join(outdir, 'metadata.json'), metadata)


def write_data(outdir: str, tempdir: str, write_report:bool = True) -> None:
    
    print("Combining temporary data CSV files..")
    combine_data(outdir, tempdir)
    if write_report:
        print("Combining temporary report CSV files..")
        combine_report(outdir, tempdir)
    
    print("Writing metadata JSON file..")
    write_metadata(outdir)
    
    print("Removing temporary files")
    remove_dir(tempdir)