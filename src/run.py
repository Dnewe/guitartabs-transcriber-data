import os
import multiprocessing
import threading
from functools import partial
from typing import Tuple
from utils.fs_io import write_rows_to_csv, create_dir, combine_csvfiles, remove_dir
from process_gpfile import process_gpfile


def init_directories(args) -> Tuple[str,str]:
    # Create directories
    outdir = os.path.join(args.output, os.path.basename(args.input))
    create_dir(outdir)
    tempdir = os.path.join(outdir,"temp")
    create_dir(tempdir)

    return outdir, tempdir


def get_filepaths(dir):
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            filepath = subdir + os.sep + file
            yield filepath


def process_file(filepath, tempdir:str) -> None:
    if filepath[:-1].endswith('.gp'):
        data_dicts =  process_gpfile(filepath)
        datacsv_path = os.path.join(tempdir, f"datacsv_thread{threading.get_ident()}.csv")
        reportcsv_path = os.path.join(tempdir, f"reportcsv_thread{threading.get_ident()}.csv")
        write_rows_to_csv(reportcsv_path, [{'filepath':filepath, 'sucess':1 if data_dicts is not None else 0}])
        if data_dicts is not None and len(data_dicts)>0:
            write_rows_to_csv(datacsv_path, data_dicts)
        


def process_files_in_parallel(dir, tempdir:str) -> None:
    filepaths= get_filepaths(dir)
    partial_process_file = partial(process_file, tempdir=tempdir)
    with multiprocessing.Pool() as pool:
        pool.map(partial_process_file, filepaths)


def process_files(dir, tempdir:str) -> None:
    for subdir, dirs, files in os.walk(dir): 
            for file in files:
                filepath:str = subdir + os.sep + file
                process_file(filepath, tempdir)


def run(args):
    print("Creating files and directories")
    outdir, tempdir = init_directories(args)

    print(f"Processing files (multiproc={args.multiproc})")
    if args.multiproc:
        process_files_in_parallel(args.input, tempdir)
    else:
        process_files(args.input, tempdir)
    
    print("Combining temporary CSV files")
    datacsv_path = os.path.join(outdir,f"data_{os.path.basename(args.input)}.csv")
    reportcsv_path = os.path.join(outdir, f"report_{os.path.basename(args.input)}.csv") if args.report else None

    combine_csvfiles(datacsv_path, [os.path.join(tempdir,csvname) for csvname in os.listdir(tempdir) if csvname.startswith("data")])
    if args.report:
        combine_csvfiles(reportcsv_path, [os.path.join(tempdir,csvname) for csvname in os.listdir(tempdir) if csvname.startswith("report")])
    
    print("Removing temporary files")
    remove_dir(tempdir)