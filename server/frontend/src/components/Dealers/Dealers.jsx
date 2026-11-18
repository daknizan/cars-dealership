import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const Dealers = ({ loggedIn, userName }) => {
  const [dealers, setDealers] = useState([]);
  const [state, setState] = useState("");

  const fetchDealers = async (st) => {
    const url = st ? `/djangoapp/get_dealers/${st}` : "/djangoapp/get_dealers";
    const res = await fetch(url);
    const json = await res.json();
    setDealers(json.dealers || []);
  };

  useEffect(() => {
    fetchDealers("");
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchDealers(state);
  };

  const handleLogout = async () => {
    await fetch("/djangoapp/logout");
    window.location.href = "/";
  };

  return (
    <div>
      <nav style={{ background: "#0b3d91", padding: "14px 24px", display: "flex", gap: 20 }}>
        <span style={{ color: "#fff", fontWeight: 600 }}>🚗 Cars Dealership</span>
        <Link to="/" style={{ color: "#fff" }}>Home</Link>
        <a href="/About.html" style={{ color: "#fff" }}>About Us</a>
        <a href="/Contact.html" style={{ color: "#fff" }}>Contact Us</a>
        {loggedIn ? (
          <>
            <span style={{ color: "#fff" }}>👤 {userName}</span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <Link to="/login" style={{ color: "#fff" }}>Login</Link>
        )}
      </nav>
      <div style={{ maxWidth: 1000, margin: "30px auto", padding: "0 20px" }}>
        <h1>Dealers</h1>
        <form onSubmit={handleSearch} style={{ marginBottom: 20 }}>
          <input style={{ display: "inline", width: 200, marginRight: 10 }}
                 placeholder="Filter by state (e.g. Kansas)"
                 value={state} onChange={(e) => setState(e.target.value)} />
          <button type="submit">Search</button>
        </form>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr><th>ID</th><th>Name</th><th>City</th><th>State</th><th>Address</th><th>Zip</th><th></th></tr>
          </thead>
          <tbody>
            {dealers.map((d) => (
              <tr key={d.id}>
                <td>{d.id}</td><td>{d.full_name}</td><td>{d.city}</td>
                <td>{d.st}</td><td>{d.address}</td><td>{d.zip}</td>
                <td>
                  <Link to={`/dealer/${d.id}`}>Dealer Reviews</Link>
                  {loggedIn && <> | <Link to={`/postreview/${d.id}`}>Add Review</Link></>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dealers;
