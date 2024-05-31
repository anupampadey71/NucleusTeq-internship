import React, { useState, useEffect } from 'react';
import { addProject, deleteProject, getAllProjects, updateProject } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminProject = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [projectId, setProjectId] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [managerId, setManagerId] = useState('');
  const [projectIdToDelete, setProjectIdToDelete] = useState('');
  const [projectIdToUpdate, setProjectIdToUpdate] = useState('');
  const [newName, setNewName] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newManagerId, setNewManagerId] = useState('');
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

  const handleAddProject = async () => {
    try {
      const projectData = {
        projectId,
        name,
        description,
        managerId
      };
      const res = await addProject(projectData, user);
      console.log(res); // Handle success response
      setProjects(prevProjects => [...prevProjects, projectData]);
      setProjectId('');
      setName('');
      setDescription('');
      setManagerId('');
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to add project:', error.response ? error.response.data : error.message);
      alert('Failed to add project. Please try again.');
    }
  };


  const handleUpdateProject = async () => {
    try {
      const projectData = {
        name: newName,
        description: newDescription,
        managerId: newManagerId
      };
      const res = await updateProject(projectIdToUpdate, projectData, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to update project:', error.response ? error.response.data : error.message);
      alert('Failed to update project. Please try again.');
    }
  };

  const handleDeleteProject = async () => {
    try {
      const res = await deleteProject(projectIdToDelete, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to delete project:', error.response ? error.response.data : error.message);
      alert('Failed to delete project. Please try again.');
    }
  };

  useEffect(() => {
    fetchAllProjects();
  }, [refetch]);

  return (
    <div>
      <h2>Project Operations</h2>
      <div>
        <h3>Get All Projects</h3>
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
      <div>
        <h3>Add Project</h3>
        <input 
          type="text" 
          placeholder="Project ID" 
          value={projectId} 
          onChange={(e) => setProjectId(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="Name" 
          value={name} 
          onChange={(e) => setName(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="Description" 
          value={description} 
          onChange={(e) => setDescription(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="Manager ID" 
          value={managerId} 
          onChange={(e) => setManagerId(e.target.value)} 
        />
        <button onClick={handleAddProject}>Add Project</button>
      </div>
      <div>
        <h3>Update Project</h3>
        <input 
          type="text" 
          placeholder="Project ID" 
          value={projectIdToUpdate} 
          onChange={(e) => setProjectIdToUpdate(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="New Name" 
          value={newName} 
          onChange={(e) => setNewName(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="New Description" 
          value={newDescription} 
          onChange={(e) => setNewDescription(e.target.value)} 
        />
        <input 
          type="text" 
          placeholder="New Manager ID" 
          value={newManagerId} 
          onChange={(e) => setNewManagerId(e.target.value)} 
        />
        <button onClick={handleUpdateProject}>Update Project</button>
      </div>
      <div>
        <h3>Delete Project</h3>
        <input 
          type="text" 
          placeholder="Project ID" 
          value={projectIdToDelete} 
          onChange={(e) => setProjectIdToDelete(e.target.value)} 
        />
        <button onClick={handleDeleteProject}>Delete Project</button>
      </div>
    </div>
  );
};

export default AdminProject;
