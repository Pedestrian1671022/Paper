#!/usr/bin/env python
# -*- coding: utf-8  -*-
# fastICA

import wave
import scipy
import struct
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros

wavefile1 = wave.open('left.wav', 'rb')
wavefile2 = wave.open('right.wav', 'rb')

nchannels1 = wavefile1.getnchannels()
sample_width1 = wavefile1.getsampwidth()
framerate1 = wavefile1.getframerate()
numframes1 = wavefile1.getnframes()
numframes2 = wavefile2.getnframes()

print(numframes2)

sound1 = zeros(numframes1)
sound2 = zeros(numframes2)

for i in range(numframes1):
    sound1[i] = struct.unpack('h', wavefile1.readframes(1))[0]
for i in range(numframes2):
    sound2[i] = struct.unpack('h', wavefile2.readframes(1))[0]

mixmatrix = []
mixmatrix.append(sound1)
mixmatrix.append(sound2)
mixmatrix = np.mat(mixmatrix)
mixmatrixlist = mixmatrix.tolist()

print(len(mixmatrixlist[0]))

plt.subplot(221)
plt.plot(mixmatrixlist[0])
plt.subplot(222)
plt.plot(mixmatrixlist[1])

meanmatrix = np.mean(mixmatrix, axis=1)
mixmatrix = mixmatrix - np.tile(meanmatrix, numframes1)
covmatrix = np.cov(mixmatrix)
eval, evec = np.linalg.eig(covmatrix)
Q = np.mat(np.sqrt(np.diag(eval))).I * evec.T
whitematrix = Q * mixmatrix
# print(np.cov(whitematrix))

numfICA, nsamples = whitematrix.shape
B = np.mat(np.zeros((numfICA, numfICA)))
for i in range(numfICA):
    maxIterations = 100
    Iteration = 0
    b = np.random.rand(numfICA, 1)-0.5
    b = b/np.linalg.norm(b)
    while Iteration < maxIterations:
        bOld = b
        t = whitematrix.T * b
        g = np.multiply(t, scipy.exp(np.multiply(t, t) / -2))
        dg = np.multiply((1-np.multiply(t, t)), scipy.exp(np.multiply(t, t) / -2))
        b= (whitematrix*g)/nsamples - np.mean(dg)*b

        b= b-B*B.T*b
        b = b/np.linalg.norm(b)
        if abs(abs(b.T*bOld)-1)<1e-9:
            break
        Iteration = Iteration+1
    B[:, i] = b

icaleft = wave.open('icaleft.wav', 'wb')
icaright = wave.open('icaright.wav', 'wb')

icaleft.setnchannels(nchannels1)
icaright.setnchannels(nchannels1)
icaleft.setsampwidth(sample_width1)
icaright.setsampwidth(sample_width1)
icaleft.setframerate(framerate1)
icaright.setframerate(framerate1)

fastICAMatrix = B.T*Q*mixmatrix
fastICAMatrixlist = fastICAMatrix.tolist()

plt.subplot(223)
plt.plot(fastICAMatrixlist[0])
plt.subplot(224)
plt.plot(fastICAMatrixlist[1])

for i in fastICAMatrixlist[0]:
    icaleft.writeframes(struct.pack('h', np.short(i*1000)))

for i in fastICAMatrixlist[1]:
    icaright.writeframes(struct.pack('h', np.short(i*1000)))

plt.show()