from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "skillId" : todo[0],
        "skillName" : todo[1]
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output