import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Make sure you have `react-router-dom` installed
import { useAuth } from '../../context/AuthContext';

const ManagerDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div>
      <h2>Manager Dashboard</h2>
      <nav style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '20px' }}>
        <Link to="/manager/departments" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Departments
        </Link>
        <Link to="/manager/employees" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Employees
        </Link>
        
        <Link to="/manager/skillsets" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Skillsets
        </Link>
        <Link to="/manager/managers" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Manager
        </Link>
        <Link to="/manager/employeeskills" style={{ margin: '0 10px', textDecoration: 'none' }}>
          EmployeeSkills
        </Link>
        <Link to="/manager/projects" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Projects
        </Link>
        <Link to="/manager/requests" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Requests
        </Link>
        <Link to="/manager/assignments" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Assignment
        </Link>
      </nav>
    </div>
  );
};

export default ManagerDashboard;
