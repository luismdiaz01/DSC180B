# DSC180B
Exploring Predictive Policing in San Diego for DSC180B Capstone Project

Link to the GIS map can be found at https://arcg.is/1CmX0r

## Usage Instructions

To replicate the entire (or subsets of the) project, copy and paste `python run.py` in the command line while in the root directory followed by the arguments below:
* `data`: Ingests raw data from online sources.
* `process`: Runs the pipeline for cleaning and formatting raw datasets.
* `eda`: Performs exploratory data analysis and outputs visualizations.
* `analyze`: Performs statistical tests on differences in observed proportions between PredPol and non-PredPol instances.
* `test-project`: Runs the entire pipeline from start to end on a smaller, versioned test data.

For example, running the code below would reproduce the entire project:

`python run.py data process eda analyze`

## Description of Contents

The project consists of these portions:
```
PROJECT
├── config
│   ├── data-params.json
│   └── process-params.json
│   └── eda-params.json
│   └── analyze-params.json
│   └── test-data-params.json
│   └── test-process-params.json
│   └── test-eda-params.json
│   └── test-analyze-params.json
│   └── env.json
├── data
│   ├── raw
│   └── cleaned
├── notebooks
│   └── .gitkeep
├── references
│   └── arrest_charges.json
│   └── arrest_types.json
│   └── crime_charges.json
│   └── crime_types.json
│   └── divisions_mapper.json
│   └── nhgis0005_ds172_2010_block_codebook.txt
│   └── races.json
└── src
    └── etl.py
├── test_data
│   ├── raw
│   └── cleaned
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
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
