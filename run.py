# Import modules/libraries
import sys
import json
import shutil
import os

sys.path.insert(0, 'src') # add library code to path
from etl import get_data, process
from EDA_crimes import generate_viz as gv_crimes
from EDA_stops import generate_viz as gv_stops
from EDA_arrests import generate_viz as gv_arrests

# Global constants
DATA_PARAMS = 'config/data-params.json'
#TEST_PARAMS = 'config/test-params.json'
PROCESS_PARAMS = 'config/process-params.json'
#TEST_PROCESS_PARAMS = 'config/test-process-params.json'
EDA_CRIMES_PARAMS = 'config/eda-crimes-params.json'
EDA_STOPS_PARAMS = 'config/eda-stops-params.json'
EDA_ARRESTS_PARAMS = 'config/eda-arrests-params.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)

    return param


def main(targets):
    if not os.path.exists('data/'):
        os.mkdir('data/')
    if not os.path.exists('viz/'):
        os.mkdir('viz/')
        
    # make the clean target
    if 'clean' in targets:
        os.unlink('data/raw')
        os.unlink('data/cleaned')
        os.unlink('data/temp')      
        os.unlink('data/out')     
        os.unlink('data/test')

    # make the data target
    if 'data' in targets:
        cfg = load_params(DATA_PARAMS)
        get_data(**cfg)

    # make the test target
#    if 'data-test' in targets:
#        cfg = load_params(TEST_PARAMS)
#        get_data(**cfg)
        
    if 'process' in targets:
        cfg = load_params(PROCESS_PARAMS)
        process(**cfg)
        
#    if 'process-test' in targets:
#        cfg = load_params(TEST_PROCESS_PARAMS)
#        process(**cfg)
        
#    if 'test-project' in targets:
#        cfg = load_params(TEST_PARAMS)
#        get_data(**cfg)    
#        cfg = load_params(TEST_PROCESS_PARAMS)
#        process(**cfg)

    if 'eda' in targets:
        if not os.path.exists('viz/EDA'):
            os.mkdir('viz/EDA')
        
        cfg_stops = load_params(EDA_STOPS_PARAMS)    
        cfg_crimes = load_params(EDA_CRIMES_PARAMS)
        cfg_arrests = load_params(EDA_ARRESTS_PARAMS)
        
        gv_stops(**cfg_stops)
        gv_crimes(**cfg_crimes)
        gv_arrests(**cfg_arrests)
        
    if 'eda_arrests' in targets:
        if not os.path.exists('viz/EDA'):
            os.mkdir('viz/EDA')

        cfg_arrests = load_params(EDA_ARRESTS_PARAMS)
        gv_arrests(**cfg_arrests)
        
    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)