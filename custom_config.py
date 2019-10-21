from modules.config.global_config import *

# store all variables from global config
context_vars = vars()

# utils variables
experiment_list = [
    'MatchExtractsWithReference',
    'AreSameImagesRandom',
    'AreSameImagesReference',
    'AreSameImagesReferenceOneExtract',
    'PercentQualityRandom',
    'IsImageCorrect',
    'IsImageCorrectOneExtract'
    'CalibrationMeasurement'
]

default_host = 'diran.univ-littoral.fr'