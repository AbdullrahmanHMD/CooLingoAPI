import json

from datetime import datetime


from data_extractor import *


def is_word_mastered(clicked, seen):
    
    if len(clicked) != 0:
        last_clicked = clicked[-1]
        
    else:
        if len(seen) < 10:
            return False
        else:
            return True
        
    seen_word = seen[-10]    
        
    # 25-May-2022 19:32:18
    time_format = "%d-%b-%Y %H:%M:%S"
    last_clicked = datetime.strptime(last_clicked, time_format)
    seen_word = datetime.strptime(seen_word, time_format)

    return max(last_clicked, seen_word) == seen_word

def is_word_reviwing(clicked, seen):
    
    if len(clicked) != 0:
        last_clicked = clicked[-1]
        
    else:
        if len(seen) < 5:
            return False
        else:
            return True
        
    seen_word = seen[-5]    
        
    # 25-May-2022 19:32:18
    time_format = "%d-%b-%Y %H:%M:%S"
    last_clicked = datetime.strptime(last_clicked, time_format)
    seen_word = datetime.strptime(seen_word, time_format)

    return max(last_clicked, seen_word) == seen_word

def get_word_status(clicked, seen):
    status = 'learning'
    if is_word_mastered(clicked, seen):
        status = 'mastered'
    elif is_word_reviwing(clicked, seen):
        status = 'in review'

    return status

clicked = ["25-May-2022 19:32:00", "25-May-2022 19:32:00", "25-May-2022 19:32:00", "25-May-2022 19:32:19"]
seen = ["25-May-2022 19:32:18", "25-May-2022 19:32:18", "25-May-2022 19:32:18" ,"25-May-2022 19:32:18" ,"25-May-2022 19:32:18" ,"25-May-2022 19:32:18"
        ,"25-May-2022 19:32:20", "25-May-2022 19:32:20", "25-May-2022 19:32:20", "25-May-2022 19:32:20", "25-May-2022 19:32:20"]


print(get_word_status(clicked, seen))