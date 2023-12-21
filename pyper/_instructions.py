import pandas as pd
from ._pieces import _Feature, _Check
import pdb


def _lst_coerce(obj):
    if type(obj) == list:
        return obj
    return [obj]

def _better_concat(lst, axis=0):
    lst = _lst_coerce(lst)
    if lst == []:
        return pd.DataFrame()
    return pd.concat(lst, axis)

class _Pipeline:
    def __init__(self):
        self.step_idx = 0
        self.steps = {}
    def add_step(self, name, feature, step_params):
        # Initialize a step object
        self.steps[self.step_idx] = _Step(name, feature, step_params)
        # self.step_idx +=1
    def add_check_to(self, name, check):
        if name not in check.exclude_step:
            if name in check.modify_step:
                check.check_params.update(check.modify_step[name])
            self.steps[self.step_idx].add_check(check)
    def run_all(self, start = 0, stop = None):
        log = []
        if stop == None: 
            stop = len(self.steps)
        for name, step in list(self.steps.items())[start:stop]:
            step.run()
            result = step.run_all_checks()
            if len(result) > 0:
                log.append(result)
        return _better_concat(log,0)

class _Step:
    def __init__(self, name, feature, step_params):
        self.name = name
        #TODO: Need to validate that aStep always has indir, outdir, read_func, and write_func.
        self.step_params = step_params
        self.feature = feature
        self.checks = [] 
    def run(self):
        dfs = []
        if len(self.feature.inppath) > 0:
            dfs = [self.step_params['read_func'](x) for x in self.feature.inppath]
        out = _lst_coerce(self.feature.function(*dfs, **self.feature.function_params))
        for i in range(0,len(self.feature.outpath)):
            self.step_params['write_func'](out[i], self.feature.outpath[i])
        #TODO: Still need map strategy, this is just blend. 
    def run_check(self, check, outpath):
        df = self.step_params['read_func'](outpath)
        return check.function(df, **check.check_params)
    def run_all_checks(self):
        results = []
        #pdb.set_trace()
        for path in self.feature.outpath:
            result = _better_concat([self.run_check(chk, path) for chk in self.checks], 1)
            context = pd.DataFrame({
                "step": [self.feature.step_params['name']]
                , "description": [self.feature.step_params['description']]
                , "outpath": path
            })
            results.append(_better_concat([context, result], 1))
        return _better_concat(results, 0)
    def add_check(self, check):
        self.checks.append(check)

# Scaffolding
# data = {
#     "raw": "/Users/christian.tillich/Repos/nmr-pyper/dont_push/raw.csv"
#     ,"val_means": "/Users/christian.tillich/Repos/nmr-pyper/dont_push/1_val_means.csv"
# }

# step_params = {
#     "indir": "/Users/christian.tillich/Repos/nmr-pyper/dont_push/"
#     ,"outdir": "/Users/christian.tillich/Repos/nmr-pyper/dont_push/"
#     ,"read_func": pd.read_csv
#     ,"write_func": (lambda df, path: df.to_csv(path))
# }

# func = lambda x: x.groupby('parent_brand')['Value Rating'].mean().reset_index()
# chk1 = lambda x: pd.DataFrame({"nrow": [len(x)]}) 
# chk2 = lambda x: x.dtypes.to_frame('type').value_counts().to_frame().transpose()
# feat = _Feature(func, inppath = data['raw'], outpath = data['val_means'])
# chks = [
#     _Check(chk1, data['val_means'])
#     ,_Check(chk2, data['val_means'])
# ]

# test = _Step('test', feat, step_params)    
# test.add_check(chks[0])  
# test.add_check(chks[1])