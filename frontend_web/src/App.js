// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CapacityData from "./Components/CapacityData";
import BuildingDetail from "./Components/BuildingDetail";
import "./styles/App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<CapacityData />} />
          <Route path="/building/:name" element={<BuildingDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
