///Node.js Code (Receiving Data and Sending to Azure Blob Storage)
// server.js
const express = require("express");
const { BlobServiceClient } = require("@azure/storage-blob");
const app = express();

app.use(express.json());

const AZURE_CONNECTION_STRING = "<Your_Azure_Connection_String>";
const blobServiceClient = BlobServiceClient.fromConnectionString(
  AZURE_CONNECTION_STRING
);
const containerClient = blobServiceClient.getContainerClient(
  "<Your_Container_Name>"
);

app.post("/api/data", async (req, res) => {
  try {
    const { enter_count, exit_count, timestamp } = req.body;
    const blobName = `in_out_results_${timestamp}.json`;
    const blockBlobClient = containerClient.getBlockBlobClient(blobName);
    const data = JSON.stringify({ enter_count, exit_count, timestamp });

    await blockBlobClient.upload(data, data.length);
    res.status(200).send("Data uploaded to Azure Blob Storage");
  } catch (error) {
    console.error("Error uploading data to Azure", error);
    res.status(500).send("Failed to upload data");
  }
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
