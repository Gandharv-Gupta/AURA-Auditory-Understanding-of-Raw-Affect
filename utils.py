import os
import csv
from datetime import datetime
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hume API Key
api_key = os.getenv("HUME_API_KEY")

# Ensure Screams directory exists
os.makedirs("Screams", exist_ok=True)

# Ensure logs.csv exists
if not os.path.exists("logs.csv"):
    with open("logs.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Name", "User Emotion",
            "Model Emotion 1", "Score 1",
            "Model Emotion 2", "Score 2",
            "Model Emotion 3", "Score 3",
            "Filename"
        ])

def generate_filename(name: str) -> str:
    """Generate a unique filename based on name and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.strip().replace(" ", "_").lower()
    return f"{safe_name}_{timestamp}.wav"

async def get_audio_emotions(file_name: str):
    """Send audio to Hume API and get top 3 predicted emotions."""
    client = AsyncHumeClient(api_key=api_key)
    audio_path = os.path.join("Screams", file_name)
    model_config = Config(burst={})
    stream_options = StreamConnectOptions(config=model_config)

    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file(audio_path)

        if (
            result is None or 
            result.burst is None or 
            not result.burst.predictions
        ):
            print(f"Warning: Hume API returned no predictions for {file_name}")
            return None  # <-- Return None if no predictions

        emotions = result.burst.predictions[0].emotions
        top_3 = sorted(emotions, key=lambda e: e.score, reverse=True)[:3]
        return {e.name: round(e.score * 100, 2) for e in top_3}

def save_audio_file(file_path: str, audio_data: bytes):
    """Save audio bytes to disk."""
    with open(file_path, "wb") as f:
        f.write(audio_data)

def log_to_csv(name: str, user_emotion: str, top3_emotions: dict, filename: str):
    """Log results to CSV."""
    emotion_items = list(top3_emotions.items())

    while len(emotion_items) < 3:
        emotion_items.append(('(no data)', 0.0))

    row = [
        name,
        user_emotion,
        emotion_items[0][0], emotion_items[0][1],
        emotion_items[1][0], emotion_items[1][1],
        emotion_items[2][0], emotion_items[2][1],
        filename
    ]

    with open("logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)
