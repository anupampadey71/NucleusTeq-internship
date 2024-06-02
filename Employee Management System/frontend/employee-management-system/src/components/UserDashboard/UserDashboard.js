import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Make sure you have `react-router-dom` installed
import { useAuth } from '../../context/AuthContext';
import './UserCss/UserDashboard.css'

const UserDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="user-dashboard-container">
      <h2>User Dashboard</h2>
      <nav className="user-nav">
        <Link to="/user/departments" className="nav-link">
          Departments
        </Link>
        <Link to="/user/employees" className="nav-link">
          Employees
        </Link>
        <Link to="/user/skillsets" className="nav-link">
          Skillsets
        </Link>
        <Link to="/user/managers" className="nav-link">
          Manager
        </Link>
        <Link to="/user/employeeskills" className="nav-link">
          EmployeeSkills
        </Link>
        <Link to="/user/projects" className="nav-link">
          Projects
        </Link>
        <Link to="/user/assignments" className="nav-link">
          Assignment
        </Link>
      </nav>
    </div>
  );
  
};

export default UserDashboard;
