import React, { useState, useEffect } from 'react';
import { addEmployeeSkill, deleteEmployeeSkill, getEmployeeSkills, updateEmployeeSkill } from '../../services/apiService';
import { useAuth } from '../../context/AuthContext';
import './UserCss/UserEmployeeSkill.css'; // Import CSS file

const UserEmployeeSkill = () => {
  const { user } = useAuth();
  const [employeeSkills, setEmployeeSkills] = useState([]);
  const [employeeId, setEmployeeId] = useState('');
  const [currentSkillId, setCurrentSkillId] = useState('');
  const [newSkillId, setNewSkillId] = useState('');
  const [employeeIdToAdd, setEmployeeIdToAdd] = useState('');
  const [skillIdToAdd, setSkillIdToAdd] = useState('');
  const [employeeIdToUpdate, setEmployeeIdToUpdate] = useState('');
  const [employeeIdToDelete, setEmployeeIdToDelete] = useState('');
  const [skillIdToDelete, setSkillIdToDelete] = useState('');
  const [refetch, setRefetch] = useState(false);

  const fetchEmployeeSkills = async () => {
    try {
      const res = await getEmployeeSkills(employeeId, user);
      setEmployeeSkills(res.data.skills);
    } catch (error) {
      console.error('Failed to get employee skills:', error.response ? error.response.data : error.message);
      alert('Failed to get employee skills. Please try again.');
    }
  };

  const handleAddEmployeeSkill = async () => {
    try {
      const res = await addEmployeeSkill(employeeIdToAdd, skillIdToAdd, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
      setEmployeeIdToAdd('');
      setSkillIdToAdd('');
    } catch (error) {
      console.error('Failed to add employee skill:', error.response ? error.response.data : error.message);
      alert('Failed to add employee skill. Please try again.');
    }
  };

  const handleUpdateEmployeeSkill = async () => {
    try {
      const res = await updateEmployeeSkill(employeeIdToUpdate, currentSkillId, newSkillId, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
      setEmployeeIdToUpdate('');
      setCurrentSkillId('');
      setNewSkillId('');
    } catch (error) {
      console.error('Failed to update employee skill:', error.response ? error.response.data : error.message);
      alert('Failed to update employee skill. Please try again.');
    }
  };

  const handleDeleteEmployeeSkill = async () => {
    try {
      const res = await deleteEmployeeSkill(employeeIdToDelete, skillIdToDelete, user);
      console.log(res); // Handle success response
      setRefetch(!refetch);
      setEmployeeIdToDelete('');
      setSkillIdToDelete('');
    } catch (error) {
      console.error('Failed to delete employee skill:', error.response ? error.response.data : error.message);
      alert('Failed to delete employee skill. Please try again.');
    }
  };

  useEffect(() => {
    if (refetch) {
      fetchEmployeeSkills();
    }
  }, [refetch]);

  return (
    <div className="user-employee-skill-container">
      <h2>Employee Skills</h2>
      <div>
        <h3>Employee Skills by Employee ID</h3>
        <input 
          type="text" 
          placeholder="Employee ID" 
          value={employeeId} 
          onChange={(e) => setEmployeeId(e.target.value)} 
        />
        <button onClick={fetchEmployeeSkills}>Get Skills</button>
        {employeeSkills.length > 0 && (
          <div>
            <h4>Skills for Employee ID: {employeeId}</h4>
            <table>
              <thead>
                <tr>
                  <th>Skill</th>
                </tr>
              </thead>
              <tbody>
                {employeeSkills.map((skill, index) => (
                  <tr key={index}>
                    <td>{skill}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <div className="employee-actions-container">
        <div>
          <h3>Add Employee Skills</h3>
          <input 
            type="text" 
            placeholder="Employee ID" 
            value={employeeIdToAdd} 
            onChange={(e) => setEmployeeIdToAdd(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="Skill ID" 
            value={skillIdToAdd} 
            onChange={(e) => setSkillIdToAdd(e.target.value)} 
          />
          <button onClick={handleAddEmployeeSkill}>Add Skill</button>
        </div>
        <div>
          <h3>Update Employee Skills</h3>
          <input 
            type="text" 
            placeholder="Employee ID" 
            value={employeeIdToUpdate} 
            onChange={(e) => setEmployeeIdToUpdate(e.target.value)}  
          />
          <input 
            type="text" 
            placeholder="Current Skill ID" 
            value={currentSkillId} 
            onChange={(e) => setCurrentSkillId(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="New Skill ID" 
            value={newSkillId} 
            onChange={(e) => setNewSkillId(e.target.value)} 
          />
          <button onClick={handleUpdateEmployeeSkill}>Update Skill</button>
        </div>
        <div>
          <h3>Delete Employee Skills</h3>
          <input 
            type="text" 
            placeholder="Employee ID" 
            value={employeeIdToDelete} 
            onChange={(e) => setEmployeeIdToDelete(e.target.value)} 
          />
          <input 
            type="text" 
            placeholder="Skill ID" 
            value={skillIdToDelete} 
            onChange={(e) => setSkillIdToDelete(e.target.value)} 
          />
          <button onClick={handleDeleteEmployeeSkill}>Delete Skill</button>
        </div>
      </div>
    </div>
  );
};

export default UserEmployeeSkill;
