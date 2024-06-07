import React, { useState, useEffect } from 'react';
import { getEmployees, addEmployee, updateEmployee, deleteEmployee } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';
import './AdminCss/AdminEmployee.css';

const AdminEmployee = () => {
  const { user } = useAuth();
  const [employees, setEmployees] = useState([]);
  const [employeeInfo, setEmployeeInfo] = useState({ employeeId: '', email: '', name: '', salary: '', role: '' });
  const [updateEmployeeInfo, setUpdateEmployeeInfo] = useState({ employeeId: '', email: '', name: '', salary: '', role: '', is_assigned: false });
  const [deleteEmployeeId, setDeleteEmployeeId] = useState('');

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await getEmployees(user);
      setEmployees(response.data);
    } catch (error) {
      console.error('Failed to fetch employees', error);
    }
  };

  const handleAddEmployee = async () => {
    try {
      await addEmployee(
        employeeInfo.employeeId, 
        employeeInfo.email, 
        employeeInfo.name, 
        employeeInfo.salary, 
        employeeInfo.role, 
        user
      );
      fetchEmployees();
      setEmployeeInfo({ employeeId: '', email: '', name: '', salary: '', role: '' });
    } catch (error) {
      console.error('Failed to add employee:', error.response ? error.response.data : error.message);
      alert('Failed to add employee. Please try again.');
    }
  };

  const handleUpdateEmployee = async () => {
    try {
      await updateEmployee(
        updateEmployeeInfo.employeeId, 
        updateEmployeeInfo.email, 
        updateEmployeeInfo.name, 
        updateEmployeeInfo.salary, 
        updateEmployeeInfo.role, 
        updateEmployeeInfo.is_assigned,
        user
      );
      fetchEmployees();
      setUpdateEmployeeInfo({ employeeId: '', email: '', name: '', salary: '', role: '', is_assigned: false });
    } catch (error) {
      console.error('Failed to update employee:', error.response ? error.response.data : error.message);
      alert('Failed to update employee. Please try again.');
    }
  };

  const handleDeleteEmployee = async () => {
    try {
      await deleteEmployee(deleteEmployeeId, user);
      fetchEmployees();
      setDeleteEmployeeId('');
    } catch (error) {
      console.error('Failed to delete employee:', error.response ? error.response.data : error.message);
      alert('Failed to delete employee. Please try again.');
    }
  };

  const handleEmployeeChange = (e) => {
    const { name, value } = e.target;
    setEmployeeInfo({ ...employeeInfo, [name]: value });
  };

  const handleUpdateEmployeeChange = (e) => {
    const { name, value } = e.target;
    setUpdateEmployeeInfo({ ...updateEmployeeInfo, [name]: value });
  };

  const handleDeleteEmployeeChange = (e) => {
    setDeleteEmployeeId(e.target.value);
  };

  return (
    <div className="admin-employee-container">
      <div className="employees-list">
        <h3>Employees</h3>
        {employees.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Email</th>
                <th>Name</th>
                <th>Salary</th>
                <th>Role</th>
                <th>Assigned</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.employeeId}>
                  <td>{emp.employeeId}</td>
                  <td>{emp.email}</td>
                  <td>{emp.name}</td>
                  <td>{emp.salary}</td>
                  <td>{emp.role}</td>
                  <td>{emp.is_assigned ? 'Assigned' : 'Not Assigned'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No employees available.</p>
        )}
      </div>
  
      <div className="create-employee">
        <h3>Add Employee</h3>
        <div>
          <input type="text" placeholder="Employee Id" value={employeeInfo.employeeId} onChange={handleEmployeeChange} name="employeeId" />
          <br />
          <input type="text" placeholder="Email" value={employeeInfo.email} onChange={handleEmployeeChange} name="email" />
          <br />
          <input type="text" placeholder="Name" value={employeeInfo.name} onChange={handleEmployeeChange} name="name" />
          <br />
          <input type="text" placeholder="Salary" value={employeeInfo.salary} onChange={handleEmployeeChange} name="salary" />
          <br />
          <input type="text" placeholder="Role" value={employeeInfo.role} onChange={handleEmployeeChange} name="role" />
          <br />
          <button onClick={handleAddEmployee}>Add Employee</button>
        </div>
      </div>
  
      <div className="update-employee">
        <h3>Update Employee</h3>
        <div>
          <input type="text" placeholder="Employee Id" value={updateEmployeeInfo.employeeId} onChange={handleUpdateEmployeeChange} name="employeeId" />
          <br />
          <input type="text" placeholder="Email" value={updateEmployeeInfo.email} onChange={handleUpdateEmployeeChange} name="email" />
          <br />
          <input type="text" placeholder="Name" value={updateEmployeeInfo.name} onChange={handleUpdateEmployeeChange} name="name" />
          <br />
          <input type="text" placeholder="Salary" value={updateEmployeeInfo.salary} onChange={handleUpdateEmployeeChange} name="salary" />
          <br />
          <input type="text" placeholder="Role" value={updateEmployeeInfo.role} onChange={handleUpdateEmployeeChange} name="role" />
          <br />
          <label>
            Assigned:
            <input type="checkbox" checked={updateEmployeeInfo.is_assigned} onChange={(e) => setUpdateEmployeeInfo({ ...updateEmployeeInfo, is_assigned: e.target.checked })} name="is_assigned" />
          </label>
          <br />
          <button onClick={handleUpdateEmployee}>Update Employee</button>
        </div>
      </div>
  
      <div className="delete-employee">
        <h3>Delete Employee</h3>
        <div>
          <input type="text" placeholder="Employee Id" value={deleteEmployeeId} onChange={handleDeleteEmployeeChange} name="employeeId" />
          <br />
          <button onClick={handleDeleteEmployee}>Delete Employee</button>
        </div>
      </div>
    </div>
  );
  
};

export default AdminEmployee;
