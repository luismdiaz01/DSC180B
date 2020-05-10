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
from analyze_crimes import analyze

# Global constants
DATA_PARAMS = 'config/data-params.json'
PROCESS_PARAMS = 'config/process-params.json'
TEST_PROCESS_PARAMS = 'config/test-process-params.json'
EDA_CRIMES_PARAMS = 'config/eda-crimes-params.json'
TEST_EDA_CRIMES_PARAMS = 'config/test-eda-crimes-params.json'
EDA_STOPS_PARAMS = 'config/eda-stops-params.json'
TEST_EDA_STOPS_PARAMS = 'config/test-eda-stops-params.json'
EDA_ARRESTS_PARAMS = 'config/eda-arrests-params.json'
TEST_EDA_ARRESTS_PARAMS = 'config/test-eda-arrests-params.json'
ANALYZE_CRIMES_PARAMS = 'config/analyze-crimes-params.json'

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
        shutil.rmtree('data/raw', ignore_errors=True)
        shutil.rmtree('data/cleaned', ignore_errors=True)
        shutil.rmtree('viz', ignore_errors=True)
        
    if 'clean-test' in targets:
        shutil.rmtree('test_data/cleaned', ignore_errors=True)
        shutil.rmtree('viz', ignore_errors=True)

    # make the data target
    if 'data' in targets:
        cfg = load_params(DATA_PARAMS)
        get_data(**cfg)
        
    if 'process' in targets:
        cfg = load_params(PROCESS_PARAMS)
        process(**cfg)        

    if 'eda' in targets:
        if not os.path.exists('viz/EDA'):
            os.mkdir('viz/EDA')
        
        cfg_stops = load_params(EDA_STOPS_PARAMS)    
        cfg_crimes = load_params(EDA_CRIMES_PARAMS)
        cfg_arrests = load_params(EDA_ARRESTS_PARAMS)
        
        gv_stops(**cfg_stops)
        gv_crimes(**cfg_crimes)
        gv_arrests(**cfg_arrests)
        
    if 'analyze' in targets:
        if not os.path.exists('viz/Analysis'):
            os.mkdir('viz/Analysis')
            
        cfg_crimes = load_params(ANALYZE_CRIMES_PARAMS)
        
        analyze(**cfg_crimes)
    
    if 'test' in targets:
        process_cfg = load_params(TEST_PROCESS_PARAMS)
        process(**process_cfg)
        if not os.path.exists('viz/EDA'):
            os.mkdir('viz/EDA')
            
        if not os.path.exists('viz/Analysis'):
            os.mkdir('viz/Analysis')
        
        cfg_stops = load_params(TEST_EDA_STOPS_PARAMS)    
        cfg_crimes = load_params(TEST_EDA_CRIMES_PARAMS)
        cfg_arrests = load_params(TEST_EDA_ARRESTS_PARAMS)
        
        gv_stops(**cfg_stops)
        gv_crimes(**cfg_crimes)
        gv_arrests(**cfg_arrests)
    
    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)