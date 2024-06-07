import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './UserCss/UserDashboard.css';

const UserDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <div className="user-dashboard-container">
      <h2>User Dashboard</h2>
      <nav className="user-nav">
        <Link to="/user/departments" className="nav-link">Departments</Link>
        <Link to="/user/employees" className="nav-link">Employees</Link>
        <Link to="/user/skillsets" className="nav-link">Skillsets</Link>
        <Link to="/user/managers" className="nav-link">Manager</Link>
        <Link to="/user/employeeskills" className="nav-link">Employee Skills</Link>
        <Link to="/user/projects" className="nav-link">Projects</Link>
        <Link to="/user/assignments" className="nav-link">Assignments</Link>
      </nav>
      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default UserDashboard;
