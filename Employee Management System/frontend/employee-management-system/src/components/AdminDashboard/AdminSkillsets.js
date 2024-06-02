import React, { useState, useEffect } from 'react';
import { addSkill, deleteSkill, getSkills, updateSkill } from '../../services/apiService';
import { useAuth } from '../../context/AuthContext';
import './AdminCss/AdminSkillset.css';

const AdminSkillset = () => {
  const { user } = useAuth();
  const [skills, setSkills] = useState([]);
  const [skillInfo, setSkillInfo] = useState({ skillId: '', skillName: '' });
  const [updateSkillInfo, setUpdateSkillInfo] = useState({ skillId: '', skillName: '' });
  const [deleteSkillId, setDeleteSkillId] = useState('');
  const [refetch, setRefetch] = useState(false);

  useEffect(() => {
    fetchSkills();
  }, [refetch]);

  const fetchSkills = async () => {
    try {
      const response = await getSkills(user);
      setSkills(response.data);
    } catch (error) {
      console.error('Failed to fetch skills', error);
    }
  };

  const handleSkillChange = (e) => {
    const { name, value } = e.target;
    setSkillInfo({ ...skillInfo, [name]: value });
  };

  const handleUpdateSkillChange = (e) => {
    const { name, value } = e.target;
    setUpdateSkillInfo({ ...updateSkillInfo, [name]: value });
  };

  const handleDeleteSkillChange = (e) => {
    setDeleteSkillId(e.target.value);
  };

  const handleAddSkill = async () => {
    if (!skillInfo.skillId || !skillInfo.skillName) {
      alert('Please fill all the info!');
      return;
    }
    try {
      await addSkill(skillInfo.skillId, skillInfo.skillName, user);
      setRefetch(!refetch);
      setSkillInfo({ skillId: '', skillName: '' });
    } catch (error) {
      console.error('Failed to add skill:', error.response ? error.response.data : error.message);
      alert('Failed to add skill. Please try again.');
    }
  };

  const handleUpdateSkill = async () => {
    if (!updateSkillInfo.skillId || !updateSkillInfo.skillName) {
      alert('Please fill all the info!');
      return;
    }
    try {
      await updateSkill(updateSkillInfo.skillId, updateSkillInfo.skillName, user);
      setRefetch(!refetch);
      setUpdateSkillInfo({ skillId: '', skillName: '' });
    } catch (error) {
      console.error('Failed to update skill:', error.response ? error.response.data : error.message);
      alert('Failed to update skill. Please try again.');
    }
  };

  const handleDeleteSkill = async () => {
    if (!deleteSkillId) {
      alert('Please fill all the info!');
      return;
    }
    try {
      await deleteSkill(deleteSkillId, user);
      setRefetch(!refetch);
      setDeleteSkillId('');
    } catch (error) {
      console.error('Failed to delete skill:', error.response ? error.response.data : error.message);
      alert('Failed to delete skill. Please try again.');
    }
  };

  return (
    <div className="admin-skillset-container">
      <div className="skillsets-list">
        <h3>Skillsets</h3>
        {skills.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Skill ID</th>
                <th>Skill Name</th>
              </tr>
            </thead>
            <tbody>
              {skills.map((skill) => (
                <tr key={skill.skillId}>
                  <td>{skill.skillId}</td>
                  <td>{skill.skillName}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No skills available.</p>
        )}
      </div>

      <div className="create-skillset">
        <h3>Add Skill</h3>
        <div>
          <input type="text" placeholder="Skill ID" value={skillInfo.skillId} onChange={handleSkillChange} name="skillId" />
          <br />
          <input type="text" placeholder="Skill Name" value={skillInfo.skillName} onChange={handleSkillChange} name="skillName" />
          <br />
          <button onClick={handleAddSkill}>Add Skill</button>
        </div>
      </div>

      <div className="update-skillset">
        <h3>Update Skill</h3>
        <div>
          <input type="text" placeholder="Skill ID" value={updateSkillInfo.skillId} onChange={handleUpdateSkillChange} name="skillId" />
          <br />
          <input type="text" placeholder="Skill Name" value={updateSkillInfo.skillName} onChange={handleUpdateSkillChange} name="skillName" />
          <br />
          <button onClick={handleUpdateSkill}>Update Skill</button>
        </div>
      </div>

      <div className="delete-skillset">
        <h3>Delete Skill</h3>
        <div>
          <input type="text" placeholder="Skill ID" value={deleteSkillId} onChange={handleDeleteSkillChange} name="skillId" />
          <br />
          <button onClick={handleDeleteSkill}>Delete Skill</button>
        </div>
      </div>
    </div>
  );
};

export default AdminSkillset;
