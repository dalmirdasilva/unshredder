#!/usr/bin/python

from __future__ import division
from PIL import Image

NUMBER_OF_SHREDS = 20

image = Image.open("image.png")

image_data = image.getdata()
image_width, image_height = image.size
shred_width = int(image_width / NUMBER_OF_SHREDS)
unshredded_image = Image.new("RGBA", image.size)

def add(x, y): return x + y
def avg(seq):
    length = len(seq)
    if length == 0:
        return 0
    else:
        return reduce(add, seq, 0) / length

def get_pixel_value(x, y):
    return image_data[y * image_width + x]
    
def set_pixel_value(x, y, pixel):
    image_data[y * image_width + x] = pixel

def get_difference(pixel0, pixel1):
    return (abs(pixel0[0] - pixel1[0]) + abs(pixel0[1] - pixel1[1]) + abs(pixel0[2] - pixel1[2]) + abs(pixel0[3] - pixel1[3]))

def compare_shreds(a, b):
    differences = []
    for h in range(0, image_height - 1):
        x1 = (a * shred_width) + shred_width - 1
        x2 = b * shred_width
        differences.append(get_difference(get_pixel_value(x1, h), get_pixel_value(x2, h)))
    return avg(differences)

def write_shreds(ordered_shreds):
    start = 0
    for i in ordered_shreds:
        x1 = i * shred_width
        x2 = x1 + shred_width - 1
        source_region = image.crop((x1, 0, x2, image_height - 1))
        destination_point = (start, 0)
        unshredded_image.paste(source_region, destination_point)
        start = start + shred_width
    
def find_first():
    return 8
    
ordered_shreds = [find_first()]
last_ordered_shred = ordered_shreds[0]

while len(ordered_shreds) < NUMBER_OF_SHREDS:
    averages = []
    for i in range(0, NUMBER_OF_SHREDS):
        averages.append({'shred': i, 'avg': compare_shreds(last_ordered_shred, i)})
    best_shred = -1
    best_average = float("inf")
    for average in averages:
        if average['avg'] < best_average:
            best_shred = average['shred']
            best_average = average['avg']
    last_ordered_shred = best_shred
    ordered_shreds.append(best_shred)

write_shreds(ordered_shreds)
unshredded_image.save("unshredded.png", "PNG")
