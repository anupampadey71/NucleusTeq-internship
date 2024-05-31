import React, { useState, useEffect } from 'react';
import { getAllAssignments } from '../../services/apiService'; // Reusing the same API service as ManagerAssignment
import { useAuth } from '../../context/AuthContext';

const UserAssignment = () => {
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
    <div>
      <h2>Your Assignmented projects</h2>
      <div>
        <h3> Assignments Table</h3>
        <table>
          <thead>
            <tr>
              <th>Assignment ID</th>
              <th>Employee ID</th>
              <th>Project ID</th>
              <th>Assigned</th>
            </tr>
          </thead>
          <tbody>
            {assignments.map((assignment, index) => (
              <tr key={index}>
                <td>{assignment.assignmentId}</td>
                <td>{assignment.employeeId}</td>
                <td>{assignment.projectId}</td>
                <td>{assignment.assigned ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserAssignment;
