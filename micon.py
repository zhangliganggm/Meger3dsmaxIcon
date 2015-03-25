__author__ = 'ACE_Zhang'
# create: Acee-studio Ace_zhang
# Email: Acee-studio@qq.com
# Author: Ace_zhang
# last updata: 26-3-2015
# Copyright (C) 2015 Acee-studio
# ----------------------------------------------------

# Don't filter bmp.

import os
from PIL import Image
from argparse import ArgumentParser  
  
p = ArgumentParser(usage='Meger 3dsmax Icon 0.1 by AceeStudio', description='This is a Script for Quick Merge Icon file.')  
p.add_argument('-path', default=False, help='Auto Serch Icon of Path')  
p.add_argument('-large', default=24, type=int, help='Large Size of Icon')  
p.add_argument('-small', default=16, type=int, help='Small Size of Icon')  
p.add_argument('-newname', default=False, help='output fine image with newname')  

filter = ('.jpg', '.png', '.tif')
filter_l = lambda name: (name.endswith(a) for a in filter)
BG_COLOR_ALPHA = (0,0,0)
BG_COLOR_RGB = (255,255,255)

def merge(path, image_block, size=24, isaplha=None, newname=None):
    if path[-1] != '/':
        path += '/'
    bg_color = BG_COLOR_ALPHA if isaplha else BG_COLOR_RGB
    isaplha = 'a' if isaplha  else 'i'
    
    #start merge image list
    for image_key in image_block.keys():
        image_list = image_block[image_key]

        background = Image.new("RGB", (size*len(image_list), size), bg_color)

        for i, filename in enumerate(image_list):
            png = Image.open(path+filename)
            png.load()
            png = png.resize((size, size), Image.ANTIALIAS)
            if isaplha == 'a':
                alpha = Image.new("RGB", png.size, (255, 255, 255))
                background.paste(alpha,(i*size, 0), mask=png.split()[3]) 
            else:
                background.paste(png,(i*size, 0), mask=png.split()[3]) 

        # setting new outputname
        image_key = newname if newname else image_key
        if image_key[-1] != '_':
            image_key += '_'
        background.save(path+image_key+'{size}{mode}.bmp'.format(size=size, mode=isaplha))

def find_range(filename):
    filename, type = os.path.splitext(filename)
    int_string = ''
    len_type = len(type)
    for a in xrange(len(filename)-1, -1, -1):
        int_string += filename[a]
        try:
            int(int_string)
        except:
            return len(filename)-len(int_string[:-1]), -len_type
    return len(filename)-len(int_string), -len_type

def get_file(path):
    image_key = {}
    def get_key(path, split):
        key, index = path[:split[0]], path[split[0]:split[1]], 
        if key not in image_key:
            image_key.setdefault(key, [])
            image_key[key].append(path)
        else:
            image_key[key].append(path)
        

    for a in os.listdir(path):
        if any(filter_l(a)):
            get_key(a, find_range(a))
    
    return image_key


if __name__ == '__main__':
    args = p.parse_args()
     
    print p.format_help()
    if args.path:
        image_key = get_file(args.path)
        merge(args.path, image_key, args.large, newname=args.newname)
        merge(args.path, image_key, args.large, True, newname=args.newname)
        merge(args.path, image_key, args.small, newname=args.newname)
        merge(args.path, image_key, args.small, True, newname=args.newname)
