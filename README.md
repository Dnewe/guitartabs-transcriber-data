# Guitar Tabs Transcriber Training

## Project Overview

**Guitar Tabs Transcriber** is a personal project I worked on in 2024. with the aim to write a deep learning model that converts guitar musics to guitar tablatures[^1].

The main goal was to build a model and a training pipeline from scratch without ML framework, **using only NumpPy**. To understand **neural networks** and **backpropagation** on a deeper level.

[^1]: Tablature (or tab for short) is a form of musical notation indicating instrument fingering or the location of the played notes rather than musical pitches.

## Data

### Input
Data must be in format GuitarPro (*.gtp, *.gp2, *.gp3, *.gp4, *.gp5).

### Output
- **data.csv**: CSV files containing processed features.
- **metadata.json**: JSON file containing parameters used and data CSV header format (needs rework).
- **report.csv**: If report is enabled, CSV file mapping filepaths to whether it has been successfully processed or not.

### Pipeline

**Cleaning:**
The GuitarPro files are filtered to match user [filter parameters](#cleaning-parameters).\
This is necessary because for the model to learn, data must stay consistent (eg. same guitar tuning for all features).

**Normalization:**
To prevent class imbalance, to [distribution parameters](#normalization-parameters).\
This is useful because guitar musics is often similar, using low frets, making the model unable to learn complex tabs.\
This is a naive approach which needs rework.

**Features:**
The data is transformed into features that contain information on the beat[^2] to predict, previous and future beats[^2] and the fret value to predict of the beat[^2].\ 
The specific format is defined in the [parameters](#featureformat-parameters).

The processed data is then stored on a CSV file.

[^2]: The beat is the basic unit of time. Each beats can have multiple notes, a single note or no note.


> [!NOTE]
> Only the fret value is used as the target because the string number can be computed using the input pitch and the fret number.

#### Parameters
<a name="cleaning-parameters"></a>
**Filter parameters:**
- **TUNING** *(List[str])*: Filters out guitar tracks with different tuning. (Default= ['E2', 'A2', 'D3', 'G3', 'B3', 'E4'])
- **STRINGS** *(int)*: Filters out guitar tracks with different number of strings. (Default= 6)
- **FRETS** *(int)*: Filters out features using higher frets (FRETS>=24: all frets). (Default= 24)
- **CAPO** *(int)*: Filters out guitar tracks with different capo (CAPO=0: no capo). (Default= 0)

<a name="normalization-parameters"></a>
**Normalization parameters:**
- **MAX_STRING_DISTR** *(int)*: Represents the maximum distribution of used strings in the processed data. (Default= 0.25)
- **MAX_FRET_DISTR** *(int)*: Represents the maximum distribution of used frets in the processed data. (Default= 0.2)

<a name="featureformat-parameters"></a>
**Features format:**
- **BEATS_BEFORE** *(int)*: Represents the number of beats (with GT) before each beat to predict. (Default= 7) 
- **BEATS_BEFORE** *(int)*: Represents the number of beats (with GT) after each beat to predict. (Default= 7)  

**Others:**
- **TEST_DATA** *(bool)*: If true, deactivates normalization (max distribution on strings and frets).


## Training

Training pipeline at [guitartabs-transcriber-training](https://github.com/Dnewe/guitartabs-transcriber-training).


## Install

Library requirements in *requirement.txt*.

```
python -m venv .venv
pip install -r requirements.txt
```

## Run

**Command**:
```powershell
python src/main.py --input <input_dir> --output <output_dir> --multiproc --report
```

**Arguments:**
- **--input (-i)** <*input_dir*>: Path to the directory where guitar pro files are located (can have subdirs).
- **--output (-o)** <*output_dir*>: Path to the directory where data, metadata and report will be written.
- **--multiproc (-m)** *(optional)*: if specified, will use multiprocessing to process GP files.
- **--report (-r)** *(optional)*: if specified will produce a report of processed files.

**Example:**
```powershell
python src/main.py -i "data/input" -o "data/output" -m -r
```

