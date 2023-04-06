import pyttsx3
import librosa
import soundfile as sf
import numpy as np
import scipy.signal as sig
import psola
from pathlib import Path
from datetime import datetime
from werkzeug import secure_filename

def generate_music(text, melodyChoice):

    now = datetime.now().strftime("%m %d %H %M %S")

    #text to speech
    def converter(text):
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id) #voice 2 is jap
        engine.save_to_file(text, Path(secure_filename(f"audio_files/voice_{now}.mp3")))
        engine.runAndWait()

    converter(text)

    y, sr = librosa.load(Path("audio_files/voice.mp3"))

    melodyDict =  {"1": ["G4","G4","G4","A4","G4","G4","F4","F4",
                        "E4","E4","F4","F4","G4","G4","G4","G4",
                        "D4","D4","E4","E4","F4","F4","F4","F4",
                        "E4","E4","F4","F4","G4","G4","G4","G4",
                        "G4","G4","G4","A4","G4","G4","F4","F4",
                        "E4","E4","F4","F4","G4","G4","G4","G4",
                        "D4","D4","D4","D4","G4","G4","G4","G4",
                        "E4","E4","C4","C4","C4","C4","C4","C4"], #lond
                "2": ["D4","A4","B4","A4","G4","F#4","E4","D4",
                        "A4","G4","F#4","E4","A4","G4","F#4","E4",
                        "D4","A4","B4","A4","G4","F#4","E4","D4"], #twin
                "3": ["C4","C4","D4","D4","E4","E4","C4","C4",
                        "C4","C4","D4","D4","E4","E4","C4","C4",
                        "E4","E4","F4","F4","G4","G4","G4","G4",
                        "E4","E4","F4","F4","G4","G4","G4","G4",
                        "G4","A4","G4","F4","E4","E4","C4","C4",
                        "G4","A4","G4","F4","E4","E4","C4","C4",
                        "C4","C4","G3","G3","C4","C4","C4","C4",
                        "C4","C4","G3","G3","C4","C4","C4","C4"], #frer
                "4": ["A3","C4","C4","C4","D4","D4","D4", 
                        "E4","G4","E4","C4","C4","A3",
                        "C4","C4","C4","D4","D4","D4",
                        "E4","E4","E4","C4","C4","A3",
                        "C4","C4","C4","D4","D4","D4",
                        "E4","G4","E4","C4","C4","C4",
                        "A4","A4","A4","D4","D4","F4",
                        "E4","E4","E4","C4","C4","G4",
                        "C5","C5","C5","A4","A4","C5",
                        "B4","D5","B4","G4","G4","G4",
                        "C5","C5","C5","A4","A4","C5",
                        "B4","B4","B4","G4","G4","G4",
                        "F4","F4","E4","F4","F4","G4",
                        "A4","A4","B4","C5","C5","C5",
                        "A4","A4","A4","D4","D4","F4",
                        "E4","E4","E4","E4","C4","C4"]} #popg

    verseNum = len(text.split("\n\n"))
    text.replace("\n", " ")

    melody = melodyDict[melodyChoice]*verseNum

    def corrector(f0, melody):
        phaseLen = len(f0)//len(melody)
        currPhase = 0
        noteCounter = 0
        allTuned = np.zeros_like(f0) #the collector
        while noteCounter < len(melody)-1:
            note = melody[noteCounter]
            if noteCounter == len(melody)-2:
                allTuned[currPhase:] = librosa.note_to_hz(note)
            else:
                allTuned[currPhase:currPhase+phaseLen] = librosa.note_to_hz(note)
            currPhase += phaseLen
            noteCounter += 1
        smoothed_allTuned = sig.medfilt(allTuned, kernel_size=11)
        smoothed_allTuned[np.isnan(smoothed_allTuned)] = allTuned[np.isnan(smoothed_allTuned)] #I don't get this at all

        return smoothed_allTuned

    def tuner(y, sr, melody):
        #tracking pitch
        frame_length = 2048 #length of the analysis frame
        hop_length = frame_length//4
        fmin = librosa.note_to_hz("C2")
        fmax = librosa.note_to_hz("C7")
        f0, _, _ = librosa.pyin(y,
                                frame_length=frame_length,
                                hop_length=hop_length,
                                sr=sr,
                                fmin=fmin,
                                fmax=fmax)
        #correcting
        doneTuned = corrector(f0, melody)
        #phase shifting
        return psola.vocode(y, sample_rate=int(sr), target_pitch=doneTuned, fmin=fmin, fmax=fmax)

    newY = tuner(y, sr, melody)

    # filepath = Path("audio_files/voice.mp3")
    sf.write(Path(secure_filename(f"audio_files/song_{now}.mp3")), newY, sr)