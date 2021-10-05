import time
import numpy as np
from tifffile import imread


# takes 35 secs on my PC, likely because the for-loops business
def v1(i):
	# flat version of the image
	i_flat = i.ravel()

	# some shortcuts...
	xLine = i.shape[2]
	xySlice = i.shape[1]*xLine

	sum = 0
	for z in range(i.shape[0]):
		base_z = z * xySlice
		for y in range(i.shape[1]):
			base_zy = base_z + y*xLine
			for x in range(i.shape[2]):
				v = i_flat[base_zy + x]
				sum += v
	return sum

# takes 36 secs on my PC, slowed down likely by the 'off' increments
def v1_T(i):
	# flat version of the image
	i_flat = i.ravel()

	maxZ,maxY,maxX = i.shape
	off = 0

	sum = 0
	for z in range(maxZ):
		for y in range(maxY):
			for x in range(maxX):
				v = i_flat[off]
				sum += v
				off += 1
	return sum


# takes 27 secs on my PC
def v2(i):
	# flat version of the image
	sum = 0
	for v in i.ravel():
		sum += v
	return sum


# takes 29 secs on my PC
# 3 secs penalty for learning where we are in the image
def v3(i):
	sum = 0
	for offset,v in enumerate(i.ravel()):
		sum += v
	return sum


def convertNeigIndicesIntoOffsets_3D(ref_img, neigh_list): 
    xLine = ref_img.shape[2]
    xySlice = ref_img.shape[1]*xLine

    ret_offsets = []
    for dx,dy,dz in neigh_list:
        offset = dx + dy*xLine + dz*xySlice
        ret_offsets.append(offset)

    # make cache happy
    return sorted(ret_offsets)


def find_borders_3D(img,neigh_list):
	# re-arranges order of the offsets!
	# (assumes order is not important for the algorithm itself)
	neigh_offsets = convertNeigIndicesIntoOffsets_3D(img,neigh_list)
	print("orig list: "+str(neigh_list))
	print(" new list: "+str(neigh_offsets))

	# assumes neigh_list has "radius" max 1px!
	neigh_rad = 1

	# assumes img is large enough!
	# (so that maxX remains a strictly-positive integer)
	maxZ,maxY,maxX = img.shape
	maxX -= neigh_rad+neigh_rad
	maxY -= neigh_rad+neigh_rad
	maxZ -= neigh_rad+neigh_rad
	# NB: shortens each dim by the "border zone" of the neighs

	# flat version of the image, and its "running offset"
	img_flat = img.ravel()
	off = 0

	borderPxs = 0
	off += neigh_rad * img.shape[1]*img.shape[2]  # skip neigh_rad xy-planes
	for z in range(maxZ):
		off += neigh_rad * img.shape[2]            # skip neigh_rad x-rows
		for y in range(maxY):
			off += neigh_rad                        # skip neigh_rad y-columns
			for x in range(maxX):

				v = img_flat[off]
				if v != 0:
					# fg pixel, check its neighbors
					for doff in neigh_offsets:
						if v != img_flat[off+doff]:
							borderPxs += 1
							break

				off += 1
			off += neigh_rad                        # skip neigh_rad y-columns
		off += neigh_rad * img.shape[2]            # skip neigh_rad x-rows

	return borderPxs


def find_borders_3D_v2(img,neigh_list):
	# re-arranges order of the offsets!
	# (assumes order is not important for the algorithm itself)
	neigh_offsets = convertNeigIndicesIntoOffsets_3D(img,neigh_list)
	print("orig list: "+str(neigh_list))
	print(" new list: "+str(neigh_offsets))

	# assumes neigh_list has "radius" max 1px!
	neigh_rad = 1

	# assumes img is large enough!
	# (so that maxX remains a strictly-positive integer)
	maxZ,maxY,maxX = img.shape
	maxX -= neigh_rad+neigh_rad
	maxY -= neigh_rad+neigh_rad
	maxZ -= neigh_rad+neigh_rad
	# NB: shortens each dim by the "border zone" of the neighs

	# flat version of the image, and its "running offset"
	#img_flat = [ v for v in img.ravel() ]
	img_flat = img.ravel()   # native arrays are a bit faster, but it takes time to create them
	print(type(img_flat))
	print(type(img.ravel()))
	print(len(img_flat))
	off = 0

	borderPxs = 0
	off += neigh_rad * img.shape[1]*img.shape[2]  # skip neigh_rad xy-planes
	for z in range(maxZ):
		off += neigh_rad * img.shape[2]            # skip neigh_rad x-rows
		for y in range(maxY):
			off += neigh_rad                        # skip neigh_rad y-columns
			for x in range(maxX):
				borderPxs += img_flat[off]           # isn't helping... every mem access slows it down,
				borderPxs += img_flat[off+44234]     # even when accessing the mem-place again! wtf!?
				borderPxs += img_flat[off+44234]     # NB: using Python's native lists is not helping either

