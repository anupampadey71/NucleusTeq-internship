import React, { useState, useEffect } from 'react';
import { addAssignment, deleteAssignment, getAllAssignments, updateAssignment } from '../../services/apiService';
import { useAuth } from '../../context/AuthContext';
import './AdminCss/AdminAssignment.css';

const AdminAssignment = () => {
  const { user } = useAuth();
  const [assignments, setAssignments] = useState([]);
  const [assignmentId, setAssignmentId] = useState('');
  const [requestId, setRequestId] = useState('');
  const [employeeId, setEmployeeId] = useState('');
  const [projectId, setProjectId] = useState('');
  const [assignmentIdToDelete, setAssignmentIdToDelete] = useState('');
  const [assignmentIdToUpdate, setAssignmentIdToUpdate] = useState('');
  const [assigned, setAssigned] = useState(false);
  const [refetch, setRefetch] = useState(false);

  const fetchAllAssignments = async () => {
    try {
      const res = await getAllAssignments(user);
      setAssignments(res.data);
    } catch (error) {
      console.error('Failed to get assignments:', error.response ? error.response.data : error.message);
      alert('Failed to get assignments. Please try again.');
    }
  };

  const handleAddAssignment = async () => {
    try {
      const assignmentData = {
        assignmentId,
        requestId,
        employeeId,
        projectId
      };
      const res = await addAssignment(assignmentData, user);
      console.log(res); // Handle success response
      setAssignments(prevAssignments => [...prevAssignments, assignmentData]);
      setAssignmentId('');
      setRequestId('');
      setEmployeeId('');
      setProjectId('');
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to add assignment:', error.response ? error.response.data : error.message);
      alert('Failed to add assignment. Please try again.');
    }
  };

  const handleUpdateAssignment = async () => {
    try {
      const res = await updateAssignment(assignmentIdToUpdate, assigned, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to update assignment:', error.response ? error.response.data : error.message);
      alert('Failed to update assignment. Please try again.');
    }
  };

  const handleDeleteAssignment = async () => {
    try {
      const res = await deleteAssignment(assignmentIdToDelete, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to delete assignment:', error.response ? error.response.data : error.message);
      alert('Failed to delete assignment. Please try again.');
    }
  };

  useEffect(() => {
    fetchAllAssignments();
  }, [refetch]);

  return (
    <div className="admin-assignment-container">
      <div className="assignments-list">
        <h3>Assignments</h3>
        {assignments.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Assignment ID</th>
                <th>Request ID</th>
                <th>Employee ID</th>
                <th>Project ID</th>
                <th>Assigned</th>
              </tr>
            </thead>
            <tbody>
              {assignments.map((assignment, index) => (
                <tr key={index}>
                  <td>{assignment.assignmentId}</td>
                  <td>{assignment.requestId}</td>
                  <td>{assignment.employeeId}</td>
                  <td>{assignment.projectId}</td>
                  <td>{assignment.assigned ? 'Yes' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No assignments available.</p>
        )}
      </div>
  
      <div className="create-assignment">
        <h3>Add Assignment</h3>
        <div>
          <input
            type="text"
            placeholder="Assignment ID"
            value={assignmentId}
            onChange={(e) => setAssignmentId(e.target.value)}
            name="assignmentId"
          />
          <br />
          <input
            type="text"
            placeholder="Request ID"
            value={requestId}
            onChange={(e) => setRequestId(e.target.value)}
            name="requestId"
          />
          <br />
          <input
            type="text"
            placeholder="Employee ID"
            value={employeeId}
            onChange={(e) => setEmployeeId(e.target.value)}
            name="employeeId"
          />
          <br />
          <input
            type="text"
            placeholder="Project ID"
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            name="projectId"
          />
          <br />
          <button onClick={handleAddAssignment}>Add Assignment</button>
        </div>
      </div>
  
      <div className="update-assignment">
        <h3>Update Assignment</h3>
        <div>
          <input
            type="text"
            placeholder="Assignment ID"
            value={assignmentIdToUpdate}
            onChange={(e) => setAssignmentIdToUpdate(e.target.value)}
            name="assignmentIdToUpdate"
          />
          <br />
          <label>
            Assigned:
            <input
              type="checkbox"
              checked={assigned}
              onChange={(e) => setAssigned(e.target.checked)}
              name="assigned"
            />
          </label>
          <br />
          <button onClick={handleUpdateAssignment}>Update Assignment</button>
        </div>
      </div>
  
      <div className="delete-assignment">
        <h3>Delete Assignment</h3>
        <div>
          <input
            type="text"
            placeholder="Assignment ID"
            value={assignmentIdToDelete}
            onChange={(e) => setAssignmentIdToDelete(e.target.value)}
            name="assignmentIdToDelete"
          />
          <br />
          <button onClick={handleDeleteAssignment}>Delete Assignment</button>
        </div>
      </div>
    </div>
  );
  
};

export default AdminAssignment;
