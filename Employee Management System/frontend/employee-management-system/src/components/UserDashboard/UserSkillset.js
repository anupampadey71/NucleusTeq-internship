import React, { useEffect, useState } from 'react';
import { getSkills } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const UserSkillset = () => {
  const [skills, setSkills] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await getSkills(user);
        setSkills(response.data);
      } catch (error) {
        console.error('Failed to fetch skills', error);
        alert('Failed to fetch skills. Please try again.');
      }
    };

    fetchSkills();
  }, [user]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div>
        <h2>Skillsets Table</h2>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div>
            {/* <h3>Skillsets</h3> */}
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
        </div>
      </div>
    </div>
  );
};

export default UserSkillset;
