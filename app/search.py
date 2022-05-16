from fuzzywuzzy import fuzz
#from . import schemas, database, models


def search_author(word, standart):
    if fuzz.WRatio(word, standart) > 85:        
        return True
    else:
        return False   

def search_title(word, standart):
    if fuzz.WRatio(word, standart) > 55:        
        return True
    else:
        return False     
        

# print (search_author('Л Н Толстой', 'Лев николаевич Тодстойй'))