import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Make sure you have `react-router-dom` installed
import { useAuth } from '../../context/AuthContext';
import './ManagerCss/ManagerDashboard.css'; // Importing the CSS file for styling

const ManagerDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="manager-dashboard-container">
      <h2>Manager Dashboard</h2>
      <nav className="manager-nav">
        <Link to="/manager/departments" className="nav-link">
          Departments
        </Link>
        <Link to="/manager/employees" className="nav-link">
          Employees
        </Link>
        <Link to="/manager/skillsets" className="nav-link">
          Skillsets
        </Link>
        <Link to="/manager/managers" className="nav-link">
          Manager
        </Link>
        <Link to="/manager/employeeskills" className="nav-link">
          Employee Skills
        </Link>
        <Link to="/manager/projects" className="nav-link">
          Projects
        </Link>
        <Link to="/manager/requests" className="nav-link">
          Requests
        </Link>
        <Link to="/manager/assignments" className="nav-link">
          Assignments
        </Link>
      </nav>
    </div>
  );
};

export default ManagerDashboard;
