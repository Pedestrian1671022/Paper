#!/usr/bin/env python
# -*- coding: utf-8  -*-
# fastICA

import wave
import math
import scipy
import struct
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros

wavefile1 = wave.open('wav/original/0.wav', 'rb')
wavefile2 = wave.open('wav/original/10.wav', 'rb')
wavefile3 = wave.open('wav/original/20.wav', 'rb')

nchannels1 = wavefile1.getnchannels()
sample_width1 = wavefile1.getsampwidth()
framerate1 = wavefile1.getframerate()
numframes1 = wavefile1.getnframes()
numframes2 = wavefile2.getnframes()
numframes3 = wavefile3.getnframes()

sound1 = zeros(numframes1)
sound2 = zeros(numframes2)
sound3 = zeros(numframes3)

for i in range(numframes1):
    sound1[i] = struct.unpack('h', wavefile1.readframes(1))[0]
for i in range(numframes2):
    sound2[i] = struct.unpack('h', wavefile2.readframes(1))[0]
for i in range(numframes3):
    sound3[i] = struct.unpack('h', wavefile3.readframes(1))[0]

sound1 = sound1[20000:70000]
sound2 = sound2[10000:60000]
sound3 = sound3[:50000]

originalmatrix = []
originalmatrix.append(sound1)
originalmatrix.append(sound2)
originalmatrix.append(sound3)
originalmatrix = np.mat(originalmatrix)
originalmatrixlist = originalmatrix.tolist()

plt.subplot(331)
plt.plot(originalmatrixlist[0])
plt.subplot(332)
plt.plot(originalmatrixlist[1])
plt.subplot(333)
plt.plot(originalmatrixlist[2])

mix = np.mat(np.random.rand(3, 3))
mixmatrix = originalmatrix.T * mix
mixmatrix = mixmatrix.T
mixmatrixlist = mixmatrix.tolist()

plt.subplot(334)
plt.plot(mixmatrixlist[0])
plt.subplot(335)
plt.plot(mixmatrixlist[1])
plt.subplot(336)
plt.plot(mixmatrixlist[2])

meanmatrix = np.mean(mixmatrix, axis=1)
mixmatrix = mixmatrix - np.tile(meanmatrix, 50000)
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

fastICAMatrix = B.T*Q*mixmatrix
fastICAMatrixlist = fastICAMatrix.tolist()
plt.subplot(337)
plt.plot(fastICAMatrixlist[0])
plt.subplot(338)
plt.plot(fastICAMatrixlist[1])
plt.subplot(339)
plt.plot(fastICAMatrixlist[2])
plt.show()