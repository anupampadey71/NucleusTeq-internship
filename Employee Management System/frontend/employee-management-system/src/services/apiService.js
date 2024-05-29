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

// Similarly, create methods for employees
export const getEmployees = (user) => {
  return api.get('/employees/my_info', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const addEmployee = (employee, user) => {
  return api.post('/employees', employee, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const updateEmployee = (employeeId, employee, user) => {
  return api.put(`/employees/${employeeId}`, employee, {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { username: user.username, password: user.password },
  })
  .catch(handleError);
};

export const deleteEmployee = (employeeId, user) => {
  return api.delete('/employees', {
    headers: { Authorization: `Bearer ${user.token}` },
    params: { employeeId, username: user.username, password: user.password },
  })
  .catch(handleError);
};
