#!/usr/bin/env python3

import hashlib
import subprocess
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
import openai
import re
import tempfile
import os

load_dotenv()

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
AI_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "ai-audio")
os.makedirs(AI_AUDIO_DIR, exist_ok=True)


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_filename_for_challenge(challenge_text):
    return hashlib.sha256(challenge_text.encode('utf-8')).hexdigest() + ".wav"

def get_ai_tts(text, voice="shimmer", model="gpt-4o-mini-tts", instructions="Spreche mit deutlicher lustiger Stimme. Sprache ist Deutsch."):
    return openai.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        instructions=instructions,
        speed=0.75,
        response_format="wav"
    )

# Prevent audio cutoff on first playback
def warmup_audio():
    # Play 0.5 seconds of silence
    subprocess.run([
        "aplay", "-q",
        "-t", "raw",        # input type = raw PCM
        "-r", "44100",      # sample rate
        "-f", "S16_LE",     # sample format (16-bit little endian)
        "-c", "1",          # channels
    ], input=b"\x00" * 44100)

# FIXME: better method, openai.helpers.LocalAudioPlayer?
def play_wav(file):
    subprocess.run(["aplay", "--quiet", file])  # or ["ffplay", "-nodisp", "-autoexit", file]

def speak(text):
    file = os.path.join(AI_AUDIO_DIR, get_filename_for_challenge(text))
    if not os.path.exists(file):
        response = get_ai_tts(text)
        with open(file, "wb") as f:
            f.write(response.read())
    play_wav(file)

# FIXME: use structured output
def get_challenges_from_ai(topic):
    prompt = f"""
Du bist ein Sprachtrainer für die 2. Klasse Grundschule.
Gib mir 10 kurze, einzelne Wörter oder vollständige Sätze in neuer deutscher Rechtschreibung zum Üben,
thematisch passend zum Thema "{topic}". Bei einzelnen Substantiven füge stets einen bestimmten/unbestimmten Artikel kleingeschrieben hinzu.
Beende vollständige Sätze stets mit einem Punkt.
Liefere nur die Begriffe oder Sätze, keine Erklärungen. Antworte als Liste im Format:
1. ...
2. ...
usw.
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    # Extract items from numbered list
    raw_text = response.choices[0].message.content.strip()
    lines = raw_text.splitlines()
    challenges = [re.sub(r"^\d+\.\s*", "", line).strip() for line in lines if line.strip()]
    return challenges[:10]

def normalize(text):
    # Remove punctuation and extra whitespace, convert to lowercase
    text = re.sub(r"[^\wäöüÄÖÜß]", " ", text.lower(), flags=re.UNICODE)
    return " ".join(text.split())

def run_game(challenges):
    session = PromptSession()
    bindings = KeyBindings()

    current_index = [0]  # mutable so inner function can access
    current_challenge = [challenges[current_index[0]]]

    @bindings.add("tab")
    def _(event):
        speak(current_challenge[0])

    print("🎯 Wiederhole, was du hörst. Drücke [Tab], um es erneut zu hören.\n")
    warmup_audio()

    score = 0
    for i, challenge_text in enumerate(challenges, start=1):
        current_challenge[0] = challenge_text
        print(f"🔊 Aufgabe {i} von {len(challenges)}:")
        speak(challenge_text)

        user_input = session.prompt("Deine Eingabe: ", key_bindings=bindings)
        if normalize(user_input) == normalize(challenge_text):
            print("✅ Richtig!\n")
            if user_input != challenge_text:
                print(f"💡 Exakte Schreibweise: {challenge_text}\n")
            play_wav(os.path.join(AUDIO_DIR, "correct.wav"))
            score += 1
        else:
            print(f"❌ Falsch. Korrekt wäre gewesen: '{challenge_text}'\n")
            play_wav(os.path.join(AUDIO_DIR, "correct.wav"))

    print(f"🏁 Spiel beendet. Deine Punktzahl: {score} von {len(challenges)}")
    if score >= len(challenges) * 0.7:
        play_wav(os.path.join(AUDIO_DIR, "win.wav"))

def main():
    themen = [
        "Haustiere",
        "Frühstück",
        "Reisen",
        "Berufe",
        "Farben",
        "Gefühle",
        "Familie",
        "Sportarten",
        "Zufälliges Thema",
    ]

    print("🧠 Wähle ein Thema:")
    for i, thema in enumerate(themen, 1):
        print(f"{i}. {thema}")
    auswahl = input("Nummer eingeben: ").strip()

    try:
        index = int(auswahl) - 1
        if 0 <= index < len(themen):
            thema = themen[index]
        else:
            raise ValueError()
    except ValueError:
        print("Ungültige Auswahl. Standard: 'Haustiere'")
        thema = "Haustiere"

    print(f"\n📚 Thema gewählt: {thema}")
    print("⏳ Fordere Aufgaben von der KI an...\n")
    challenges = get_challenges_from_ai(thema)
    run_game(challenges)

if __name__ == "__main__":
    main()
