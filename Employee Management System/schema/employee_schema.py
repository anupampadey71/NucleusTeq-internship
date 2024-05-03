from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "employeeId" : todo[0],
        "email" : todo[1],
        "name" : todo[2],
        "salary" : todo[3],
        "role" : todo[4]
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output