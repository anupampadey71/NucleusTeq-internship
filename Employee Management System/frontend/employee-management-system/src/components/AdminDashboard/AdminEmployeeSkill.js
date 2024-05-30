import React, { useState } from 'react';
import { addSkill, updateSkill, deleteSkill } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminEmployeeSkill = () => {
  const { user } = useAuth();
  const [employeeId, setEmployeeId] = useState('');
  const [currentSkillId, setCurrentSkillId] = useState('');
  const [newSkillId, setNewSkillId] = useState('');

  const handleAddSkill = async () => {
    try {
      await addSkill(employeeId, newSkillId, user);
      // Clear input fields after successful addition
      setEmployeeId('');
      setNewSkillId('');
    } catch (error) {
      console.error('Failed to add skill:', error.response ? error.response.data : error.message);
      alert('Failed to add skill. Please try again.');
    }
  };

  const handleUpdateSkill = async () => {
    try {
      await updateSkill(employeeId, currentSkillId, newSkillId, user);
      // Clear input fields after successful update
      setEmployeeId('');
      setCurrentSkillId('');
      setNewSkillId('');
    } catch (error) {
      console.error('Failed to update skill:', error.response ? error.response.data : error.message);
      alert('Failed to update skill. Please try again.');
    }
  };

  const handleDeleteSkill = async () => {
    try {
      await deleteSkill(employeeId, currentSkillId, user);
      // Clear input fields after successful deletion
      setEmployeeId('');
      setCurrentSkillId('');
    } catch (error) {
      console.error('Failed to delete skill:', error.response ? error.response.data : error.message);
      alert('Failed to delete skill. Please try again.');
    }
  };

  return (
    <div>
      <div>
        <h3>Add Skill</h3>
        <div>
          <input type='text' placeholder='Employee ID' value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} />
          <br />
          <input type='text' placeholder='Skill ID' value={newSkillId} onChange={(e) => setNewSkillId(e.target.value)} />
          <br />
          <button onClick={handleAddSkill}>Add Skill</button>
        </div>
      </div>

      <div>
        <h3>Update Skill</h3>
        <div>
          <input type='text' placeholder='Employee ID' value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} />
          <br />
          <input type='text' placeholder='Current Skill ID' value={currentSkillId} onChange={(e) => setCurrentSkillId(e.target.value)} />
          <br />
          <input type='text' placeholder='New Skill ID' value={newSkillId} onChange={(e) => setNewSkillId(e.target.value)} />
          <br />
          <button onClick={handleUpdateSkill}>Update Skill</button>
        </div>
      </div>

      <div>
        <h3>Delete Skill</h3>
        <div>
          <input type='text' placeholder='Employee ID' value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} />
          <br />
          <input type='text' placeholder='Skill ID' value={currentSkillId} onChange={(e) => setCurrentSkillId(e.target.value)} />
          <br />
          <button onClick={handleDeleteSkill}>Delete Skill</button>
        </div>
      </div>
    </div>
  );
};

export default AdminEmployeeSkill;
