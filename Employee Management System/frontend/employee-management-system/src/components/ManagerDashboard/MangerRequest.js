import React, { useState, useEffect } from 'react';
import { addRequest, deleteRequest, getAllRequests, updateRequest } from '../../services/apiService';
import { useAuth } from '../../context/AuthContext';
import './ManagerCss/ManagerRequest.css';

const ManagerRequest = () => {
  const { user } = useAuth();
  const [requests, setRequests] = useState([]);
  const [requestId, setRequestId] = useState('');
  const [projectId, setProjectId] = useState('');
  const [skillId, setSkillId] = useState('');
  const [status, setStatus] = useState('');
  const [requestIdToDelete, setRequestIdToDelete] = useState('');
  const [requestIdToUpdate, setRequestIdToUpdate] = useState('');
  const [newStatus, setNewStatus] = useState('');
  const [refetch, setRefetch] = useState(false);

  const fetchAllRequests = async () => {
    try {
      const res = await getAllRequests(user);
      setRequests(res.data.requests);
    } catch (error) {
      console.error('Failed to get requests:', error.response ? error.response.data : error.message);
      alert('Failed to get requests. Please try again.');
    }
  };

  const handleAddRequest = async () => {
    try {
      const requestData = {
        requestId,
        projectId,
        skillId,
        status
      };
      const res = await addRequest(requestData, user);
      console.log(res); // Handle success response
      setRequests(prevRequests => [...prevRequests, requestData]);
      setRequestId('');
      setProjectId('');
      setSkillId('');
      setStatus('');
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to add request:', error.response ? error.response.data : error.message);
      alert('Failed to add request. Please try again.');
    }
  };

  const handleUpdateRequest = async () => {
    try {
      const res = await updateRequest(requestIdToUpdate, newStatus, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to update request:', error.response ? error.response.data : error.message);
      alert('Failed to update request. Please try again.');
    }
  };

  const handleDeleteRequest = async () => {
    try {
      const res = await deleteRequest(requestIdToDelete, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to delete request:', error.response ? error.response.data : error.message);
      alert('Failed to delete request. Please try again.');
    }
  };

  useEffect(() => {
    fetchAllRequests();
  }, [refetch]);

  return (
    <div className="manager-request-container">
      <div className="requests-list">
        <h2>Request List</h2>
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
                <td>{request[0]}</td>
                <td>{request[1]}</td>
                <td>{request[2]}</td>
                <td>{request[3]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
  
      <div className="request-operation-container">
        <div>
          <h3>Add Request</h3>
          <input 
            type="text" 
            placeholder="Request ID" 
            value={requestId} 
            onChange={(e) => setRequestId(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="Project ID" 
            value={projectId} 
            onChange={(e) => setProjectId(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="Skill ID" 
            value={skillId} 
            onChange={(e) => setSkillId(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="Status" 
            value={status} 
            onChange={(e) => setStatus(e.target.value)} 
          />
          <button onClick={handleAddRequest}>Add Request</button>
        </div>
  
        <div>
          <h3>Update Request</h3>
          <input 
            type="text" 
            placeholder="Request ID" 
            value={requestIdToUpdate} 
            onChange={(e) => setRequestIdToUpdate(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="New Status" 
            value={newStatus} 
            onChange={(e) => setNewStatus(e.target.value)} 
          />
          <button onClick={handleUpdateRequest}>Update Request</button>
        </div>
  
        <div>
          <h3>Delete Request</h3>
          <input 
            type="text" 
            placeholder="Request ID" 
            value={requestIdToDelete} 
            onChange={(e) => setRequestIdToDelete(e.target.value)} 
          />
          <button onClick={handleDeleteRequest}>Delete Request</button>
        </div>
      </div>
    </div>
  );
  
};

export default ManagerRequest;

