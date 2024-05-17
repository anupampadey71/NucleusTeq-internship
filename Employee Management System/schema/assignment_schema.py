from typing import List

def individual_assignment_serial(assignment) -> dict:
    dictionary = {
        "assignmentId": assignment[0],
        "requestId": assignment[1],
        "employeeId": assignment[2],
        "projectId": assignment[3],
        "assigned": assignment[4]
    }
    return dictionary

def list_serial(assignments) -> List[dict]:
    output = [individual_assignment_serial(assignment) for assignment in assignments]
    return output
