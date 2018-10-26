import os
import gdal

coefs = (0.000010, -0.012166, 4.335928)

source_file = "/home/tepex/AARI/SAGA/simulation/dem_2018.tif"  # this should be a DEM for year 2018

print "started"

for year in range(2017, 1998, -1):

	print year

	out_file = "/home/tepex/AARI/SAGA/simulation/dem_" + str(year) + ".tif"

	cmd = 'gdal_calc.py -A %s --outfile=%s --NoDataValue=-99999 --calc="A + %s * A**2 + %s * A + %s"' % (source_file, out_file, coefs[0], coefs[1], coefs[2])

	print "Year %s" % year
	#print cmd

	os.system(cmd)

	source_file = out_file
