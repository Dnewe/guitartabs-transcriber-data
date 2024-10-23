import os
import csv
import json
import shutil
from typing import List,Dict
import config


def create_dir(dirpath:str):
    try:
        os.mkdir(dirpath)
    except Exception as e:
        print(f"Directory at path: {dirpath} already exists.")


def remove_dir(dirpath:str):
    try:
        shutil.rmtree(dirpath)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def init_csvfile(csvpath:str, header:List[str]):
    with open(csvpath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)


def write_rows_to_csv(csvpath:str, rows:List[Dict]):
    header = [key for key in rows[0].keys()]

    with open(csvpath, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerows(rows)
        csvfile.close()


def combine_csvfiles(results_csvpath, csvpath_list:List):
    init_csvfile(results_csvpath, config.DATACSV_HEADER)

    with open(results_csvpath, 'a', newline='') as result_file:
        writer = csv.writer(result_file)

        # Iterate through each CSV file in the list
        for csvpath in csvpath_list:
            with open(csvpath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                writer.writerows(reader)


def write_json(filepath:str, data:Dict) -> None:
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)