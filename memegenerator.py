# -*- coding: utf-8 -*-

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import sys


def make_meme(topStrings, bottomStrings, filename):

	img = Image.open(filename)
	imageSize = img.size


	draw = ImageDraw.Draw(img)

	fontsizes = []
	for topString in topStrings:
		fontsizes.append(get_fontsize(imageSize, topString))
	for bottomString in bottomStrings:
		fontsizes.append(get_fontsize(imageSize, bottomString))
	fontSize = min(fontsizes)
	font = ImageFont.truetype("font.ttf", fontSize)

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
	img.save("temp.png")

def get_fontsize(imageSize, text):
	# find biggest font size that works
	fontSize = int(imageSize[1]/10)
	font = ImageFont.truetype("font.ttf", fontSize)
	textSize = font.getsize(text)
	while textSize[0] > imageSize[0]-20:
		fontSize = fontSize - 1
		font = ImageFont.truetype("font.ttf", fontSize)
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

def get_upper(somedata):
	'''
	Handle Python 2/3 differences in argv encoding
	'''
	result = ''
	try:
		result = somedata.decode("utf-8").upper()
	except:
		result = somedata.upper()
	return result

def get_lower(somedata):
	'''
	Handle Python 2/3 differences in argv encoding
	'''
	result = ''
	try:
		result = somedata.decode("utf-8").lower()
	except:
		result = somedata.lower()

	return result



if __name__ == '__main__':

	args_len = len(sys.argv)
	topString = ''
	meme = 'standard'

	if args_len == 1:
		# no args except the launch of the script
		print('args plz')

	elif args_len == 2:
		# only one argument, use standard meme
		bottomString = get_upper(sys.argv[-1])

	elif args_len == 3:
		# args give meme and one line
		bottomString = get_upper(sys.argv[-1])
		meme = get_lower(sys.argv[1])

	elif args_len == 4:
		# args give meme and two lines
		topString = get_upper(sys.argv[-2])
		bottomString = get_upper(sys.argv[-1])
		meme = get_lower(sys.argv[1])
	else:
		# so many args
		# what do they mean
		# too intense
		print('to many argz')

	print(meme)
	filename = str(meme)+'.jpg'
	make_meme(topString, bottomString, filename)
