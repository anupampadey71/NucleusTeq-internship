from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "projectId" : todo[0],
        "name" : todo[1],
        "description" : todo[2]
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output