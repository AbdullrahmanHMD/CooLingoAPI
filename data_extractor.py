import json
import os
import random

QUESTION_NUM = 8

questions_file_name = "questions.txt"
languages_path_name = "languages.txt"

file_path = os.path.join(os.getcwd(), 'data')

questions_path = os.path.join(file_path, questions_file_name)
languages_path = os.path.join(file_path, languages_path_name)


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        json_array = json.load(file)
        
    return json_array

def get_questions(k):
    questions = load_json_file(questions_path)
    selected_questions = random.sample(questions['questions'], k=k)
    
    return  {"questions" : selected_questions}

def get_languages():
    langauges = load_json_file(languages_path)
    return langauges


