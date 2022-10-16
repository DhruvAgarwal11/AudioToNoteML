import coremltools as ct
from scipy.io import wavfile
import os
from wave import open
# import audiofile
from pydub import AudioSegment
from pydub.playback import play
from scipy.io.wavfile import read
import numpy as np
from numpy.core import multiarray
import statistics
# import firebase






def predict(myNote):
    # mlmodel = ct.models.MLModel('/Users/dhruv/Downloads/NewClassifier.mlmodel')
    mlmodel = ct.models.MLModel('NewClassifier.mlmodel')
    # myNote = '/Users/dhruv/Desktop/Hackathon_Project/2'
    # myNote = read("/Users/dhruv/Desktop/Hackathon_Project/2/test2.wav")
    myNote = read(myNote)

    numpyArr = np.array(myNote[1], dtype = float)
    allNumpyArrs = []
    for i in range(1, 2):
    # for i in range(1, (len(numpyArr) // 7800 + 1)):
        tempArr = numpyArr[((i - 1) * 7800):(i * 7800)]
        allNumpyArrs.append(tempArr)
        #print("\tShape: " + str(tempArr.shape))
        #print(tempArr.shape)
    #print(type(mlmodel.get_spec().description.input[0].type.multiArrayType))
    labels = []
    for i in range(0, len(allNumpyArrs)):
        probability = mlmodel.predict(data = {"audioSamples": allNumpyArrs[i]})
        print(probability)
        print()
        classLabel = probability['classLabel']
        labels.append(classLabel)
    #print(statistics.mode(labels))
    finalLabel = statistics.mode(labels)
    #print(finalLabel)
    finalLabel = finalLabel.replace(':', '')
    #print(finalLabel)
    if 'b' in finalLabel:
        finalLabel = finalLabel.replace('b', '')
        finalLabel = '_' + finalLabel
    #print(finalLabel)
    if '#' in finalLabel:
        finalLabel = finalLabel.replace('#', '')
        finalLabel = '^' + finalLabel
    #print(finalLabel)
    if finalLabel[-1] == '3':
        finalLabel = finalLabel[:-1] + ','
    elif finalLabel[-1] == '4':
        finalLabel = finalLabel[:-1]
    else:
        finalLabel = finalLabel[:-1] + "\'"
    #print(finalLabel)
    # return finalLabel
    db_url = 'https://oskey-5a5e3-default-rtdb.firebaseio.com'
    """fdb = firebase.FirebaseApplication(db_url, None)
    for user in new_users:
        fdb.post('/user', user)
        time.sleep(3)"""
    return finalLabel

print(predict("test7.wav"))