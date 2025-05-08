import React, { useEffect, useState } from "react";

function App() {
  const [transcription, setTranscription] = useState("");
  const [status, setStatus] = useState("Connecting to WebSocket...");
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8765");
    setWs(websocket);

    websocket.onopen = () => {
      setStatus("Connected to WebSocket");
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setTranscription(data.transcription);
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
      setStatus("WebSocket Error");
    };

    websocket.onclose = () => {
      setStatus("WebSocket Connection Closed");
    };

    return () => {
      websocket.close();
    };
  }, []);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file && ws && ws.readyState === WebSocket.OPEN) {
      const arrayBuffer = await file.arrayBuffer();
      ws.send(arrayBuffer);
    }
  };

  return (
    <div className="App p-4">
      <h1 className="text-xl font-bold mb-4">Real-Time Transcription</h1>
      <p className="mb-2 text-gray-500">{status}</p>

      <div className="mb-4">
        <input type="file" accept="audio/*" onChange={handleFileUpload} />
      </div>

      <div className="bg-gray-100 p-4 rounded-xl shadow-md">
        <p>{transcription || "Waiting for transcription..."}</p>
      </div>
    </div>
  );
}

export default App;