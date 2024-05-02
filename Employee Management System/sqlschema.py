class Employee:
    def __init__(self, employeeId, email, name, role, project=None, manager=None, department=None):
        self.employeeId = employeeId
        self.email = self._validate_email(email)
        self.name = name
        self.role = role
        self.project = project  # Can be assigned later
        self.manager = manager  # Can be assigned later
        self.department = department  # Can be assigned later

    def _validate_email(self, email):
        # Implement email validation logic (e.g., using regular expressions)
        # Raise an exception if email is invalid
        pass

    def assign_project(self, project):
        if isinstance(project, Project):
            self.project = project
            # Update project data as needed (e.g., add employee to project list)
        else:
            raise ValueError("Invalid project object provided")

    # ... other methods like getters, setters, etc.

class Project:
    def __init__(self, projectId, name, description, manager=None):
        self.projectId = projectId
        self.name = name
        self.description = description
        self.manager = manager  # Can be assigned a Manager object later

    def assign_manager(self, manager):
        if isinstance(manager, Manager):
            self.manager = manager
        else:
            raise ValueError("Invalid manager object provided")

    # ... other methods like getters, setters, etc.

class Manager(Employee):
    def __init__(self, employeeId, department=None):
        super().__init__(employeeId, None, None, "Manager", department=department)  # Predefined manager role

class Department:
    def __init__(self, departmentId, name, managerId=None):
        self.departmentId = departmentId
        self.name = name
        self.manager = managerId  # Can be assigned a Manager object later

    def assign_manager(self, manager):
        if isinstance(manager, Manager):
            self.manager = manager
        else:
            raise ValueError("Invalid manager object provided")

    # ... other methods like getters, setters, etc.

class SkillSet:
    def __init__(self, skillId, skillName):
        self.skillId = skillId
        self.skillName = skillName

class EmployeeSkill:
    def __init__(self, employee: Employee, skill: SkillSet):
        # Enforce relationship by requiring Employee and SkillSet objects
        self.employee = employee
        self.skill = skill

class Request:
    def __init__(self, requestId, projectId: Project, skill: SkillSet, status):
        self.requestId = requestId
        self.project = projectId
        self.skill = skill
        self.status = status

        # You can add validation for status values here (e.g., "Open", "Closed")

# Example usage
emp1 = Employee("EMP001", "john.doe@company.com", "John Doe", "Software Engineer")
project1 = Project("PROJ001", "E-commerce Platform", "Development of an online store platform.")
manager1 = Manager("EMP002")  # Inherits from Employee

# Assign project and manager
emp1.assign_project(project1)
project1.assign_manager(manager1)

# Skills and EmployeeSkill association
skill1 = SkillSet("SKILL001", "Java Development")
emp_skill1 = EmployeeSkill(emp1, skill1)

# Request creation
request1 = Request("REQ001", project1, skill1, "Open")  # Open request for Java skills

