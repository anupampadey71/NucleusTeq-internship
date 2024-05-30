import React, { useState, useEffect } from 'react';
import { addDepartment, deleteDepartment, getDepartments, updateDepartment } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminDepartment = () => {
  const { user } = useAuth();
  const [departments, setDepartments] = useState([]);
  const [createInfo, setCreateInfo] = useState({ id: '', name: '', managerId: '' });
  const [updateInfo, setUpdateInfo] = useState({ id: '', name: '' });
  const [deleteInfo, setDeleteInfo] = useState({ id: '' });

  useEffect(() => {
    fetchDepartments();
  }, []);

  const fetchDepartments = async () => {
    try {
      const response = await getDepartments(user);
      setDepartments(response.data);
    } catch (error) {
      console.error('Failed to fetch departments', error);
    }
  };

  const handleCreate = async () => {
    if (!createInfo.id || !createInfo.name || !createInfo.managerId) {
      alert('Please fill all the info!');
      return;
    }
    try {
      await addDepartment(createInfo.id, createInfo.name, createInfo.managerId, user);
      fetchDepartments();
      setCreateInfo({ id: '', name: '', managerId: '' });
    } catch (error) {
      console.error('Failed to create department:', error);
      alert('Failed to create department. Please try again.');
    }
  };

  const handleUpdate = async () => {
    if (!updateInfo.id || !updateInfo.name) {
      alert('Please fill all the info!');
      return;
    }
    try {
      await updateDepartment(updateInfo.id, updateInfo.name, user);
      fetchDepartments();
      setUpdateInfo({ id: '', name: '' });
    } catch (error) {
      console.error('Failed to update department:', error);
      alert('Failed to update department. Please try again.');
    }
  };

  const handleDelete = async () => {
    if (!deleteInfo.id) {
      alert('Please fill all the info!');
      return;
    }
    try {
      await deleteDepartment(deleteInfo.id, user);
      fetchDepartments();
      setDeleteInfo({ id: '' });
    } catch (error) {
      console.error('Failed to delete department:', error);
      alert('Failed to delete department. Please try again.');
    }
  };

  const handleCreateChange = (e) => {
    const { name, value } = e.target;
    setCreateInfo({ ...createInfo, [name]: value });
  };

  const handleUpdateChange = (e) => {
    const { name, value } = e.target;
    setUpdateInfo({ ...updateInfo, [name]: value });
  };

  const handleDeleteChange = (e) => {
    const { name, value } = e.target;
    setDeleteInfo({ ...deleteInfo, [name]: value });
  };

  return (
    <div>
      <div>
        <h3>Departments</h3>
        {departments.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Department ID</th>
                <th>Name</th>
                <th>Manager ID</th>
              </tr>
            </thead>
            <tbody>
              {departments.map((dept) => (
                <tr key={dept.departmentId}>
                  <td>{dept.departmentId}</td>
                  <td>{dept.name}</td>
                  <td>{dept.ManagerId}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No departments available.</p>
        )}
      </div>

      <div>
        <h3>Create Department</h3>
        <div>
          <input type='text' placeholder='ID' value={createInfo.id} onChange={handleCreateChange} name='id' />
          <br />
          <input type='text' placeholder='Name' value={createInfo.name} onChange={handleCreateChange} name='name' />
          <br />
          <input type='text' placeholder='Manager ID' value={createInfo.managerId} onChange={handleCreateChange} name='managerId' />
          <br />
          <button onClick={handleCreate}>Create</button>
        </div>
      </div>

      <div>
        <h3>Update Department</h3>
        <div>
          <input type='text' placeholder='Department Id' value={updateInfo.id} onChange={handleUpdateChange} name='id' />
          <br />
          <input type='text' placeholder='Name' value={updateInfo.name} onChange={handleUpdateChange} name='name' />
          <br />
          <button onClick={handleUpdate}>Update</button>
        </div>
      </div>

      <div>
        <h3>Delete Department</h3>
        <div>
          <input type='text' placeholder='Department Id' value={deleteInfo.id} onChange={handleDeleteChange} name='id' />
          <br />
          <button onClick={handleDelete}>Delete</button>
        </div>
      </div>
    </div>
  );
};

export default AdminDepartment;