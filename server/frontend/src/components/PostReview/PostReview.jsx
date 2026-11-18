import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const PostReview = ({ userName }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [review, setReview] = useState("");
  const [carMake, setCarMake] = useState("");
  const [carModel, setCarModel] = useState("");
  const [carYear, setCarYear] = useState(2025);

  const submit = async (e) => {
    e.preventDefault();
    const res = await fetch("/djangoapp/add_review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dealership: parseInt(id),
        review,
        car_make: carMake,
        car_model: carModel,
        car_year: carYear,
        purchase: true,
        purchase_date: new Date().toISOString().slice(0, 10),
      }),
    });
    const json = await res.json();
    if (json.status === 200) {
      navigate(`/dealer/${id}`);
    } else {
      alert(json.message || "Failed to post review");
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto" }}>
      <h2>Post a review for dealer #{id}</h2>
      <p>Posting as <strong>{userName}</strong></p>
      <form onSubmit={submit}>
        <textarea rows={4} placeholder="Your review" value={review}
                  onChange={(e) => setReview(e.target.value)} required style={{ width: "100%" }} />
        <input placeholder="Car make" value={carMake} onChange={(e) => setCarMake(e.target.value)} />
        <input placeholder="Car model" value={carModel} onChange={(e) => setCarModel(e.target.value)} />
        <input type="number" placeholder="Car year" value={carYear} onChange={(e) => setCarYear(e.target.value)} />
        <button type="submit">Submit review</button>
      </form>
    </div>
  );
};

export default PostReview;
