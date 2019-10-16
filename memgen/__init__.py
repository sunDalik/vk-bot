# -*- coding: utf-8 -*-
# based on https://github.com/danieldiekmeier/memegenerator
# added multiline strings feature
# usage: make_meme(["We live", "in", "a society"], ["Bottom text"], "joker.jpg")
# will generate `temp.png`

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import sys

font_file = 'memgen/font.ttf'

def make_meme(in_file, out_file, msg_list):
    top_msg = random.choice(msg_list)
    while len(top_msg) > 50:
        top_msg = random.choice(msg_list)

    bottom_msg = random.choice(msg_list)
    while len(bottom_msg) > 50:
        bottom_msg = random.choice(msg_list)

    make_meme_with_top_bottom([top_msg], [bottom_msg], in_file, out_file)

def make_meme_with_top_bottom(topStrings, bottomStrings, filename, out_filename):
    img = Image.open(filename)
    imageSize = img.size

    draw = ImageDraw.Draw(img)

    fontsizes = []
    for topString in topStrings:
        fontsizes.append(get_fontsize(imageSize, topString))
    for bottomString in bottomStrings:
        fontsizes.append(get_fontsize(imageSize, bottomString))
    fontSize = min(fontsizes)
    font = ImageFont.truetype(font_file, fontSize)

    line_num = 0
    for topString in topStrings:
            textSize = font.getsize(topString)
            topTextPosition = get_text_position_top(imageSize, line_num, textSize)
            # draw outlines
            # there may be a better way
            outlineRange = int(fontSize/15)
            for x in range(-outlineRange, outlineRange+1):
                    for y in range(-outlineRange, outlineRange+1):
                            draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)

            draw.text(topTextPosition, topString, (255,255,255), font=font)
            line_num += 1
    line_num = 1
    for bottomString in bottomStrings:
            textSize = font.getsize(bottomString)
            bottomTextPosition = get_text_position_bottom(imageSize, line_num, textSize)
            # draw outlines
            # there may be a better way
            outlineRange = int(fontSize/15)
            for x in range(-outlineRange, outlineRange+1):
                    for y in range(-outlineRange, outlineRange+1):
                            draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

            draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)
            line_num += 1
    img.save(out_filename)

def get_fontsize(imageSize, text):
	# find biggest font size that works
	fontSize = int(imageSize[1]/10)
	font = ImageFont.truetype(font_file, fontSize)
	textSize = font.getsize(text)
	while textSize[0] > imageSize[0]-20:
		fontSize = fontSize - 1
		font = ImageFont.truetype(font_file, fontSize)
		textSize = font.getsize(text)
	return fontSize

def get_text_position_top(image_size, line_num, text_size):
	# find top centered position for top text
	textPositionX = (image_size[0]/2) - (text_size[0]/2)
	textPositionY = (text_size[1] + 2) * line_num
	return (textPositionX, textPositionY)
def get_text_position_bottom(image_size, line_num, text_size):
	# find bottom centered position for bottom text
	textPositionX = (image_size[0]/2) - (text_size[0]/2)
	textPositionY = image_size[1] - (text_size[1] + 2) * line_num
	return (textPositionX, textPositionY)
