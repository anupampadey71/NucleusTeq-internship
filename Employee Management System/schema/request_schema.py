from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "requestId" : todo[0],
        "projectId" : todo[1],
        "skillId" : todo[2],
        "status" : todo[3]
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output