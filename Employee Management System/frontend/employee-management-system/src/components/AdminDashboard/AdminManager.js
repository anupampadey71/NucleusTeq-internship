import React, { useState, useEffect } from 'react';
import { addManager, deleteManager, getManagers, updateManager, getManagerEmployees } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminManager = () => {
  const { user } = useAuth();
  const [managers, setManagers] = useState([]);
  const [managerId, setManagerId] = useState('');
  const [managerIdDelete, setManagerIdDelete] = useState('');
  const [managerIdUpdate, setManagerIdUpdate] = useState('');
  const [employeeId, setEmployeeId] = useState('');
  const [oldEmployeeId, setOldEmployeeId] = useState('');
  const [newEmployeeId, setNewEmployeeId] = useState('');
  const [managerEmployees, setManagerEmployees] = useState([]);
  const [addManagerId, setAddManagerId] = useState('');
  const [addEmployeeId, setAddEmployeeId] = useState('');
  const [refetch, setRefetch] = useState(false);

  
  const fetchManagers = async () => {
    try {
      const res = await getManagers(user);
      setManagers(res.data);
    } catch (error) {
      console.error('Failed to get managers:', error.response ? error.response.data : error.message);
      alert('Failed to get managers. Please try again.');
    }
  };

  const handleAddManager = async () => {
    try {
      const res = await addManager(addManagerId, addEmployeeId, user);
      console.log(res); // Handle success response
      setManagers(prevManagers => [...prevManagers, { managerId: addManagerId, employeeId: addEmployeeId }]);
      setAddManagerId('');
      setAddEmployeeId('');
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to add manager:', error.response ? error.response.data : error.message);
      alert('Failed to add manager. Please try again.');
    }
  };

  const handleGetManagerEmployees = async () => {
    try {
      const res = await getManagerEmployees(managerId, user);
      setManagerEmployees(res.data.employees);
    } catch (error) {
      console.error('Failed to get manager employees:', error.response ? error.response.data : error.message);
      alert('Failed to get manager employees. Please try again.');
    }
  };

  const handleUpdateManager = async () => {
    try {
      const res = await updateManager(managerIdUpdate, oldEmployeeId, newEmployeeId, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to update manager:', error.response ? error.response.data : error.message);
      alert('Failed to update manager. Please try again.');
    }
  };

  const handleDeleteManager = async () => {
    try {
      const res = await deleteManager(managerIdDelete, employeeId, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to delete manager:', error.response ? error.response.data : error.message);
      alert('Failed to delete manager. Please try again.');
    }
  };
  useEffect(() => {
    fetchManagers();
  }, [refetch]);

  return (
    <div>
      <h2>Manager Operations</h2>
      <div>
        <h3>Get Managers</h3>
        {managers.map((manager, index) => (
          <div key={index}>
            <p>Manager ID: {manager.ManagerId}</p>
            <p>Employee ID: {manager.employeeId}</p>
          </div>
        ))}
      </div>
      <div>
        <h3>Add Manager</h3>
        <input type="text" placeholder="Manager ID" value={addManagerId} onChange={(e) => setAddManagerId(e.target.value)} />
        <input type="text" placeholder="Employee ID" value={addEmployeeId} onChange={(e) => setAddEmployeeId(e.target.value)} />
        <button onClick={handleAddManager}>Add Manager</button>
      </div>
      
      <div>
        <h3>Update Manager</h3>
        <input type="text" placeholder="Manager ID" value={managerIdUpdate} onChange={(e) => setManagerIdUpdate(e.target.value)} />
        <input type="text" placeholder="Old Employee ID" value={oldEmployeeId} onChange={(e) => setOldEmployeeId(e.target.value)} />
        <input type="text" placeholder="New Employee ID" value={newEmployeeId} onChange={(e) => setNewEmployeeId(e.target.value)} />
        <button onClick={handleUpdateManager}>Update Manager</button>
      </div>
      <div>
        <h3>Delete Manager</h3>
        <input type="text" placeholder="Manager ID" value={managerIdDelete} onChange={(e) => setManagerIdDelete(e.target.value)} />
        <input type="text" placeholder="Employee ID" value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} />
        <button onClick={handleDeleteManager}>Delete Manager</button>
      </div>
      <div>
        <h3>Get Employees by Manager ID</h3>
        <input type="text" placeholder="Manager ID" value={managerId} onChange={(e) => setManagerId(e.target.value)} />
        <button onClick={handleGetManagerEmployees}>Get Employees</button>
        {managerEmployees.length > 0 && (
          <div>
            <h4>Employees under Manager ID: {managerId}</h4>
            <ul>
              {managerEmployees.map((employee, index) => (
                <li key={index}>{employee}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminManager;
