'''
    Linear regression parameters for all models 
    file not executable, dictionaries meant to be imported and used for
    future calculations
'''
pymc3_params = dict({
    'POTATO': {
        'pressure_mean': -0.01, 
        'temp_max': -0.005, 
        'intercept': 0.68
    },
    'CITRUS': {
        'rain_mean': -0.04, 
        'pressure_mean': 0.08, 
        'rain_var': -0.01, 
        'intercept': 0.51
    },
    'PEAS': {
        'temp_min': -0.28,
        'temp_max': 0.30, 
        'intercept': 0.76
    }

})

lr_params = dict({
    'POTATO': {
        'pressure_mean': -0.0055, 
        'temp_max': 0.0083, 
        'intercept': 0.6375
    },
    'CITRUS': {
        'rain_mean': -0.0155, 
        'pressure_mean': 0.0326, 
        'rain_var': -0.0076, 
        'intercept': 0.4809 
    },
    'PEAS': {
        'temp_min': -0.0110,
        'temp_max': 0.0074, 
        'intercept': 0.4806
    }

})

ridge_params = dict({
    'POTATO': {
        'pressure_mean': -0.0001, 
        'temp_max': 0.0002,  
        'intercept': 0.6423
    },
    'CITRUS': {
        'rain_mean': -0.0009, 
        'pressure_mean': 0.0009, 
        'rain_var': -0.0001, 
        'intercept': 0.4677 
    },
    'PEAS': {
        'temp_min': -0.0005,
        'temp_max': 0.0074, 
        'intercept': 0.4673
    }

})