#				v = img_flat[off] \
#					+ img_flat[off+neigh_offsets[0]] \
#					+ img_flat[off+neigh_offsets[1]] \
#					+ img_flat[off+neigh_offsets[2]] \
#					+ img_flat[off+neigh_offsets[3]] \
#					+ img_flat[off+neigh_offsets[4]] \
#					+ img_flat[off+neigh_offsets[5]]
#
#			for a,b,c in zip(img_flat[off:off+maxX], img_flat[off-850084:], img_flat[off-922:]):
#				borderPxs += a+b+c
#
				off += 1
			off += neigh_rad                        # skip neigh_rad y-columns
		off += neigh_rad * img.shape[2]            # skip neigh_rad x-rows

	return borderPxs

#
#
# >>> l = [1,2,3,4,5,6,7,8,9]
# >>> for a,b,c in zip(l[0:2],l[3:],l[5:]):
# ...     print(a,b,c)
# ... 
# 1 4 6
# 2 5 7
#
# NB: zip shifts and auto-shortens to yield parallel access to the same data


def find_borders_3D_v3(img,img_data,neigh_list):
	# re-arranges order of the offsets!
	# (assumes order is not important for the algorithm itself)
	neigh_offsets = convertNeigIndicesIntoOffsets_3D(img,neigh_list)
	print("orig list: "+str(neigh_list))
	print(" new list: "+str(neigh_offsets))

	# assumes neigh_list has "radius" max 1px!
	neigh_rad = 1

	# assumes img is large enough!
	# (so that maxX remains a strictly-positive integer)
	maxZ,maxY,maxX = img.shape

	# this determines inner region in which it is safe to sweep
	minOffset = neigh_rad*maxY*maxX + neigh_rad*maxX + neigh_rad
	maxOffset = len(img_data) - minOffset
	print("sweep offsets: "+str(minOffset)+" -> "+str(maxOffset))

	borderPxs = 0
	idx = 0
	# assumes there are exactly 6 neighbors!
	for v,a,b,c,d,e,f in zip(img_data[minOffset:maxOffset], \
	                         img_data[minOffset+neigh_offsets[0]:], \
	                         img_data[minOffset+neigh_offsets[1]:], \
	                         img_data[minOffset+neigh_offsets[2]:], \
	                         img_data[minOffset+neigh_offsets[3]:], \
	                         img_data[minOffset+neigh_offsets[4]:], \
	                         img_data[minOffset+neigh_offsets[5]:]):
		borderPxs += v + a+b+c+d+e+f
		idx += 1

	print("visited pixels: "+str(idx))
	return borderPxs


def benchmarks(i):
	a_time = time.time()
	sum_a = v3(i)
	b_time = time.time()
	sum_b = v1(i)
	c_time = time.time()
	sum_c = v1_T(i)
	d_time = time.time()

	print(sum_a)
	print("duration: "+str(b_time - a_time)+" secs")
	print(sum_b)
	print("duration: "+str(c_time - b_time)+" secs")
	print(sum_c)
	print("duration: "+str(d_time - c_time)+" secs")


i = imread('./data/masks_3D.tif')
# assuming 3D for now!
#benchmarks(i)

# flat version of the image as native Python list
i_data = [ v for v in i.ravel() ]

neigs = [[0,0,-1], [0,-1,0], [-1,0,0], [1,0,0], [0,1,0], [0,0,1]]
a_time = time.time()
print("found border pixels: "+str(find_borders_3D_v3(i,i_data,neigs)))
b_time = time.time()
print("duration: "+str(b_time - a_time)+" secs")

