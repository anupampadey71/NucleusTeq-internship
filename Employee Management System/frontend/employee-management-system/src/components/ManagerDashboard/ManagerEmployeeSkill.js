import React, { useState, useEffect } from 'react';
import { getEmployeeSkills } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';

const ManagerEmployeeSkill = () => {
  const { user } = useAuth();
  const [employeeSkills, setEmployeeSkills] = useState([]);
  const [employeeId, setEmployeeId] = useState('');

  const fetchEmployeeSkills = async (employeeId) => {
    try {
      const res = await getEmployeeSkills(employeeId, user);
      setEmployeeSkills(res.data.skills);
    } catch (error) {
      console.error('Failed to get employee skills:', error.response ? error.response.data : error.message);
      alert('Failed to get employee skills. Please try again.');
    }
  };

  useEffect(() => {
    if (employeeId) {
      fetchEmployeeSkills(employeeId);
    }
  }, [employeeId]);

  return (
    <div>
      <h2>Skills of Each Employee under Manger</h2>
      <div>
        {/* <h3>Get Employee Skills</h3> */}
        <input 
          type="text" 
          placeholder="Employee ID" 
          value={employeeId} 
          onChange={(e) => setEmployeeId(e.target.value)} 
        />
        {/* <button onClick={() => fetchEmployeeSkills(employeeId)}>Get Skills</button> */}
        {employeeSkills.length > 0 && (
          <div>
            <h4>Skills for Employee ID: {employeeId}</h4>
            <ul>
              {employeeSkills.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ManagerEmployeeSkill;
