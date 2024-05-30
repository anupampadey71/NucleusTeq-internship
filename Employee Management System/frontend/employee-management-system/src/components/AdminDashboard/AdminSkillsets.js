import React, { useEffect, useState } from 'react';
import {
  getSkills,
  addSkill,
  updateSkill,
  deleteSkill,
} from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const AdminSkillset = () => {
  const [skills, setSkills] = useState([]);
  const { user } = useAuth();
  const [refetch, setRefetch] = useState(false);

  const [skillInfo, setSkillInfo] = useState({
    skillId: '',
    skillName: '',
  });

  const [updateSkillInfo, setUpdateSkillInfo] = useState({
    skillId: '',
    skillName: '',
  });

  const [deleteSkillId, setDeleteSkillId] = useState('');

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await getSkills(user);
        setSkills(response.data);
      } catch (error) {
        console.error('Failed to fetch skills', error);
      }
    };

    fetchSkills();
  }, [user, refetch]);

  const handleSkillChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setSkillInfo({
      ...skillInfo,
      [name]: value
    });
  };

  const handleUpdateSkillChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setUpdateSkillInfo({
      ...updateSkillInfo,
      [name]: value
    });
  };

  const handleDeleteSkillChange = (e) => {
    const value = e.target.value;
    setDeleteSkillId(value);
  };

  const handleAddSkill = async () => {
    if (!skillInfo.skillId || !skillInfo.skillName) {
      alert('Please fill all the info!');
      return;
    }
    try {
      const res = await addSkill(skillInfo.skillId, skillInfo.skillName, user);
      setRefetch(!refetch);
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
      const res = await updateSkill(updateSkillInfo.skillId, updateSkillInfo.skillName, user);
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
      const res = await deleteSkill(deleteSkillId, user);
      setRefetch(!refetch);
    } catch (error) {
      console.error('Failed to delete skill:', error.response ? error.response.data : error.message);
      alert('Failed to delete skill. Please try again.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div>
        <h2>Admin Skillset Management</h2>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div>
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

          <div>
            <h3>Add Skill</h3>
            <div>
              <input type='text' placeholder='Skill Id' value={skillInfo.skillId} onChange={handleSkillChange} name='skillId' />
              <br />
              <input type='text' placeholder='Skill Name' value={skillInfo.skillName} onChange={handleSkillChange} name='skillName' />
              <br />
              <button onClick={handleAddSkill}>Add Skill</button>
            </div>
          </div>

          <div>
            <h3>Update Skill</h3>
            <div>
              <input type='text' placeholder='Skill Id' value={updateSkillInfo.skillId} onChange={handleUpdateSkillChange} name='skillId' />
              <br />
              <input type='text' placeholder='Skill Name' value={updateSkillInfo.skillName} onChange={handleUpdateSkillChange} name='skillName' />
              <br />
              <button onClick={handleUpdateSkill}>Update Skill</button>
            </div>
          </div>

          <div>
            <h3>Delete Skill</h3>
            <div>
              <input type='text' placeholder='Skill Id' value={deleteSkillId} onChange={handleDeleteSkillChange} name='skillId' />
              <br />
              <button onClick={handleDeleteSkill}>Delete Skill</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminSkillset;
