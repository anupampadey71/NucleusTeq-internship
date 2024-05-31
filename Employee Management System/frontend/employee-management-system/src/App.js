import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate,Outlet } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';

import { AuthProvider, useAuth } from './context/AuthContext';
import AdminDepartment from './components/AdminDashboard/AdminDepartment';
import AdminEmployee from './components/AdminDashboard/AdminEmployee';
import AdminSkillset from './components/AdminDashboard/AdminSkillsets';
import AdminManager from './components/AdminDashboard/AdminManager';
import AdminEmployeeSkill from './components/AdminDashboard/AdminEmployeeSkill';
import AdminProject from './components/AdminDashboard/AdminProject';
import AdminRequest from './components/AdminDashboard/AdminRequest';
import AdminAssignment from './components/AdminDashboard/AdminAssignment';
// import ProtectedRoute from './ProtectedRoute';
const ProtectedRoute = ({ element: Component, role, ...rest }) => {
  const { user } = useAuth();
  console.log({user,role});
  if (!user) {
    console.log('no user');
    return <Navigate to="/login" />;
  }

  else if (role && user.role !== role) {
    console.log('wrong role');
    return <Navigate to="/login" />;
  }
  else{
    console.log('right role');
    // return <Component {...rest} />;
    return <Outlet/>
  }

  
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedRoute role="admin" />}>
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/departments" element={<AdminDepartment />} />
            <Route path="/admin/employees" element={<AdminEmployee />} />
            <Route path="/admin/skillsets" element={<AdminSkillset />} />
            <Route path="/admin/managers" element={<AdminManager />} />
            <Route path="/admin/employeeskills" element={<AdminEmployeeSkill />} />
            <Route path="/admin/projects" element={<AdminProject />} />
            <Route path="/admin/requests" element={<AdminRequest />} />
            <Route path="/admin/assignments" element={<AdminAssignment />} />
          </Route>
          {/* <Route path="/admin" element={<AdminDashboard/>  } /> */}
          {/* <Route path="/admin/departments" element={<ProtectedRoute element={<AdminDepartment/>} role="admin" />} /> */}
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
