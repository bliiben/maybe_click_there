import urllib2
main = "http://dontclickhere.drivy.com/img/"

# Load until crashes
# You have to make sure that all file are >0 bytes
# As dowloads may fail sometimes.

for i in range ( 5000 ):
	name = "img"+str(i)
	req = urllib2.Request(main+name+".png")
	response = urllib2.urlopen(req)
	the_page = response.read()
	print ("loading : " + name+" length-" +str(len(the_page)))
	with open("img/"+name+".png", "wb") as file:
		file.write(the_page)