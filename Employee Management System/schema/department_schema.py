from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "departmentId" : todo[0],
        "name" : todo[1],
        "ManagerId" : todo[2],
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output