import React, { createContext, useState, useContext, useEffect } from 'react';

// Create the Auth context
const AuthContext = createContext();

// Custom hook to use the Auth context
export const useAuth = () => {
  return useContext(AuthContext);
};

// AuthProvider component to wrap the app and provide auth state
export const AuthProvider = ({ children }) => {
  // Initialize state with user data from local storage if available
  const [user, setUser] = useState(() => {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  });

  // Function to handle user login
  const login = (userData) => {
    // Save user data to state and local storage
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  // Function to handle user logout
  const logout = () => {
    // Remove user data from state and local storage
    setUser(null);
    localStorage.removeItem('user');
  };

  // Use effect to sync state with local storage changes
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
