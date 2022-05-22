import json

from datetime import datetime


dateTimeObj = datetime.now()

time_stamp = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S")

print(time_stamp)


word = "Sarieh"

word_dict = {word : {'clicked' : [], 'seen' : []}}

word_dict[word]['clicked'].append(time_stamp)
word_dict[word]['clicked'].append(time_stamp)
word_dict[word]['clicked'].append(time_stamp)
word_dict[word]['clicked'].append(time_stamp)

word_dict[word]['seen'].append(time_stamp)
word_dict[word]['seen'].append(time_stamp)
word_dict[word]['seen'].append(time_stamp)
word_dict[word]['seen'].append(time_stamp)

print(json.dumps(word_dict))