import React, { useState, useEffect } from 'react';
import { getUserManager } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const UserManager = () => {
  const { user } = useAuth();
  const [managerId, setManagerId] = useState('');
  const [refetch, setRefetch] = useState(false);
  const [loggedInUserManagerId, setLoggedInUserManagerId] = useState('');

  const fetchLoggedInUserManagerId = async () => {
    try {
      const res = await getUserManager(user.username, user.password);
      setLoggedInUserManagerId(res.managerId);
    } catch (error) {
      console.error('Failed to get user manager:', error.response ? error.response.data : error.message);
      alert('Failed to get user manager. Please try again.');
    }
  };

  useEffect(() => {
    fetchLoggedInUserManagerId();
  }, [refetch]);

  return (
    <div>
      <h2>Your Manager </h2>

      <div>
        {/* <h3>Logged-In User Manager ID</h3> */}
        <p>{loggedInUserManagerId}</p>
      </div>
    </div>
  );
};

export default UserManager;
