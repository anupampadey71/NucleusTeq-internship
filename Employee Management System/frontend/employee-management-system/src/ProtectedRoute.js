import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

const ProtectedRoute = ({ role }) => {
  const { user } = useAuth();
  console.log({user, role});
  if (!user) {
    return <Navigate to="/login" />;
  }

  if (role && user.role !== role) {
    return <Navigate to="/login" />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
