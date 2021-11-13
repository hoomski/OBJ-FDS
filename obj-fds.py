#!/usr/bin/env python

import sys

with open(sys.argv[1], 'r') as obj_file:

	obst = []
	box = []
	line = obj_file.readline()

	while line != '':
		if line.startswith('o'):
			for j in range(10):
				box.append(line)
				line = obj_file.readline()
			obst.append(box)
			box = []
			if line.startswith('v'):
				print("\n!!! Warning: Nested object nr %d: *%s* !!!\n" %(len(obst), obst[len(obst)-1][0].rstrip()))	
		else:
			line = obj_file.readline()


#Wydruk obiektow w celach tesotwych
for a in range(len(obst)):
	for b in range(10):
		print(obst[a][b].rstrip())
		obst[a][b] = obst[a][b].split()
	print("\n")

#Konwersja do sixtupletu XB
obst_xb = []
box_xb = []
for a in range(len(obst)):
	for b in range(10):
		if b == 0:
			box_xb.append(obst[a][b][1])
		if b == 1:
			box_xb.append(map(ord, obst[a][b][1][6:].decode('hex')))
		if b == 2:
			x1 = float(obst[a][b][1])
			y1 = float(obst[a][b][2])
			z1 = float(obst[a][b][3])
		if b > 1 and b < 10:
			if float(obst[a][b][1]) != x1:
				x2 = float(obst[a][b][1])
				if x1 > x2:
					temp = x1
					x1 = x2
					x2 = temp
			if float(obst[a][b][2]) != y1:
				y2 = float(obst[a][b][2])
				if y1 > y2:
					temp = y1
					y1 = y2
					y2 = temp
			if float(obst[a][b][3]) != z1:
				z2 = float(obst[a][b][3])
				if z1 > z2:
					temp = z1
					z1 = z2
					z2 = temp
	box_xb.append(x1)
	box_xb.append(x2)
	box_xb.append(y1)
	box_xb.append(y2)
	box_xb.append(z1)
	box_xb.append(z2)
	obst_xb.append(box_xb)
	box_xb = []
#Koniec konwersji do XB

#Wydruk obiektow w celach tesotwych
#for a in range(len(obst_xb)):
#	for b in range(8):
#		print(obst_xb[a][b])
#	print("\n")

#Zapis do pliku .fds

with open(sys.argv[1].replace("obj", "fds"), 'w') as fds_file:
	for a in range(len(obst_xb)):
		fds_file.write("&OBST XB= ")
		for b in range(2,8):
			obst_xb[a][b] = '{0:.2f}'.format(obst_xb[a][b]/1000)
			fixed_width = "{0:>5}".format(str(obst_xb[a][b]))
			fds_file.write(fixed_width)
			fds_file.write(", ")
		fds_file.write("SURF_ID='surface', RGB= %3d, %3d, %3d" %(obst_xb[a][1][0], obst_xb[a][1][1], obst_xb[a][1][2]))
		fds_file.write(" / %s\n" %obst_xb[a][0])
