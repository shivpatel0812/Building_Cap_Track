import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/LocationBox.css";

function LocationBox({ name, image, capacity, totalCapacity }) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/building/${name}`);
  };

  const capacityPercentage = Math.round((capacity / totalCapacity) * 100);

  return (
    <div className="location-box" onClick={handleClick}>
      <div className="location-image">
        <img src={image} alt={name} />
      </div>
      <div className="location-details">
        <h2>{name}</h2>
      </div>
      <div className="capacity-graph">
        <div className="bar-background">
          <div className="bar-fill" style={{ width: `${capacityPercentage}%` }}>
            {capacity}/{totalCapacity} ({capacityPercentage}%)
          </div>
        </div>
      </div>
    </div>
  );
}

export default LocationBox;
