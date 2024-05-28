from typing import List

def individual_serial(todo) -> dict:
    dictionary = {
        "employeeId": todo[0],
        "email": todo[1],
        "name": todo[2],
        "salary": todo[3],
        "role": todo[4],
        "is_assigned": todo[5]  # Include is_assigned in the serialization
    }
    return dictionary

def list_serial(todos) -> List[dict]:
    output = [individual_serial(todo) for todo in todos]
    return output
