// Import the MongoDB driver
const { MongoClient } = require("mongodb");

let client;

module.exports = async function (context, req) {
  // MongoDB connection URI with your credentials
  const uri =
    process.env.MONGO_URI ||
    "mongodb+srv://shivpatelca2:Basketball!!998@aicapacitytrackorstorag.lqkqcuc.mongodb.net/?retryWrites=true&w=majority&appName=AICapacityTrackorstorage";

  // Initialize the MongoDB client
  if (!client) {
    client = new MongoClient(uri, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
  }

  try {
    // Check if the client is already connected
    if (!client.isConnected()) {
      await client.connect();
    }

    // Specify the database and collection to use
    const database = client.db("test"); // Replace with your DB name if needed
    const collection = database.collection("Capacity_database"); // Replace with your collection name

    // Create a fake test document
    const fakeDocument = {
      name: "Test User",
      email: "testuser@example.com",
      age: 30,
    };

    // Insert the fake document into the collection
    const result = await collection.insertOne(fakeDocument);

    // Return success response
    context.res = {
      status: 200,
      body: {
        message: "Document inserted successfully",
        insertedId: result.insertedId,
      },
    };
  } catch (error) {
    // Handle errors and return error response
    context.res = {
      status: 500,
      body: {
        message: "Error connecting to MongoDB",
        error: error.message,
      },
    };
  } finally {
    // Optionally close the connection if you don't plan to reuse it
    // You can leave it connected for performance reasons
    // await client.close();
  }
};
