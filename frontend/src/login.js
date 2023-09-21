import React, { useState } from "react";
import Dashboard from "./dashboard";
import './login.css'
import { useNavigate, Link } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [username, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSignup, setIsSignup] = useState(false);
  const [authenticated, setauthenticated] = useState(localStorage.getItem(localStorage.getItem("authenticated")|| false));
  const users = [{ username: "admin@gmail.com", password: "testpassword" }];
  const handleSubmit = (e) => {
    e.preventDefault()
    const account = users.find((user) => user.username === username);
    if (account && account.password === password) {
        localStorage.setItem("authenticated", true);
        navigate("/dashboard");
    }
  };
  return (
    <div className="container">
    <div className="card">
      <h1>OurHour</h1>
      <h2>{isSignup ? 'Sign Up' : 'Login'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input 
            type="email" 
            id="email" 
            value={username} 
            onChange={(e) => setEmail(e.target.value)} 
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input 
            type="password" 
            name="Password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required
          />
        </div>
        <button type="submit">{isSignup ? 'Sign Up' : 'Login'}</button>
      </form>
      <p>{isSignup ? 'Have an account?' : "Don't have an account?"} <a href="#" onClick={() => setIsSignup(!isSignup)}>{isSignup ? 'Login' : 'Sign Up'}</a></p>
      <p>
          Are you a student? <Link to="/ticket">Create Ticket</Link>
      </p>
    </div>
  </div>
  );
}

export default Login;
