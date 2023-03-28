class _Feature():
    _func_msg = """
    The parameter `func` must be a function that operates on a data set. 
    """
    _in_msg = """
    The parameter `inppath` requires either a string or a list of strings for the 
    name of your data sets.
    """
    _out_msg = """
    The parameter `outpath` requires either a string or a list of strings for the 
    name of your data sets.
    """
    _param_msg = """
    The parameter `func_params` should be a dictionary containing argument names
    and values as key/value pairs. 
    """
    _step_msg = """
    The parameter `step_params` should be a dictionary containing the recipe 
    parameter name and value as key/value pairs. 
    """
    def __init__(self, func, inppath = None, outpath = None, func_params = None, step_params = None):
        if not callable(func):
            raise Exception(self._func_msg)
        if type(inppath) != list and type(inppath) != str and inppath != None:
            raise Exception(self._in_msg)
        if type(outpath) != list and type(outpath) != str and outpath != None:
            raise Exception(self._out_msg)
        if func_params == None:
            func_params = {}
        if type(func_params) != dict:
            raise Exception(self._param_msg)
        if step_params == None:
            step_params = {}
        if type(step_params) != dict:
            raise Exception(self._step_msg)
        self.function = func
        self.inppath = inppath
        self.outpath = outpath
        self.function_params = func_params
        self.step_params = step_params
        # I also want names and descriptions. The default values being the name
        # of the function input if possible. 
    

class _Check():
    _func_msg = """
    The parameter `func` must be a function that operates on a data set. 
    """
    _data_msg = """
    The parameter `data` requires either a string or a list of strings for the 
    name of your data sets.
    """
    _ex_msg = """
    The parameter `ex_msg` must be a string or list of strings, or else must be
    absent. 
    """
    _mod_msg = """
    The parameter `modify_step` should be a nested dictionary. The first level
    of the dictionary should be the name of the step to be executed and the 
    second level should be the parameter name and value to be replaced specifically
    for that step. 
    """
    _check_msg = """
    The parameter `step_params` should be a dictionary containing the parameter
    name and value as key/value pairs. 
    """
    def __init__(self, func, exclude_step = None, modify_step = None, check_params = None):
        if not callable(func):
            raise Exception(self._func_msg)
        # if type(inppath) != list and type(inppath) != str:
        #     raise Exception(self._data_msg)
        if type(exclude_step) == str:
            exclude_step = [exclude_step]
        if exclude_step == None:
            exclude_step = []
        if type(exclude_step) != list:
            raise Exception(self._ex_msg)
        if modify_step == None:
            modify_step = {}
        if type(modify_step) != dict:
            raise Exception(self._mod_msg)
        if check_params == None:
            check_params = {}
        if type(check_params) != dict and check_params != None:
            raise Exception(self._check_msg)
        self.function = func
        # self.inppath = inppath
        self.exclude_step = exclude_step
        self.modify_step = modify_step
        self.check_params = check_params
        