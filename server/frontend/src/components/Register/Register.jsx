import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const register = async (e) => {
    e.preventDefault();
    const res = await fetch("/djangoapp/registration", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, firstName, lastName, email, password }),
    });
    const json = await res.json();
    if (json.status === "Authenticated") {
      navigate("/login");
    } else {
      alert(json.error || "Registration failed");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "60px auto" }}>
      <h2>Register</h2>
      <form onSubmit={register}>
        <input placeholder="Username" value={userName} onChange={(e) => setUserName(e.target.value)} required />
        <input placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
        <input placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Register</button>
      </form>
      <p><a href="/login">Already have an account? Login</a></p>
    </div>
  );
};

export default Register;
