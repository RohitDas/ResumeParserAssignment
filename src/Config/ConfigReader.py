import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/home/likewise-open/PUNESEZ/rohitangsu.das/Documents/ResumeParser/src/Config/config.ini')

class ConfigReader:

    Gazetter = config.get('FilePath', 'Gazetter')
    SubGazetter = config.get('FilePath', 'SubGazetter')
    ResumeJSONdir =config.get('FilePath', 'ResumeJSONdir')
    LOG = config.get('FilePath', 'LoggingFile')
    HTML_LOG = config.get('FilePath','HTMLLoggingFile')
    ResumeDir = config.get('FilePath','ResumeDir')
    ModelFilePath = config.get('FilePath','ModelFilePath')
    WordLengthThetha = config.get('FilePath','WordLengthThetha')
    TemporaryFileLoad = config.get('FilePath','TemporaryFileLoad')
    PaddingThetha = config.get('FilePath','PaddingThetha')
    CityNameGazzetter = config.get('FilePath','CityNameGazzetter')
    NamesGazzetter = config.get('FilePath','NamesGazzetter')
    CRFModelFilePath = config.get('FilePath','CRFModelFilePath')
    DecisionTreeTrainingFile = config.get('FilePath', 'CRFModelFilePath')
    CountryGazetter = config.get('FilePath', 'CountryGazetter')
