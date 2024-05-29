import React, { useEffect, useState } from 'react';
import { addDepartment, deleteDepartment, getDepartments, updateDepartment } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminDashboard = () => {
  const [departments, setDepartments] = useState([]);
  const { user } = useAuth();
  console.log("AdminDashboard", user)
  const [refetch, setRefetch] = useState(false);
  
  const [createInfo, setCreateInfo] = useState({
    id: '',
    name: '',
    managerId: ''
  })
  const [updateInfo, setUpdateInfo] = useState({
    id: '',
    name: '',
  })
  const [deleteInfo, setDeleteInfo] = useState({
    id: ''
  })
  
  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await getDepartments(user);
        setDepartments(response.data);
      } catch (error) {
        console.error('Failed to fetch departments', error);
      }
    };
    fetchDepartments();
  }, [user.token, refetch]);

  const handleCreateChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setCreateInfo({
        ...createInfo,
        [name]: value
    })
  }

  const handleUpdateChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setUpdateInfo({
        ...updateInfo,
        [name]: value
    })
  }
  const handleDeleteChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setDeleteInfo({
        ...deleteInfo,
        [name]: value
    })
  }

  const handleCreate = async () => {
    if (!createInfo.id || !createInfo.name || !createInfo.managerId) {
        alert('Please fill all the info!');
        return;
    }
    const res = await addDepartment(createInfo.id, createInfo.name, createInfo.managerId,user);
    setRefetch(!refetch);
  }

  const handleUpdate = async () => {
    if (!updateInfo.id || !updateInfo.name) {
        alert('Please fill all the info!');
        return;
    }
     const res = await updateDepartment(updateInfo.id, updateInfo.name,user);
     setRefetch(!refetch);
  }

  const handleDelete = async () => {
    if (!deleteInfo.id) {
      alert('Please fill all the info!');
      return;
    }
    const res = await deleteDepartment(deleteInfo.id,user);
    setRefetch(!refetch);
  }

  return (
    <div>
      <h2>Admin Dashboard</h2>
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

        <div>
            <p>Create department</p>
            <div>
                <input type='text' placeholder='Id' value={createInfo.id} onChange={handleCreateChange} 
                    name='id'
                /> 
                <br/>
                <input type='text' placeholder='Name' value={createInfo.name} onChange={handleCreateChange}
                    name='name'
                />
                <br/>
                <input type='text' placeholder='Manager Id' value={createInfo.managerId} onChange={handleCreateChange}
                    name='managerId'
                />
                <br/>

                <button onClick={handleCreate}>Create</button>
            </div>  
        </div>

        <div>
            <p>Update department</p>
            <div>
                <input type='text' placeholder='Id' value={updateInfo.id} onChange={handleUpdateChange} 
                    name='id'
                /> 
                <br/>
                <input type='text' placeholder='Name' value={updateInfo.name} onChange={handleUpdateChange}
                    name='name'
                />
                <br/>

                <button onClick={handleUpdate}>Update</button>
            </div>  
        </div>

        <div>
            <p>Delete department</p>
            <div>
                <input type='text' placeholder='Id' value={deleteInfo.id} onChange={handleDeleteChange} 
                    name='id'
                /> 
                <br/>
                <button onClick={handleDelete}>Delete</button>
        </div>
        </div>
    </div>
  );
};

export default AdminDashboard;