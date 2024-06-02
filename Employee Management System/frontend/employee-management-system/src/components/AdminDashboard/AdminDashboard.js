import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AdminCss/AdminDashboard.css'; // Importing the CSS file for styling

const AdminDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="admin-dashboard-container">
      <h2>Admin Dashboard</h2>
      <nav className="admin-nav">
        <Link to="/admin/departments" className="nav-link">
          Departments
        </Link>
        <Link to="/admin/employees" className="nav-link">
          Employees
        </Link>
        <Link to="/admin/skillsets" className="nav-link">
          Skillsets
        </Link>
        <Link to="/admin/managers" className="nav-link">
          Managers
        </Link>
        <Link to="/admin/employeeskills" className="nav-link">
          Employee Skills
        </Link>
        <Link to="/admin/projects" className="nav-link">
          Projects
        </Link>
        <Link to="/admin/requests" className="nav-link">
          Requests
        </Link>
        <Link to="/admin/assignments" className="nav-link">
          Assignments
        </Link>
      </nav>
    </div>
  );
};

export default AdminDashboard;
