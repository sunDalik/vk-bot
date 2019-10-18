# -*- coding: utf-8 -*-
# based on https://github.com/danieldiekmeier/memegenerator
# added multiline strings feature
# usage: make_meme("joker.jpg", "temp.jpg", msg_list)
# will generate `temp.png`

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import sys

font_file = 'memgen/font.ttf'

def make_meme(in_file, out_file, msg_list, min_words):
    if min_words > 0:
        msg_list_saved = msg_list
        msg_list = [m for m in msg_list if len(m.split()) > min_words]
        if len(msg_list) == 0:
            msg_list = msg_list_saved

    top_msg = random.choice(msg_list)
    while len(top_msg) > 25 + min_words * 6:
        top_msg = random.choice(msg_list)

    bottom_msg = random.choice(msg_list)
    while len(bottom_msg) > 25 + min_words * 6:
        bottom_msg = random.choice(msg_list)

    # TODO: split long messages to lines
    make_meme_with_top_bottom([top_msg], [bottom_msg], in_file, out_file)


def make_meme_with_top_bottom(top_lines, bottom_lines, filename, out_filename):
    img = Image.open(filename)
    image_size = img.size

    draw = ImageDraw.Draw(img)

    fontsizes = []
    for line in top_lines:
        fontsizes.append(get_fontsize(image_size, line))
    for line in bottom_lines:
        fontsizes.append(get_fontsize(image_size, line))
    font_size = min(fontsizes)
    font = ImageFont.truetype(font_file, font_size)

    line_num = 0
    for line in top_lines:
            text_size = font.getsize(line)
            line_pos = get_text_position_top(image_size, line_num, text_size)
            # draw outlines
            # there may be a better way
            outline_range = int(font_size/15)
            for x in range(-outline_range, outline_range+1):
                    for y in range(-outline_range, outline_range+1):
                            draw.text((line_pos[0]+x, line_pos[1]+y), line, (0,0,0), font=font)

            draw.text(line_pos, line, (255,255,255), font=font)
            line_num += 1
    line_num = 1
    for line in bottom_lines:
            text_size = font.getsize(line)
            text_pos = get_text_position_bottom(image_size, line_num, text_size)
            # draw outlines
            # there may be a better way
            outline_range = int(font_size/15)
            for x in range(-outline_range, outline_range+1):
                    for y in range(-outline_range, outline_range+1):
                            draw.text((text_pos[0]+x, text_pos[1]+y), line, (0,0,0), font=font)

            draw.text(text_pos, line, (255,255,255), font=font)
            line_num += 1

    img.save(out_filename)


def get_fontsize(image_size, text):
	# find biggest font size that works
	font_size = int(image_size[1]/10)
	font = ImageFont.truetype(font_file, font_size)
	text_size = font.getsize(text)
	while text_size[0] > image_size[0]-20:
		font_size = font_size - 1
		font = ImageFont.truetype(font_file, font_size)
		text_size = font.getsize(text)
	return font_size


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
