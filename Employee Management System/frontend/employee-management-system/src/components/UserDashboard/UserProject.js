import React, { useState, useEffect } from 'react';
import { getAllProjects } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';
import './UserCss/UserProject.css'; // Import CSS file

const UserProject = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [refetch, setRefetch] = useState(false);

  const fetchAllProjects = async () => {
    try {
      const res = await getAllProjects(user);
      setProjects(res.data);
    } catch (error) {
      console.error('Failed to get projects:', error.response ? error.response.data : error.message);
      alert('Failed to get projects. Please try again.');
    }
  };

  useEffect(() => {
    fetchAllProjects();
  }, [refetch]);

  return (
    <div className="user-project-container">
      <h2>Project Table</h2>
      <div>
        <table>
          <thead>
            <tr>
              <th>Project ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Manager ID</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((project, index) => (
              <tr key={index}>
                <td>{project.projectId}</td>
                <td>{project.name}</td>
                <td>{project.description}</td>
                <td>{project.managerId}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserProject;
