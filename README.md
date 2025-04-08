# EchoType

This is a quick & dirty (mostly AI generated) little learning game that could be summarized with
"Type what you hear". Choose a topic, and AI will generate 10 words/phases/sentences that will be
fed into an AI voice generator. After playback of each audio the solution needs to be typed in.

Info/Features/Restrictions:

* OpenAI API key is required.
* Currently `aplay` needs to exist on your system (which does on most Linux based distros).
* Generated AI audio is cached and reused for the same input string.

## Setup

Checkout the sources and change into the project directory.

Create venv and install the Python dependencies:
```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file containing your OpenAI key:
```shell
echo OPENAI_API_KEY=**YOUR-SECRET-API-KEY** >>.env
```

## Run

```shell
. .venv/bin/activate
./EchoType.py
```

## Example game

```
🧠 Wähle ein Thema:
1. Haustiere
2. Frühstück
3. Reisen
4. Berufe
5. Farben
6. Gefühle
7. Familie
8. Sportarten
9. Zufälliges Thema
Nummer eingeben: 6

📚 Thema gewählt: Gefühle
⏳ Fordere Aufgaben von der KI an...

🎯 Wiederhole, was du hörst. Drücke [Tab], um es erneut zu hören.

🔊 Aufgabe 1 von 10:
Deine Eingabe: die Freude
✅ Richtig!

🔊 Aufgabe 2 von 10:
IcDeine Eingabe: Ich bin glücklich.
✅ Richtig!

🔊 Aufgabe 3 von 10:
Deine Eingabe: der Ärga
❌ Falsch. Korrekt wäre gewesen: 'der Ärger'

🔊 Aufgabe 4 von 10:
Du Deine Eingabe: Du bist traurig.
✅ Richtig!

🔊 Aufgabe 5 von 10:
Deine Eingabe: die Angst
✅ Richtig!

🔊 Aufgabe 6 von 10:
Deine Eingabe: Sie ist wütend.
✅ Richtig!

🔊 Aufgabe 7 von 10:
Deine Eingabe: das Lächeln
✅ Richtig!

🔊 Aufgabe 8 von 10:
Deine Eingabe: Wir fühlen uns sicher.
✅ Richtig!

🔊 Aufgabe 9 von 10:
Deine Eingabe: ein lachen
✅ Richtig!

💡 Exakte Schreibweise: ein Lachen

🔊 Aufgabe 10 von 10:
Deine Eingabe: Er hat Angst.
✅ Richtig!

🏁 Spiel beendet. Deine Punktzahl: 9 von 10
```
