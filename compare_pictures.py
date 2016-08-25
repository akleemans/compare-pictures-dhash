#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Image comparison script with the help of PIL.'''
__author__  = "Adrianus Kleemans"
__date__    = "30.11.2014"

import os
import math, operator
from PIL import Image
import pylab

def diff(h1, h2):
    return sum([bin(int(a, 16) ^ int(b, 16)).count('1') for a, b in zip(h1, h2)])

def dhash(image, hash_size = 8):
    # scaling and grayscaling
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = list(image.getdata())

    # calculate differences
    diff_map = []
    for row in range(hash_size):
        for col in range(hash_size):
            diff_map.append(image.getpixel((col, row)) > image.getpixel((col + 1, row)))
    # build hex string
    return hex(sum(2**i*b for i, b in enumerate(reversed(diff_map))))[2:-1]

def main():
    # detect all pictures
    pictures = []
    os.chdir(".")
    for f in os.listdir("."):
        if f.endswith('.jpg'):
            pictures.append(f)

    # compare with first picture
    image1 = Image.open(pictures[0])
    h1 = dhash(image1)
    print 'Checking picture', pictures[0], '(hash:', h1, ')'

    data = []
    xlabels = []
    for j in range(1, len(pictures)):
        image2 = Image.open(pictures[j])
        h2 = dhash(image2)
        print 'Hash of', pictures[j], 'is', h2
        xlabels.append(pictures[j])
        data.append(diff(h1, h2))

    # plot results
    fig, ax = pylab.plt.subplots(facecolor='white')
    pos = pylab.arange(len(data))+.5

    ax.set_xlabel('difference in bits')
    ax.set_title('Bitwise difference of picture hashes')
    barlist = pylab.plt.barh(pos, data, align='center', color='#E44424')
    pylab.yticks(pos, xlabels)
    pylab.grid(True)
    pylab.plt.show()

if __name__ == '__main__':
    main()
