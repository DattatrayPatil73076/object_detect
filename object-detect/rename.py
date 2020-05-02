import os
n = 0
for file in os.scandir('./img'):
	os.rename(file, './img/test-img{:04}.jpg'.format(n+1))
	n+=1