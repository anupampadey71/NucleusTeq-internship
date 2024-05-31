import React, { useState, useEffect } from 'react';
import { getManagers, getManagerEmployees } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const UserManager = () => {
  const { user } = useAuth();
  const [managers, setManagers] = useState([]);
  const [managerEmployees, setManagerEmployees] = useState([]);
  const [managerId, setManagerId] = useState('');
  const [refetch, setRefetch] = useState(false);

  const fetchManagers = async () => {
    try {
      const res = await getManagers(user);
      setManagers(res.data);
    } catch (error) {
      console.error('Failed to get managers:', error.response ? error.response.data : error.message);
      alert('Failed to get managers. Please try again.');
    }
  };

  const handleGetManagerEmployees = async () => {
    try {
      const res = await getManagerEmployees(managerId, user);
      setManagerEmployees(res.data.employees);
    } catch (error) {
      console.error('Failed to get manager employees:', error.response ? error.response.data : error.message);
      alert('Failed to get manager employees. Please try again.');
    }
  };

  useEffect(() => {
    fetchManagers();
  }, [refetch]);

  return (
    <div>
      <h2>Manager Operations</h2>
      <div>
        <h3>Get Managers</h3>
        <table>
          <thead>
            <tr>
              <th>Manager ID</th>
              <th>Employee ID</th>
            </tr>
          </thead>
          <tbody>
            {managers.map((manager, index) => (
              <tr key={index}>
                <td>{manager.ManagerId}</td>
                <td>{manager.employeeId}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <h3>Get Employees by Manager ID</h3>
        <input type="text" placeholder="Manager ID" value={managerId} onChange={(e) => setManagerId(e.target.value)} />
        <button onClick={handleGetManagerEmployees}>Get Employees</button>
        {managerEmployees.length > 0 && (
          <div>
            <h4>Employees under Manager ID: {managerId}</h4>
            <ul>
              {managerEmployees.map((employee, index) => (
                <li key={index}>{employee}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserManager;
