import json
import os
import random

QUESTION_NUM = 8

file_name = "questions.txt"
questions_path = os.path.join(os.getcwd(), file_name)


def load_json_file(file_path):
    with open(questions_path, 'r') as file:
        json_array = json.load(file)
        
    return json_array

def select_random_questions(questions, k):
    selected_questions = random.sample(questions['questions'], k=k)
    
    return selected_questions

JSON_QUESTIONS_FILE = load_json_file(questions_path)
QUESTIONS_JSON_ARRAY = {"questions" : select_random_questions(JSON_QUESTIONS_FILE, QUESTION_NUM)}

print(QUESTIONS_JSON_ARRAY)