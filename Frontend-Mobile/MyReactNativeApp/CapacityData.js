// src/Components/CapacityData.js
import React from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";

function CapacityData({ navigation }) {
  const buildings = [
    { name: "Clemons Library" },
    { name: "Shannon Library" },
    { name: "Mem Gym" },
    { name: "AFC Gym" },
  ];

  return (
    <ScrollView>
      <View style={styles.container}>
        {buildings.map((building, index) => (
          <View key={index} style={styles.buildingContainer}>
            <Text style={styles.buildingName}>{building.name}</Text>
            <Button
              title="View Details"
              onPress={() =>
                navigation.navigate("BuildingDetail", { name: building.name })
              }
            />
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  buildingContainer: {
    marginBottom: 15,
    padding: 15,
    backgroundColor: "#f0f0f0",
    borderRadius: 8,
  },
  buildingName: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
  },
});

export default CapacityData;
