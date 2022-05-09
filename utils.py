from decimal import Decimal
import json


class DecimalJsonEncoder(json.JSONDecoder):
    """_summary_
        This class converts decimal values in the JSON file to
        string format.
    """
    
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        
        return json.JSONEncoder.default(self, obj)
        

def serialize_list(list_):
    response = "["
    
    for el in list_:
        response += el 
        response += ", "
    response = response[:-2] + "]"
    
    return response