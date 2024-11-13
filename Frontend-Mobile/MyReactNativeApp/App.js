import { StatusBar } from "expo-status-bar";
import { StyleSheet, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import CapacityData from "./Components/CapacityData"; // Assuming you create this component
import BuildingDetail from "./Components/BuildingDetail"; // Assuming you create this component

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator initialRouteName="CapacityData">
        <Stack.Screen
          name="CapacityData"
          component={CapacityData}
          options={{ title: "Building Capacity Tracker" }}
        />
        <Stack.Screen
          name="BuildingDetail"
          component={BuildingDetail}
          options={({ route }) => ({ title: route.params.name })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
