import os
import json
import numpy

# global variable
script_path = os.path.dirname(os.path.abspath(__file__))


def save_customlist(customlist):
    """
    Save custom fitting function dictionary in a txt file customFit.txt

    Parameters
    ----------

    customlist : dict
        dict of custom fitting functions.
        Ex : {'funcName':'lambda x, a, b : a*x+b ; (1, 0.1)'}

    """
    with open(os.path.join(script_path, 'customFit.txt'), 'w') as fid:
        json.dump(customlist, fid, indent=2, sort_keys=True)


def get_func(strfunc=None, typefunc=None):
    """
    Returns a string or a dict of custom fitting functions

    Parameters
    ----------

    strfunc : str, optional
        Must correspond to the name (in dict.keys) of a function : if given,
        returns the corresponding string function.
        Default: None
    typefunc : str, optional
        Possible values: linear, power or custom. If provided, returns the
        dictionary of the corresponding type of functions.
        Default: None

    Returns
    ----------
    str or dict

    """
    linlist = {'constant': 'lambda x, a : a ; (1)', 
               'ax': 'lambda x, a : a*x ; (1)',
               'ax+b': 'lambda x, a, b : a*x+b ; (1, 1)',
               'a(x-b)': 'lambda x, a, b : a*(x-b) ; (1, 1)'}
    powerlist = {'ax^n': 'lambda x, a, n : a*(x**n) ; (1, 1)',
                 'a+bx^n': 'lambda x, a, b, n : a+b*(x**n) ; (1, 1, 1)',
                 'a(x-b)^n': 'lambda x, a, b, n : a*((x-b)**n) ; (1, 1, 1)',
                 'a+b(x-c)^n': 'lambda x, a, b, c, n : a+b*((x-c)**n) ; (1, 1, 1, 1)'}
    explist = {'exp(x/a)': 'lambda x, a : a*numpy.exp(x/a) ; (1)', 
               'a*exp(x/b)': 'lambda x, a, b : a*numpy.exp(x/b) ; (1, 1)', 
               'a*exp(x/b) + c': 'lambda x, a, b, c : a*numpy.exp(x/b) + c ; (1, 1, 1)', 
               'a*exp((x-b)/c)': 'lambda x, a, b, c : a*numpy.exp((x-b)/c) ; (1, 1, 1)',
               'a(1-exp(-x/b))': 'lambda x, a, b : a*(1 - numpy.exp(-x/b)) ; (1, 1)'}
    custom_path = os.path.join(script_path, 'customFit.txt')
    if os.path.exists(custom_path):
        with open(custom_path, 'r') as fid:
            customlist = json.load(fid)
    else:
        customlist = {}
    funclist = {**linlist, **powerlist, **explist, **customlist}
    if strfunc is None:
        if typefunc is None:
            return funclist
        elif typefunc == 'linear':
            return linlist
        elif typefunc == 'power':
            return powerlist
        elif typefunc == 'exp':
            return explist
        elif typefunc == 'custom':
            return customlist
    else:
        return funclist[strfunc]


def from_fdef(fdef):
    """
    Returns a function and its initialising parameters' values from a string
    containing them, typically 'fdef ; (param)'

    Parameters
    ----------

    fdef : str, optional
        String of type 'fdef ; (param)'

    Returns
    ----------
    f: function
    p: tuple
        initialising parameters' values

    """
    fstr, pstr = fdef.split(';')
    return eval(fstr), eval(pstr)

def str_line(lin):
    """
    Returns a string in the form 'marker' + 'linestyle' from a 
    matplotlib.lines.line2D object

    Parameters
    ----------

    lin : matplotlib.lines.line2D object

    Returns
    ----------
    strlin: str
        string in the form 'marker' + 'linestyle'
    """
    strlin = ''
    if lin.get_marker() is not 'None':
        strlin = strlin + lin.get_marker()
    if lin.get_linestyle() is not 'None':
        strlin = strlin + lin.get_linestyle()
    return strlin

