import React, { useState, useEffect } from 'react';
import { getEmployeeSkills } from '../../services/apiService'; // Adjusted import path
import { useAuth } from '../../context/AuthContext';
import './ManagerCss/ManagerEmployeeSkill.css';

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
    <div className="manager-employee-skill-container">
      <h2>Skills of Each Employee under Manager</h2>
      <div className="employee-skill-search">
        <input 
          type="text" 
          placeholder="Employee ID" 
          value={employeeId} 
          onChange={(e) => setEmployeeId(e.target.value)} 
        />
      </div>
      {employeeSkills.length > 0 && (
        <div className="employee-skill-list">
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
  );
};

export default ManagerEmployeeSkill;
