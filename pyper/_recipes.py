import pandas as pd
import os.path as fp
from ._pieces import _Feature, _Check
from ._instructions import _Pipeline, _Step
from copy import deepcopy

_def_read = pd.read_csv
_def_write = (lambda df, path: df.to_csv(path, index = False))

#New instantiation is saving previous data. 
class Recipe:
    def __init__(self, default_dir, read_func = _def_read, write_func = _def_write, ext = ".csv", data = {}):
        self.data = {}
        self.data.update(data)
        #self.pipeline = _Pipeline()
        self.features = []
        self.checks = []
        self.step_params = {
            "read_func": read_func
            ,"write_func": write_func
            ,"inpdir": default_dir
            ,"outdir": default_dir
            ,"ext": ext
            ,"description": "I don't have a description, please add one."
            ,"strategy": "blend"
        }

    def show_data(self):
        return self.data

    def read(self, data_name):
        self.step_params['read_func'](self.data[data_name])
    
    def _assign_data(self, name, path):
        overwrite_msg = (
            "Data set " + name + " was already added in previous step. Please " +
            "choose a different name."
        )
        if self.data.get(name) != None:
            raise Exception(overwrite_msg)
        self.data[name] = path

    def _split_step_params(self, dct):
        valid = list(self.step_params.keys())
        valid.append('name')
        steps = {x:dct[x] for x in dct if x in valid}
        func = {x:dct[x] for x in dct if x not in valid}
        return steps, func

    def add_feature(self, func, inp = None, out = None, strategy = "blend", **params):
        step_params, func_params = self._split_step_params(params)
        step_params['name'] = func.__name__
        defaults = deepcopy(self.step_params)
        defaults.update(step_params)
        step_params = defaults

        if type(inp) == str:
            inp = [inp]
        if type(inp) != list and inp != None:
            raise Exception("Parameter `inp` must be a string or list of strings.")
        if type(out) == str:
            out = [out]
        if type(out) != list and out != None:
            raise Exception("Parameter `out` must be a string or list of strings.")
        
        #Check that the input data set currently exists in recipe.data. Else, 
        #construct the path based on all known info and try to access it. If 
        #file is successfully read, add to recipe.data. 
        if inp != None:
            for i in inp:
                if self.data.get(i) != None:
                    inppath = self.data[i]
                else:
                    name = i + step_params['ext']
                    path = fp.join(step_params['inpdir'], name)
                    try:
                        step_params['read_func'](path)
                    except:
                        raise Exception("File " + path + " does not exist.")
                    self._assign_data(inp, path)
            inppaths = [self.data.get(i) for i in inp]
        else:
            inppaths = []

        #Tick the added feature count by 1. Construct the name of the output data
        #set, adding the feature index to the front of the name. Construct the 
        #full path, assign the data set reference to recipe.data. 
        idx = len(self.features) + 1
        if out != None:
            for o in out:
                name = str(idx) + "_" + o + step_params['ext']
                path = fp.join(step_params['outdir'], name)
                self._assign_data(o, path)
            outpaths = [self.data.get(o) for o in out]
        else:
            outpaths = []

        #Create the feature
        aFeature = _Feature(func, inppaths, outpaths, func_params, step_params)
        self.features.append(aFeature)
        return self

    def add_check(self, func, exclude_step = None, modify_step = None, **params):
        step_params, check_params = self._split_step_params(params)
        aCheck = _Check(func, exclude_step, modify_step, check_params)
        self.checks.append(aCheck)
        return self

    def _prepare(self):
        aPipeline = _Pipeline()
        for feat in self.features:
            params = deepcopy(feat.step_params)
            stepname = params.pop('name')
            aPipeline.add_step(stepname, feat, params)
            for chk in self.checks:
                aPipeline.add_check_to(stepname, chk)
            aPipeline.step_idx += 1
        return aPipeline
    #def plan(self):
        # Run _prepare. 
        # Format prepare results as DataFrame
        # Return DataFrame plan

    def run(self, start = 0, stop = None):
        aPipeline = self._prepare()
        log = aPipeline.run_all(start = start, stop = stop)
        logname = 'log' + self.step_params['ext']
        logpath = fp.join(self.step_params['outdir'],logname)
        if type(log) == pd.DataFrame:
            self.step_params['write_func'](log, logpath)
        return(log)
