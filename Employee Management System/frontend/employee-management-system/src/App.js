import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate,Outlet } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';
// import AdminDepartment from './components/AdminDashboard/AdminDepartment/AdminDepartment';
import { AuthProvider, useAuth } from './context/AuthContext';
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
            {/* <Route path="/admin/departments" element={<AdminDepartment />} /> */}
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
