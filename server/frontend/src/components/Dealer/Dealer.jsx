import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

const Dealer = ({ userName, loggedIn }) => {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch(`/djangoapp/dealer/${id}`).then((r) => r.json()).then((j) => setDealer(j.dealer));
    fetch(`/djangoapp/reviews/dealer/${id}`).then((r) => r.json()).then((j) => setReviews(j.reviews || []));
  }, [id]);

  if (!dealer) return <p style={{ padding: 30 }}>Loading...</p>;

  return (
    <div style={{ maxWidth: 900, margin: "30px auto", padding: "0 20px" }}>
      <p><Link to="/">← Back to Dealers</Link></p>
      <h1>{dealer.full_name}</h1>
      <p>{dealer.address}, {dealer.city}, {dealer.st} {dealer.zip}</p>
      <h2>Reviews</h2>
      {loggedIn && <p><Link to={`/postreview/${id}`}>Post a review</Link> (logged in as {userName})</p>}
      {reviews.length === 0 && <p>No reviews yet.</p>}
      {reviews.map((r) => (
        <div key={r.id} style={{ background: "#fff", borderRadius: 8, padding: 16, marginBottom: 12, boxShadow: "0 2px 8px rgba(0,0,0,.08)" }}>
          <p><strong>{r.name}</strong> — {r.car_make} {r.car_model} {r.car_year}</p>
          <p>{r.review}</p>
          <p className={`sentiment-${r.sentiment}`}>Sentiment: {r.sentiment}</p>
        </div>
      ))}
    </div>
  );
};

export default Dealer;
