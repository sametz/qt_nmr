"""Converts parameters sent by the view to parameters that can be used by the
Model.
"""

def parse_posargs(params):
    """
    Converts params to a list of numeric arguments for the model_name, IF the
    following conditions are met:
    * dicts are the new ordered-by-default
    * arguments are listed in settings.py dicts in same order as position of
      arguments in the model_name's corresponding function

    :param params: {str: float...}
        for {name of variable: value...}
    :return: [float...]
        a list of numerical positional arguments
    """
    return [val for val in params.values()]


def parse_ab(params):
    args = [params[var] for var in ['Jab', 'Vab', 'Vcentr']]
    return args


def parse_ab2(params):
    # A separate function in case ab and ab2 parameters/model_name ever diverge
    return parse_ab(params)


def parse_abx(params):
    pass


def parse_abx3(params):
    pass


def parse_aaxx(params):
    pass


def parse_aabb(params):
    pass


def parse_first_order(params):
    pass


def parse_second_order(params):
    pass


def parse_dnmr_two_singlets(params):
    pass


def parse_dnmr_ab(params):
    pass


class Adapter:
    def __init__(self):
        pass

def view_to_model(model, params):
    adapters = {
        'AB': parse_ab,
        'AB2': parse_ab2,
        'ABX': parse_abx,
        'ABX3': parse_abx3,
        'AAXX': parse_aaxx,
        'AABB': parse_aabb,
        'first_order': parse_first_order,
        'second_order': parse_second_order,
        'dnmr_two_singlets': parse_dnmr_two_singlets,
        'dnmr_ab': parse_dnmr_ab
    }
    if model not in adapters:
        print('No adapter for model_name found')
        return None
    else:
        # return adapters[model_name](params)
        return parse_posargs(params)






    def _parse_multiplet(self):
        pass

    def _parse_abc(self):
        pass

    def _parse_dnmr(self):
        pass


