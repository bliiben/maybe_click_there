from skimage import data, io
import numpy as np
import filecmp

#Create dictionnary containing known files
storedKnownValue = { }

def avgPerCell( imagename = "img/img3800.png" ):
	img = data.imread( imagename)

	#Cut images into 8 segments.
	length = len( img[0] )
	image_width = int(length/8)
	for i in range( 8 ):
		fro = image_width *i
		to = image_width*(i+1)
		cropped = img[0:len(img), fro:to]
		
		#Counter of "normal" blue
		blues = 0

		for x in range(0,len(cropped),10):
			for y in range(0,len(cropped[x]),10):
				color = cropped[x,y]

				# Just ignore if white
				if( np.sum(color) != 765 ):
					if( color[0] == 52 and color[1] == 132 and color[2] == 197):
						blues += 1
		yield blues



# Usualy around 75 blues per picture, so if there is enough we say it is a "normal" blue car
def decide ( blues ):
	return (blues >50)

# Extract the byte value from the picture
def getValue( imagename , reverse = False ):
	byte = ""
	for c in avgPerCell( imagename ):
		byte += '1' if decide(c) else '0'
	
	# Annoying thing, the normal blue becomes the inverse of its value,
	# so we need to inverse the bits on the last pictures
	if( reverse ):
		return int(byte,2) ^ 0b11111111
	else :
		return int(byte,2)
		

# Compute every img
def runThrough():
	logfile = open("logging.txt", "w")
	result = open("result.txt", "w")

	for i in range(3805) :
		filename = "img/img"+str(i)+".png"
		logfile.write(str(i)+" : ")
		v = None
		
		# The first and last type of images we use a dictionnary to store known images,
		# so we just have to compare known images to the dictionnary to know their value
		if( i <= 1356 or i >= 2685):
			for n in storedKnownValue:
				if ( filecmp.cmp(n,filename) ):
					v = storedKnownValue[n]
					break

		# In case it wasn't found in the dictionnary
		if( v == None ):
			# Annying reversing bits on latest group of images
			if( i < 2685):
				v = getValue(filename, False)
			else:
				v = getValue(filename, True)

			storedKnownValue[filename] = v

		# Log results
		logfile.write("value="+str(v)+"\n")
		result.write(chr(v))
		logfile.flush()
		result.flush()
		# Print progress
		print (i , v)

	logfile.close()
	result.close()

if __name__ == '__main__':
	runThrough()