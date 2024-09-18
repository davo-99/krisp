#!/usr/bin/python3

import os
import io
import tempfile
import subprocess
import pyaudio
import pyttsx3
import wave
import socket
import sqlite3
import speech_recognition as sr
from datetime import datetime
from textblob import TextBlob

# Function to get the active microphone and speaker names
def get_audio_devices():
    devices = os.popen("pactl list short sources").read().splitlines()
    microphone = devices[0].split('\t')[1] if devices else 'Unknown Microphone'
    
    devices = os.popen("pactl list short sinks").read().splitlines()
    speaker = devices[0].split('\t')[1] if devices else 'Unknown Speaker'
    
    return microphone, speaker

def record_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)

    return audio

def analyze_audio(audio):
    recognizer = sr.Recognizer()
    try:
        transcript = recognizer.recognize_google(audio)
        print("Transcript: ", transcript)
        sentiment = TextBlob(transcript).sentiment.polarity
        voice_sentiment = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    except sr.UnknownValueError:
        transcript = ""
        voice_sentiment = "Unknown"
    except sr.RequestError:
        transcript = ""
        voice_sentiment = "Error"
    
    return transcript, voice_sentiment

def save_to_database(conn, transcript, microphone_used, speaker_used, voice_sentiment):
    cursor = conn.cursor()
    session_metadata = None

    cursor.execute("""
    INSERT INTO user_metrics (user_id, session_metadata, talked_time, microphone_used, speaker_used, voice_sentiment)
    VALUES (?, ?, ?, ?, ?, ?)""",
    (1, session_metadata, 5, microphone_used, speaker_used, voice_sentiment))

    conn.commit()

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_metrics (
        user_id INTEGER NOT NULL CHECK(user_id >= 0),
        session_metadata BLOB,
        talked_time REAL CHECK(talked_time >= 0),
        microphone_used TEXT,
        speaker_used TEXT,
        voice_sentiment TEXT,
        timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

def main():
    microphone_used, speaker_used = get_audio_devices()
    audio = record_audio()
    transcript, voice_sentiment = analyze_audio(audio)

    conn = sqlite3.connect("/data/metrics.db")
    
    # Create the table if it doesn't exist
    create_table(conn)
    
    # Save the data to the database
    save_to_database(conn, transcript, microphone_used, speaker_used, voice_sentiment)
    
    conn.close()

if __name__ == "__main__":
    main()
