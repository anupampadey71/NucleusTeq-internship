import React, { useEffect, useState } from 'react';
import { addDepartment, deleteDepartment, getDepartments, updateDepartment, getEmployees, addEmployee, updateEmployee, deleteEmployee } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminDashboard = () => {
  const [departments, setDepartments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const { user } = useAuth();
  console.log("AdminDashboard", user);
  const [refetch, setRefetch] = useState(false);

  const [createInfo, setCreateInfo] = useState({
    id: '',
    name: '',
    managerId: ''
  });
  const [updateInfo, setUpdateInfo] = useState({
    id: '',
    name: '',
  });
  const [deleteInfo, setDeleteInfo] = useState({
    id: ''
  });

  const [employeeInfo, setEmployeeInfo] = useState({
    employeeId: '',
    email: '',
    name: '',
    salary: '',
    role: '',
    is_assigned: false,
  });

  const [updateEmployeeInfo, setUpdateEmployeeInfo] = useState({
    employeeId: '',
    email: '',
    name: '',
    salary: '',
    role: '',
    is_assigned: false,
  });

  const [deleteEmployeeId, setDeleteEmployeeId] = useState('');

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await getDepartments(user);
        setDepartments(response.data);
      } catch (error) {
        console.error('Failed to fetch departments', error);
      }
    };

    const fetchEmployees = async () => {
      try {
        const response = await getEmployees(user);
        setEmployees(response.data);
      } catch (error) {
        console.error('Failed to fetch employees', error);
      }
    };

    fetchDepartments();
    fetchEmployees();
  }, [user.token, refetch]);

  const handleCreateChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setCreateInfo({
      ...createInfo,
      [name]: value
    });
  };

  const handleUpdateChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setUpdateInfo({
      ...updateInfo,
      [name]: value
    });
  };

  const handleDeleteChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setDeleteInfo({
      ...deleteInfo,
      [name]: value
    });
  };

  const handleEmployeeChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setEmployeeInfo({
      ...employeeInfo,
      [name]: value
    });
  };

  const handleUpdateEmployeeChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setUpdateEmployeeInfo({
      ...updateEmployeeInfo,
      [name]: value
    });
  };

  const handleDeleteEmployeeChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setDeleteEmployeeId(value);
  };

  const handleCreate = async () => {
    if (!createInfo.id || !createInfo.name || !createInfo.managerId) {
      alert('Please fill all the info!');
      return;
    }
    const res = await addDepartment(createInfo.id, createInfo.name, createInfo.managerId, user);
    setRefetch(!refetch);
  };

  const handleUpdate = async () => {
    if (!updateInfo.id || !updateInfo.name) {
      alert('Please fill all the info!');
      return;
    }
    try {
      console.log('Attempting to update department:', updateInfo.id, updateInfo.name);
      const res = await updateDepartment(updateInfo.id, updateInfo.name, user);
      console.log('Department updated successfully:', res.data);
      setRefetch(!refetch);
      setUpdateInfo({ id: '', name: '' });
    } catch (error) {
      console.error('Failed to update department:', error.response ? error.response.data : error.message);
      alert('Failed to update department. Please try again.');
    }
  };

  const handleDelete = async () => {
    if (!deleteInfo.id) {
      alert('Please fill all the info!');
      return;
    }
    const res = await deleteDepartment(deleteInfo.id, user);
    setRefetch(!refetch);
  };

  const handleAddEmployee = async () => {
    try {
      const res = await addEmployee(employeeInfo.employeeId, employeeInfo.email, employeeInfo.name, employeeInfo.salary, employeeInfo.role, user);
      console.log('Employee added successfully:', res.data);
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to add employee:', error.response ? error.response.data : error.message);
      alert('Failed to add employee. Please try again.');
    }
  };

  const handleUpdateEmployee = async () => {
    try {
      const res = await updateEmployee(updateEmployeeInfo.employeeId, updateEmployeeInfo.email, updateEmployeeInfo.name, updateEmployeeInfo.salary, updateEmployeeInfo.role, updateEmployeeInfo.is_assigned, user);
      console.log('Employee updated successfully:', res.data);
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to update employee:', error.response ? error.response.data : error.message);
      alert('Failed to update employee. Please try again.');
    }
  };

  const handleDeleteEmployee = async () => {
    try {
      const res = await deleteEmployee(deleteEmployeeId, user);
      console.log('Employee deleted successfully:', res.data);
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to delete employee:', error.response ? error.response.data : error.message);
      alert('Failed to delete employee. Please try again.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div>
        <h2>Admin Dashboard</h2>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
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
            <div>
              <p>Create department</p>
              <div>
                <input type='text' placeholder='Id' value={createInfo.id} onChange={handleCreateChange} name='id' />
                <br />
                <input type='text' placeholder='Name' value={createInfo.name} onChange={handleCreateChange} name='name' />
                <br />
                <input type='text' placeholder='Manager Id' value={createInfo.managerId} onChange={handleCreateChange} name='managerId' />
                <br />
                <button onClick={handleCreate}>Create</button>
              </div>
            </div>

            <div>
              <p>Update department</p>
              <div>
                <input type='text' placeholder='Id' value={updateInfo.id} onChange={handleUpdateChange} name='id' />
                <br />
                <input type='text' placeholder='Name' value={updateInfo.name} onChange={handleUpdateChange} name='name' />
                <br />
                <button onClick={handleUpdate}>Update</button>
              </div>
            </div>

            <div>
              <p>Delete department</p>
              <div>
                <input type='text' placeholder='Id' value={deleteInfo.id} onChange={handleDeleteChange} name='id' />
                <br />
                <button onClick={handleDelete}>Delete</button>
              </div>
            </div>
          </div>

          <div>
            <h3>Employees</h3>
            {employees.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Employee ID</th>
                    <th>Email</th>
                    <th>Name</th>
                    <th>Salary</th>
                    <th>Role</th>
                    <th>Is Assigned</th>
                  </tr>
                </thead>
                <tbody>
                  {employees.map((emp) => (
                    <tr key={emp.employeeId}>
                      <td>{emp.employeeId}</td>
                      <td>{emp.email}</td>
                      <td>{emp.name}</td>
                      <td>{emp.salary}</td>
                      <td>{emp.role}</td>
                      <td>{emp.is_assigned ? 'Yes' : 'No'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No employees available.</p>
            )}
            <div>
              <h3>Add Employee</h3>
              <p>Add Employee</p>
              <div>
                <input type='text' placeholder='Employee Id' value={employeeInfo.employeeId} onChange={handleEmployeeChange} name='employeeId' />
                <br />
                <input type='text' placeholder='Email' value={employeeInfo.email} onChange={handleEmployeeChange} name='email' />
                <br />
                <input type='text' placeholder='Name' value={employeeInfo.name} onChange={handleEmployeeChange} name='name' />
                <br />
                <input type='text' placeholder='Salary' value={employeeInfo.salary} onChange={handleEmployeeChange} name='salary' />
                <br />
                <input type='text' placeholder='Role' value={employeeInfo.role} onChange={handleEmployeeChange} name='role' />
                <br />
                <button onClick={handleAddEmployee}>Add Employee</button>
              </div>
            </div>

            <div>
              <h3>Update Employee</h3>
              <div>
                <input type='text' placeholder='Employee Id' value={updateEmployeeInfo.employeeId} onChange={handleUpdateEmployeeChange} name='employeeId' />
                <br />
                <input type='text' placeholder='Email' value={updateEmployeeInfo.email} onChange={handleUpdateEmployeeChange} name='email' />
                <br />
                <input type='text' placeholder='Name' value={updateEmployeeInfo.name} onChange={handleUpdateEmployeeChange} name='name' />
                <br />
                <input type='text' placeholder='Salary' value={updateEmployeeInfo.salary} onChange={handleUpdateEmployeeChange} name='salary' />
                <br />
                <input type='text' placeholder='Role' value={updateEmployeeInfo.role} onChange={handleUpdateEmployeeChange} name='role' />
                <br />
                <label>
                  is_assigned:
                  <input type='checkbox' checked={updateEmployeeInfo.is_assigned} onChange={handleUpdateEmployeeChange} name='is_assigned' />
                </label>
                <br />
                <button onClick={handleUpdateEmployee}>Update Employee</button>
              </div>
            </div>

            <div>
              <h3>Delete Employee</h3>
              <div>
                <input type='text' placeholder='Employee Id' value={deleteEmployeeId} onChange={handleDeleteEmployeeChange} name='employeeId' />
                <br />
                <button onClick={handleDeleteEmployee}>Delete Employee</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
