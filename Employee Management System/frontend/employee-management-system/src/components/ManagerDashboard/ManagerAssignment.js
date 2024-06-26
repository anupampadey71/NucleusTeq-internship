import React, { useState, useEffect } from 'react';
import { getAllAssignments } from '../../services/apiService'; // Reusing the same API service as AdminAssignment
import { useAuth } from '../../context/AuthContext';
import './ManagerCss/ManagerAssignment.css'
const ManagerAssignment = () => {
  const { user } = useAuth();
  const [assignments, setAssignments] = useState([]);
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

  useEffect(() => {
    fetchAllAssignments();
  }, [refetch]);

  return (
    <div className="manager-assignment-container">
      <h2>Assignments</h2>
      <div className="assignments-list">
        <h3>All Assignments under Manager</h3>
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
                  <td>{assignment.assigned ? 'Assigned' : 'Not Assigned'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No assignments available.</p>
        )}
      </div>
    </div>
  );
};

export default ManagerAssignment;
