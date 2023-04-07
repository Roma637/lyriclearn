import pyttsx3
import librosa
import soundfile as sf
import numpy as np
import scipy.signal as sig
import psola
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
import os

def generate_music(text, melodyChoice):

    now = datetime.now().strftime("%m %d %H %M %S")

    #count num of verses/ lines
    lineNum = len([i for i in text.split('\n') if i!= ''])
    # print(lineNum)
    

    #format text for text to speech
    # verseNum = len(text.split("\n\n"))
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace("\n", ",")
    # text = text.replace('.', '')
    # text = text.replace(',', '')
    print(repr(text))

    #text to speech
    def converter(text):
        engine = pyttsx3.init()

        rate = engine.getProperty('rate')
        # print('rate:', rate)
        engine.setProperty('rate', 170)

        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id) #voice 2 is jap

        # save voice file
        temp_filename = secure_filename(f"voice_{now}.mp3")
        temp_filename = os.path.join('audio_files', temp_filename)
        # print(temp_filename)

        engine.save_to_file(text, 'testvoice.mp3')
        engine.runAndWait()
        
        os.rename("testvoice.mp3", Path(temp_filename))
        return temp_filename

    t_filename = converter(text)

    y, sr = librosa.load(Path(t_filename))

    melodyDict =  {"london": [["G4","G4","G4","A4","G4","G4","F4","F4",
                        "E4","E4","F4","F4","G4","G4","G4","G4"], #
                        ["D4","D4","E4","E4","F4","F4","F4","F4",
                        "E4","E4","F4","F4","G4","G4","G4","G4"],#
                        ["G4","G4","G4","A4","G4","G4","F4","F4",
                        "E4","E4","F4","F4","G4","G4","G4","G4"],#
                        ["D4","D4","D4","D4","G4","G4","G4","G4",
                        "E4","E4","C4","C4","C4","C4","C4","C4"]], #lond
                "twinkle": [["D4","A4","B4","A4"],#twinkle teinkle lil star 
                            ["G4","F#4","E4","D4"],  #how i wondeer what you are
                        ["A4","G4","F#4","E4"], #up above the world so high
                        ["A4","G4","F#4","E4"],
                        ["D4","A4","B4","A4"],
                        ["G4","F#4","E4","D4"]], #twin
                "frere": [["C4","C4","D4","D4","E4","E4","C4","C4", #are you sleeping
                        "C4","C4","D4","D4","E4","E4","C4","C4"], #are you sleeping
                        ["E4","E4","F4","F4","G4","G4","G4","G4", #brother john
                        "E4","E4","F4","F4","G4","G4","G4","G4"], #brother h=john
                        ["G4","A4","G4","F4","E4","E4","C4","C4",
                        "G4","A4","G4","F4","E4","E4","C4","C4"],#
                        ["C4","C4","G3","G3","C4","C4","C4","C4",
                        "C4","C4","G3","G3","C4","C4","C4","C4"]], #frer
                "weasel": [["C4","C4","C4","D4","D4","D4", #round and round the
                        "E4","G4","E4","C4","C4","A3"], #
                        ["C4","C4","C4","D4","D4","D4",
                        "E4","E4","E4","C4","C4","A3"],#
                        ["C4","C4","C4","D4","D4","D4",
                        "E4","G4","E4","C4","C4","C4"],#
                        ["A4","A4","A4","D4","D4","F4",
                        "E4","E4","E4","C4","C4","C4"]]} #popg

    

    # melody = melodyDict[melodyChoice]*verseNum
    # print(melody)
    allLines = melodyDict[melodyChoice]
    melody = []
    for i in range(lineNum):
        print(allLines[i%len(allLines)])
        melody.extend(allLines[i%len(allLines)])
    # print(melody)

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

    #save song file
    temp_filename = secure_filename(f"song_{now}.mp3")
    temp_filename = os.path.join('audio_files', temp_filename)
    filepath = Path(temp_filename)
    # print(filepath)
    sf.write(filepath, newY, sr)

    return filepath
