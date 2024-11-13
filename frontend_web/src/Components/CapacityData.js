// src/Components/CapacityData.js
import React, { useState, useEffect } from "react";
import LocationBox from "./LocationBox";
import "../styles/CapacityData.css";

// const SOCKET_IO_URL = "http://localhost:5000";

function CapacityData() {
  const [capacities, setCapacities] = useState({});

  useEffect(() => {
    // const socket = io(SOCKET_IO_URL);

    // socket.on("update_counts", (data) => {
    //   setCapacities((prevCapacities) => ({
    //     ...prevCapacities,
    //     [data.location]: { current: data.occupancy, total: data.totalCapacity },
    //   }));
    // });

    // return () => {
    //   socket.disconnect();
    // };

    const fakeCapacities = {
      "Clemons Library": { current: 250, total: 500 },
      "Shannon Library": { current: 150, total: 300 },
      "Mem Gym": { current: 100, total: 200 },
      "AFC Gym": { current: 300, total: 400 },
    };

    setCapacities(fakeCapacities);
  }, []);

  // Keeping the locations array for consistency
  const locations = [
    {
      name: "Clemons Library",
      image:
        "https://www.library.virginia.edu/sites/default/files/2023-06/Clemons-location.png",
      totalCapacity: 500,
    },
    {
      name: "Shannon Library",
      image:
        "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.virginia.edu%2Facademics%2Flibraries&psig=AOvVaw2tpSGvZzQEykEDTCpehNxM&ust=1729104190278000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCKC89ZqFkYkDFQAAAAAdAAAAABAE",
      totalCapacity: 300,
    },
    {
      name: "Mem Gym",
      image: "https://via.placeholder.com/150",
      totalCapacity: 200,
    },
    {
      name: "AFC Gym",
      image: "https://via.placeholder.com/150",
      totalCapacity: 400,
    },
  ];

  return (
    <div className="capacity-data">
      <h1>Building Capacity Tracker</h1>
      <div className="location-container">
        {locations.map((location, index) => (
          <LocationBox
            key={index}
            name={location.name}
            image={location.image}
            capacity={capacities[location.name]?.current || 0}
            totalCapacity={location.totalCapacity}
          />
        ))}
      </div>
    </div>
  );
}

export default CapacityData;
