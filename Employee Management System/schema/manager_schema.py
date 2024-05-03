from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "ManagerId" : todo[0],
        "employeeId" : todo[1]
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output