import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
});

// Centralized error handling
const handleError = (error) => {
  console.error('API call failed. ', error.response ? error.response.data : error.message);
  throw error;
};

export const login = (username, password) => {
  return api.post('/auth/login', new URLSearchParams({ username, password }))
    .catch(handleError);
};

export const getDepartments = (user) => {
  return api.get(`/departments/my_info`, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const addDepartment = (departmentId, name, managerId, user) => {
  return api.post(`/departments`, {
    departmentId,
    name,
    managerId,
  }, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const updateDepartment = (departmentId, name, user) => {
  console.log('Updating department:', departmentId, name);
  return api.put(`/departments/${departmentId}`, null, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { name, username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const deleteDepartment = (departmentId, user) => {
  return api.delete('/departments', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { departmentId, username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to get employees
export const getEmployees = (user) => {
  return api.get('/employees/my_info', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to add an employee
export const addEmployee = (employeeId, email, name, salary, role, user) => {
  return api.post('/employees', {
    employeeId,
    email,
    name,
    salary,
    role,
  }, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to update an employee
export const updateEmployee = (employeeId, email, name, salary, role, is_assigned, user) => {
  return api.put(`/employees/${employeeId}`, {
    email,
    name,
    salary,
    role,
    is_assigned,
  }, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to delete an employee
export const deleteEmployee = (employeeId, user) => {
  return api.delete('/employees', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { employeeId, username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const addSkill = (skillId, skillName, user) => {
  return api.post(`/skillsets/`, {
    skillId,
    skillName,
  }, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to get all skills
export const getSkills = (user) => {
  return api.get('/skillsets/all_skills', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};


export const updateSkill = (skillId, skillName, user) => {
  return api.put(`/skillsets/${skillId}`, null, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { name: skillName, username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const deleteSkill = (skillId, user) => {
  return api.delete(`/skillsets/${skillId}`, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};


export const addManager = (managerId, employeeId, user) => {
  return api.post(`/manager/`, {
    managerId,
    employeeId,
  }, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const getManagers = (user) => {
  return api.get(`/manager/`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const getManagerEmployees = (managerId, user) => {
  return api.get(`/manager/${managerId}/employees/`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const updateManager = (managerId, oldEmployeeId, newEmployeeId, user) => {
  return api.put(`/manager/${managerId}`, null, {
    params: { old_employeeId: oldEmployeeId, new_employeeId: newEmployeeId, username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const deleteManager = (managerId, employeeId, user) => {
  return api.delete(`/manager/${managerId}`, {
    params: { employeeId: employeeId, username: user.username, password: user.password },
  })
  .catch(handleError);
};

//EmployeeSkill
export const addEmployeeSkill = (employeeId, skillId, user) => {
  return api.post(`/employeeskill/`, {
    employeeId,
    skillId,
  }, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const updateEmployeeSkill = (employeeId, currentSkillId, newSkillId, user) => {
  return api.put(`/employeeskill/`, null, {
    params: { employee_id: employeeId, current_skill_id: currentSkillId, new_skill_id: newSkillId, username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const getEmployeeSkills = (employeeId, user) => {
  return api.get(`/employeeskill/${employeeId}`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};


// Function to add a project
export const addProject = (projectData, user) => {
  return api.post(`/project/`, projectData, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to update a project
export const updateProject = (projectId, projectData, user) => {
  return api.put(`/project/${projectId}`, projectData, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};


// Function to get all projects
export const getAllProjects = (user) => {
  return api.get(`/project/all_projects`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to delete a project
export const deleteProject = (projectId, user) => {
  return api.delete(`/project/${projectId}`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};


export const deleteEmployeeSkill = (employeeId, skillId, user) => {
  return api.delete(`/employeeskill/${employeeId}/${skillId}`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

//request
export const getAllRequests = (user) => {
  return api.get('/request/all_requests', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to add an assignment
export const addAssignment = (assignmentData, user) => {
  return api.post(`/assignment/`, assignmentData, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to get all assignments
export const getAllAssignments = (user) => {
  return api.get('/assignment/all_assignments', {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to update an assignment
export const updateAssignment = (assignmentId, assigned, user) => {
  return api.put(`/assignment/${assignmentId}`, null, {
    params: { assigned, username: user.username, password: user.password },
  })
  .catch(handleError);
};

// Function to delete an assignment
export const deleteAssignment = (assignmentId, user) => {
  return api.delete(`/assignment/${assignmentId}`, {
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};