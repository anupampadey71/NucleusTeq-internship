import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Make sure you have `react-router-dom` installed
import { useAuth } from '../../context/AuthContext';

const UserDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div>
      <h2>User Dashboard</h2>
      <nav style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '20px' }}>
        <Link to="/user/departments" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Departments
        </Link>
        <Link to="/user/employees" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Employees
        </Link>
        
        <Link to="/user/skillsets" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Skillsets
        </Link>
        <Link to="/user/managers" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Manager
        </Link>
        <Link to="/user/employeeskills" style={{ margin: '0 10px', textDecoration: 'none' }}>
          EmployeeSkills
        </Link>
        <Link to="/user/projects" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Projects
        </Link>
        
        <Link to="/user/assignments" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Assignment
        </Link>
      </nav>
    </div>
  );
};

export default UserDashboard;
