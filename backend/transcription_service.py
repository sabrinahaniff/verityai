import asyncio
import websockets
import json
import whisper
import os

# WebSocket Server Settings
HOST = "localhost"
PORT = 8765

# Load Whisper model
model = whisper.load_model("base")

async def handler(websocket):
    print("Client connected")
    try:
        while True:
            # Receive audio data as bytes
            audio_data = await websocket.recv()
            temp_file = "temp.wav"

            # Write audio data to temporary file
            with open(temp_file, "wb") as f:
                f.write(audio_data)

            # Transcribe audio
            result = model.transcribe(temp_file)
            transcription = result.get("text", "")
            os.remove(temp_file)  # Clean up temp file

            # Send transcription to frontend
            response = json.dumps({"transcription": transcription})
            await websocket.send(response)

    except websockets.ConnectionClosedError:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    print(f"Starting server at ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
