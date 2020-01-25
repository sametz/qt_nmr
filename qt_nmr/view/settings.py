ABdict = {'Jab': 12.0,
          'Vab': 15.0,
          'Vcentr': 150.0}

AB2dict = {'Jab': 12.0,
           'Vab': 15.0,
           'Vcentr': 150.0}

ABXdict = {'Jab': 12.0,
           'Jax': 2.0,
           'Jbx': 8.0,
           'Vab': 15.0,
           'Vcentr': 7.5}

ABX3dict = {'Jab': -12.0,
            'Jax': 7.0,
            'Jbx': 7.0,
            'Vab': 14.0,
            'Vcentr': 150}

AAXXdict = {"Jaa": 15.0,
            "Jxx": -10.0,
            "Jax": 40.0,
            "Jax_prime": 6.0,
            'Vcentr': 150}

AABBdict = {"Vab": 40,
            "Jaa": 15.0,
            "Jbb": -10.0,
            "Jab": 40.0,
            "Jab_prime": 6.0,
            'Vcentr': 150}

firstorder_dict = {
    'JAX': 7.00,
     '#A': 2,
     'JBX': 3.00,
     '#B': 1,
     'JCX': 2.00,
     '#C': 0,
     'JDX': 7.00,
     '#D': 0,
     'Vcentr': 150.00
}


view_defaults = {
    'multiplet': {
        'AB': ABdict,
        'AB2': AB2dict,
        'ABX': ABXdict,
        'ABX3': ABX3dict,
        'AAXX': AAXXdict,
        '1stOrd': firstorder_dict,
        'AABB': AABBdict
    },
    'nspin': {},
    'dnmr': {}
}