#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import base64
import requests
import os

def extract_text():
    original = open('original.txt', 'r')
    original_text = original.readlines()
    original.close()
    filenames = ['mix.txt', 'ica.txt']
    for filename in filenames:
        file = open(filename, 'r')
        texts = file.readlines()
        file.close()
        num = 0
        for text in texts:
            if text in original_text:
                num +=1
        print(filename,num)

if __name__ == "__main__":
    extract_text()
    print("extract_text is over!")
