import React, { useState, useContext } from "react";
import axiosClient from "../api/axiosClient.js";
import { AuthContext } from "../auth/AuthContext.jsx";

function LoginPage({ onLogin }) {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(`[ACTION] Attempting login for user: ${username}`);
    try {
      const res = await axiosClient.post("/auth/login", { username, password });
      login(res.data.token);
      console.log("[SUCCESS] Login successful, token received.");
      onLogin();
    } catch (err) {
      console.error(
        "[ERROR] Login failed:",
        err.response ? err.response.data : err.message
      );
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginPage;
