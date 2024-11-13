// src/Components/LocationBox.js (React Native version)
import React from "react";
import { View, Text, Image, TouchableOpacity, StyleSheet } from "react-native";

function LocationBox({ name, image, capacity, totalCapacity, onPress }) {
  const capacityPercentage = Math.round((capacity / totalCapacity) * 100);

  return (
    <TouchableOpacity style={styles.locationBox} onPress={onPress}>
      <Image style={styles.locationImage} source={{ uri: image }} />
      <View style={styles.locationDetails}>
        <Text style={styles.nameText}>{name}</Text>
        <View style={styles.capacityGraph}>
          <View
            style={[styles.barBackground, { width: `${capacityPercentage}%` }]}
          >
            <Text style={styles.barText}>
              {capacity}/{totalCapacity} ({capacityPercentage}%)
            </Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  locationBox: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#f9f9f9",
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    elevation: 3,
  },
  locationImage: {
    width: 80,
    height: 80,
    borderRadius: 10,
  },
  locationDetails: {
    flex: 1,
    marginLeft: 10,
    justifyContent: "center",
  },
  nameText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#232D4B",
  },
  capacityGraph: {
    marginTop: 5,
  },
  barBackground: {
    backgroundColor: "#232D4B",
    borderRadius: 5,
    padding: 5,
    justifyContent: "center",
    alignItems: "center",
  },
  barText: {
    color: "#fff",
  },
});

export default LocationBox;
