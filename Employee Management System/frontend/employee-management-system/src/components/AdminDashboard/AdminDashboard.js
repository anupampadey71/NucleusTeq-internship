import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Make sure you have `react-router-dom` installed
import { useAuth } from '../../context/AuthContext';

const AdminDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <nav style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '20px' }}>
        <Link to="/admin/departments" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Departments
        </Link>
        <Link to="/admin/employees" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Employees
        </Link>
        
        <Link to="/admin/skillsets" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Skillsets
        </Link>
        <Link to="/admin/managers" style={{ margin: '0 10px', textDecoration: 'none' }}>
          Manager
        </Link>
        <Link to="/admin/employeeskills" style={{ margin: '0 10px', textDecoration: 'none' }}>
          EmployeeSkills
        </Link>
        
        
      </nav>
    </div>
  );
};

export default AdminDashboard;
