#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import base64
import requests
import os

dir = '/home/pedestrian/Desktop/VoiceToText/text/'


def extract_text():
    for _, _, filenames in os.walk(dir + 'original/'):
        original = open(dir + 'original.txt', 'w')
        for filename in filenames:
            original_file = open(dir + 'original/' + filename, 'r')
            original.writelines(original_file.read() + '\n')
            original_file.close()
        original.close()

if __name__ == "__main__":
    extract_text()
    print("extract_text is over!")
