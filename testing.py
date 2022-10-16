from pydub import AudioSegment
#import argparse
#import array
#import math
#import wave
import matplotlib.pyplot as plt
#import numpy
#import pywt
from scipy import signal
from os import path
import librosa
import statistics
from mutagen.mp3 import MP3
# import firebase
from modelPredict import predict 
# from firebase_admin import db
import firebase_admin
import json

#cred = firebase_admin.credentials.Certificate("path/to/serviceAccountKey.json")
#firebase_admin.initialize_app(cred)
# ref = db.reference("/")
# import firebase
# import time
# import firebase_admin
# from firebase_admin import credentials

def findSongMeasures(filename, song_name):
    filename = 'E_Flat_Major.mp3'
    totalFileSeconds = MP3(filename).info.length
    song = AudioSegment.from_mp3(filename)
    # ten_seconds = 10 * 1000
    # first_10_seconds = song[:10000]
    song.export("test.wav", format="wav")
    y, sr = librosa.load('test.wav')
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    #####################
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    #####################
    #print("\t" + str(tempo))
    print(len(tempo))
    # print(statistics.mode(tempo))
    approximate_bpm = round(statistics.mean(tempo))
    approximate_bpm = 78
    print("Approximate_BPM: " + str(approximate_bpm))
    print("Total File Seconds: " + str(totalFileSeconds))
    print("Total Song Length: " + str(len(song) / 1000))
    num_quarter_notes = ((len(song)/1000.0)*approximate_bpm/60)
    print("Num quarter notes " + str(num_quarter_notes))
    #print(len(song))
    allMeasures = "|"
    curMeasureNotes = []
    sumCurMeasure = []
    for i in range(1, round(num_quarter_notes+1)):
        curSongComp = song[len(song)*(i-1)/num_quarter_notes:len(song)*(i)/num_quarter_notes]
        curSongComp.export("curNote.wav", format="wav")
        curNotePrediction = predict("curNote.wav")
        print(curNotePrediction)
        if len(curMeasureNotes) > 0 and curNotePrediction == curMeasureNotes[-1]:
            sumCurMeasure[-1] += 1
        else:
            curMeasureNotes.append(curNotePrediction)
            sumCurMeasure.append(1)
        if sum(sumCurMeasure) == 4:
            for idx, x in enumerate(curMeasureNotes):
                print(sumCurMeasure[idx])
                allMeasures += curMeasureNotes[idx]
                if sumCurMeasure[idx] == 1:
                    allMeasures += str(2)
                elif sumCurMeasure[idx] == 2:
                    allMeasures += str(4)
                elif sumCurMeasure[idx] == 3:
                    allMeasures += str(6)
                else:
                    allMeasures += str(8)
            allMeasures += "|"
            curMeasureNotes = []
            sumCurMeasure = []
        
        
    # cred = credentials.Certificate("path/to/serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    # curSongComp.export("test" + str(i) + ".wav", format="wav")
    # fdb = firebase.FirebaseApplication(db_url, None)
    #fdb.post('/' + song_name, allMeasures)
    #with open("")
    return allMeasures
print(findSongMeasures('E_Flat_Major.mp3', "E Flat Major Scale"))