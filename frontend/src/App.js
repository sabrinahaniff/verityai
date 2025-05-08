import React, { useState } from "react";

const TEXT_ANALYZE_ENDPOINT = "http://127.0.0.1:5001/analyze_sentiment";
const AUDIO_ANALYZE_ENDPOINT = "http://127.0.0.1:5002/analyze";

const App = () => {
  const [text, setText] = useState("");
  const [transcript, setTranscript] = useState("");
  const [sentimentResult, setSentimentResult] = useState("");
  const [error, setError] = useState("");
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const analyzeText = async () => {
    try {
      const response = await fetch(TEXT_ANALYZE_ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setSentimentResult(`Sentiment: ${data.sentiment} | Score: ${data.score.toFixed(2)}`);
      setError("");
    } catch (err) {
      setError(`Error: ${err.message}`);
      setSentimentResult("");
    }
  };

  const analyzeFile = async () => {
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch(AUDIO_ANALYZE_ENDPOINT, {
        method: "POST",
        body: formData,
      });
  
      console.log("Response Status:", response.status);
  
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
  
      const data = await response.json();
      console.log("Response Data:", data);
  
      setTranscript(`Transcript: ${data.transcription}`);
      setSentimentResult(`Sentiment: ${data.sentiment} | Score: ${data.score.toFixed(2)}`);
      setError("");
    } catch (err) {
      console.error("Error:", err.message);
      setError(`Error: ${err.message}`);
      setTranscript("");
      setSentimentResult("");
    }
  };
  
  return (
    <div style={{ padding: "20px" }}>
      <h1>Sentiment Analysis</h1>

      <textarea
        placeholder="Enter text to analyze..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ width: "100%", height: "100px", marginBottom: "10px" }}
      />
      <button onClick={analyzeText}>Analyze Text</button>

      <br />

      <input type="file" onChange={handleFileChange} style={{ marginBottom: "10px" }} />
      <button onClick={analyzeFile}>Analyze Audio</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Transcript:</h2>
      <p>{transcript}</p>

      <h2>Sentiment:</h2>
      <p>{sentimentResult}</p>
    </div>
  );
};

export default App;
