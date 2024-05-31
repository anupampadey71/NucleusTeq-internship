import React, { useState, useEffect } from 'react';
import { getDepartments } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const ManagerDepartment = () => {
  const { user } = useAuth();
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    fetchDepartments();
  }, []);

  const fetchDepartments = async () => {
    try {
      const response = await getDepartments(user);
      setDepartments(response.data);
    } catch (error) {
      console.error('Failed to fetch departments', error);
    }
  };

  return (
    <div>
      <div>
        <h3>Departments Table</h3>
        {departments.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Department ID</th>
                <th>Name</th>
                <th>Manager ID</th>
              </tr>
            </thead>
            <tbody>
              {departments.map((dept) => (
                <tr key={dept.departmentId}>
                  <td>{dept.departmentId}</td>
                  <td>{dept.name}</td>
                  <td>{dept.ManagerId}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No departments available.</p>
        )}
      </div>
    </div>
  );
};

export default ManagerDepartment;
