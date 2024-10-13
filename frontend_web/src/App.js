// src/App.js
import React from "react";
import LocationBox from "./Components/LocationBox";

function App() {
  // Example data (capacity is set to N/A for now)
  const locations = [
    {
      name: "Clemons Library",
      image: "https://via.placeholder.com/150",
      capacity: "N/A",
    },
    {
      name: "Shannon Library",
      image: "https://via.placeholder.com/150",
      capacity: "N/A",
    },
    {
      name: "Mem Gym",
      image: "https://via.placeholder.com/150",
      capacity: "N/A",
    },
    {
      name: "AFC Gym",
      image: "https://via.placeholder.com/150",
      capacity: "N/A",
    },
  ];

  return (
    <div className="App">
      <h1>Building Capacity Tracker</h1>
      <div className="location-container">
        {locations.map((location, index) => (
          <LocationBox
            key={index}
            name={location.name}
            image={location.image}
            capacity={location.capacity}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
