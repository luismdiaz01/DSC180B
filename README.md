# DSC180B
Exploring Predictive Policing in San Diego for DSC180B capstone project

## Usage Instructions

* Description of targets and using `run.py`

Links to the GIS map can be found at https://arcg.is/1CmX0r

## Description of Contents

The project consists of these portions:
```
PROJECT
├── .gitignore
├── README.md
├── config
│   ├── data-params.json
│   └── test-params.json
│   └── .env
├── data
│   ├── raw
│   └── cleaned
├── test_data
│   ├── raw
│   └── cleaned
├── notebooks
│   └── .gitkeep
├── references
│   └── .gitkeep
├── requirements.txt
├── run.py
└── src
    └── etl.py
```

### `src`

* `etl.py`: Library code that executes tasks useful for getting data.

### `config`

* `data-params.json`: Common parameters for getting data, serving as
  inputs to library code.
  
* `test-params.json`: parameters for running small process on small
  test data.

### `references`

* Data Dictionaries, references to external sources
- Dictionary for nhgis table

### `notebooks`

* Jupyter notebooks for *analyses*
  - notebooks are not for data processing; they should imp
