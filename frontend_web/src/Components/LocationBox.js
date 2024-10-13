import React from "react";
import "../styles/LocationBox.css";

function LocationBox({ name, image, capacity }) {
  return (
    <div className="location-box">
      <h2>{name}</h2>
      <div className="image-placeholder">
        <img src={image} alt={name} />
      </div>
      <p>Capacity: {capacity ? capacity : "N/A"}</p>
    </div>
  );
}

export default LocationBox;
