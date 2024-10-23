import React from "react";
import { useParams } from "react-router-dom";

function BuildingDetail() {
  const { name } = useParams();

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>{name}</h1>
      <p>This page is currently under construction.</p>
    </div>
  );
}

export default BuildingDetail;
