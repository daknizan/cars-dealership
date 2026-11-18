import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = ({ setLoggedIn, setUserName }) => {
  const [user, setUser] = useState("");
  const [pwd, setPwd] = useState("");
  const navigate = useNavigate();

  const login = async (e) => {
    e.preventDefault();
    const res = await fetch("/djangoapp/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName: user, password: pwd }),
    });
    const json = await res.json();
    if (json.status === "Authenticated") {
      setLoggedIn(true);
      setUserName(user);
      navigate("/");
    } else {
      alert("Login failed");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "60px auto" }}>
      <h2>Login</h2>
      <form onSubmit={login}>
        <input placeholder="Username" value={user} onChange={(e) => setUser(e.target.value)} />
        <input type="password" placeholder="Password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      <p><a href="/register">Don't have an account? Register</a></p>
    </div>
  );
};

export default Login;
