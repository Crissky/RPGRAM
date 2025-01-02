from repository.mongo import ClasseModel, RaceModel


COMMANDS = ['criarpersonagem', 'createchar']


# CALLBACK DATA
CALLBACK_TEXT_YES = 'yes'
CALLBACK_TEXT_NO = 'no'
CALLBACK_TEXT_RACES = '|'.join(RaceModel().get_all(fields=['name']))
CALLBACK_TEXT_CLASSES = '|'.join(ClasseModel().get_all(fields=['name']))
