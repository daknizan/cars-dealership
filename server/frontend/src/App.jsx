import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealer/Dealer";
import PostReview from "./components/PostReview/PostReview";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setLoggedIn={setLoggedIn} setUserName={setUserName} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dealer/:id" element={<Dealer userName={userName} loggedIn={loggedIn} />} />
        <Route path="/postreview/:id" element={<PostReview userName={userName} />} />
        <Route path="/" element={<Dealers loggedIn={loggedIn} userName={userName} />} />
      </Routes>
    </Router>
  );
}

export default App;
