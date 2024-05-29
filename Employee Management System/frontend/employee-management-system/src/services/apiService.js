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
    params: { skillName, username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const deleteSkill = (skillId, user) => {
  return api.delete('/skillsets', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { skillId, username: user.username, password: user.password },
  })
  .catch(handleError);
};