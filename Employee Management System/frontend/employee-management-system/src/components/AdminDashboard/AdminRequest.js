import React, { useState, useEffect } from 'react';
import { getAllRequests } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';
import './AdminCss/AdminRequest.css';

const AdminRequest = () => {
  const { user } = useAuth();
  const [requests, setRequests] = useState([]);

  const fetchRequests = async () => {
    try {
      const res = await getAllRequests(user);
      setRequests(res.data.requests);
    } catch (error) {
      console.error('Failed to get requests:', error.response ? error.response.data : error.message);
      alert('Failed to get requests. Please try again.');
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  return (
    <div className="admin-request-container">
      <h2>Requests By Managers</h2>
      <div className="requests-list">
        <table>
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Project ID</th>
              <th>Skill ID</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((request, index) => (
              <tr key={index}>
                {request.map((item, i) => (
                  <td key={i}>{item}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminRequest;
