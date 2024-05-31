import React, { useState, useEffect } from 'react';
import { getEmployees } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const UserEmployee = () => {
  const { user } = useAuth();
  const [employees, setEmployees] = useState([]);

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

  return (
    <div>
      <div>
        <h3>Employees Table</h3>
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
                  <td>{emp.is_assigned ? 'Yes' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No employees available.</p>
        )}
      </div>
    </div>
  );
};

export default UserEmployee;
