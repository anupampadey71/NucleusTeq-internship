import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const login = (username, password) => {
  return api.post('/auth/login', new URLSearchParams({ username, password }));
};

export const getDepartments = (user) => {
  return api.get(`/departments/my_info?username=${user.username}&password=${user.password}`, {
    headers: { Authorization: `Bearer ${user.token}` },
  });
};

export const addDepartment = (departmentId, name, managerId,user) => {
  return api.post(`/departments?username=${user.username}&password=${user.password}`, {
    "departmentId": departmentId,
    "name": name,
    "managerId": managerId
  }, {
    headers: { Authorization: `Bearer ${user.token}` },
  });
};

export const updateDepartment = (departmentId, name, user) => {
  return api.put(`/departments/${departmentId}?username=${user.username}&password=${user.password}&name=${name}`, {
    headers: { Authorization: `Bearer ${user.token}` },
  });
};

export const deleteDepartment = (departmentId, user) => {
  return api.delete(`/departments?departmentId=${departmentId}&username=${user.username}&password=${user.password}`, {
    headers: { Authorization: `Bearer ${user.token}` },
  });
};

// Similarly, create methods for employees
export const getEmployees = (token) => {
  return api.get('/employees/my_info', {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const addEmployee = (employee, token) => {
  return api.post('/employees', employee, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const updateEmployee = (employeeId, employee, token) => {
  return api.put(`/employees/${employeeId}`, employee, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const deleteEmployee = (employeeId, token) => {
  return api.delete('/employees', {
    params: { employeeId },
    headers: { Authorization: `Bearer ${token}` },
  });
};
