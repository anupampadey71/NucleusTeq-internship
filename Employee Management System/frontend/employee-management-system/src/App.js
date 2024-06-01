import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, Outlet } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';
import ManagerDashboard from './components/ManagerDashboard/ManagerDashboard';
import UserDashboard from './components/UserDashboard/UserDashboard';
import { AuthProvider, useAuth } from './context/AuthContext';
import AdminDepartment from './components/AdminDashboard/AdminDepartment';
import AdminEmployee from './components/AdminDashboard/AdminEmployee';
import AdminSkillset from './components/AdminDashboard/AdminSkillsets';
import AdminManager from './components/AdminDashboard/AdminManager';
import AdminEmployeeSkill from './components/AdminDashboard/AdminEmployeeSkill';
import AdminProject from './components/AdminDashboard/AdminProject';
import AdminRequest from './components/AdminDashboard/AdminRequest';
import AdminAssignment from './components/AdminDashboard/AdminAssignment';
import ManagerDepartment from './components/ManagerDashboard/ManagerDepartment';
import ManagerEmployee from './components/ManagerDashboard/ManagerEmployee';
import ManagerSkillset from './components/ManagerDashboard/ManagerSkillset';
import ManagerManager from './components/ManagerDashboard/ManagerManager';
import ManagerEmployeeSkill from './components/ManagerDashboard/ManagerEmployeeSkill';
import ManagerProject from './components/ManagerDashboard/ManagerProject';

import UserDepartment from './components/UserDashboard/UserDepartment';
import UserEmployee from './components/UserDashboard/UserEmployee';
import UserSkillset from './components/UserDashboard/UserSkillset';
import UserManager from './components/UserDashboard/UserManager';
import UserEmployeeSkill from './components/UserDashboard/UserEmployeeSkill';
import UserProject from './components/UserDashboard/UserProject';
import ManagerRequest from './components/ManagerDashboard/MangerRequest';
import ManagerAssignment from './components/ManagerDashboard/ManagerAssignment';
import UserAssignment from './components/UserDashboard/UserAssignment';
import ChangePassword from './pages/ChangePassword';





const ProtectedRoute = ({ role }) => {
  const { user } = useAuth();
  console.log({ user, role });
  if (!user) {
    console.log('no user');
    return <Navigate to="/login" />;
  } else if (role && user.role !== role) {
    console.log('wrong role');
    return <Navigate to="/login" />;
  } else {
    console.log('right role');
    return <Outlet />;
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

          <Route element={<ProtectedRoute role="manager" />}>
            <Route path="/manager" element={<ManagerDashboard />} />
            <Route path="/manager/departments" element={<ManagerDepartment />} />
            <Route path="/manager/employees" element={<ManagerEmployee />} />
            <Route path="/manager/skillsets" element={<ManagerSkillset />} />
            <Route path="/manager/managers" element={<ManagerManager />} />
            <Route path="/manager/employeeskills" element={<ManagerEmployeeSkill />} />
            <Route path="/manager/projects" element={<ManagerProject />} />
            <Route path="/manager/requests" element={<ManagerRequest />} />
            <Route path="/manager/assignments" element={<ManagerAssignment />} />
          </Route>

          <Route element={<ProtectedRoute role="user" />}>
            <Route path="/user" element={<UserDashboard />} />
            <Route path="/user/departments" element={<UserDepartment />} />
            <Route path="/user/employees" element={<UserEmployee />} />
            <Route path="/user/skillsets" element={<UserSkillset />} />
            <Route path="/user/managers" element={<UserManager />} />
            <Route path="/user/employeeskills" element={<UserEmployeeSkill />} />
            <Route path="/user/projects" element={<UserProject />} />
            <Route path="/user/assignments" element={<UserAssignment />} /> 
          </Route>

          <Route path="/change-password" element={<ChangePassword />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
