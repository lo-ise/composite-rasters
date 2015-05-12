from osgeo import gdal
import numpy as np
import os
from datetime import datetime

class Composite:
    """
    Creates an averaged composite of any number of 
    individual single band rasters. 

    Inputs:
    filelist of rasters that need compositing
    calculation - with 'mean' or 'median'

    """

    def __init__(self, filelist, fileprefix='', calculation='mean'):
            
        self.filelist       = filelist
        if fileprefix is not '':
            self.composite_name = os.path.join(
                    os.path.dirname(self.filelist[0]), 
                    '{0}_{1}_composite.tif'.format(fileprefix, calculation)
                    )
        else:
            self.composite_name = os.path.join(
                    os.path.dirname(self.filelist[0]), 
                    '{0}_composite.tif'.format(calculation)
                    )

        g = gdal.Open(self.filelist[0])	
        self.proj   = g.GetProjection()
        self.outgeo = g.GetGeoTransform()
        


        self.nodata = g.GetRasterBand(1).GetNoDataValue()
        self.calculation = calculation

        arr = g.ReadAsArray()
        [self.cols, self.rows] = arr.shape


    def composite(self):
        """
        Creates a composite from the input files.
        Chains together methods required to complete composite

        """
        arr = self.getarray(self.filelist)
        arr = self.averagearr(arr, self.calculation)
        tif = self.savearr(arr, self.composite_name)



    def getarray(self, filelist):
        """
        Puts together a 3d array from the list of input files
        
        """

        g = gdal.Open(filelist[0])
        x = g.ReadAsArray()

        [cols,rows] = x.shape

        new_arr = np.empty((len(filelist),cols,rows), dtype=np.float32)
        [dims,cols,rows] = new_arr.shape


        for f in filelist:
            i = filelist.index(f)
            g = gdal.Open(f)
            arr = g.ReadAsArray()
            new_arr[i,...] = arr
            g = None

        return new_arr


    def averagearr(self, arr, calculation):
        """
        Calculates a median or a mean array
        Default is mean, but this is specified when creating the instance
        of Composite().

        """

        med = np.array(arr[0,...], dtype=np.float32)
        [dims,cols,rows] = arr.shape

        for i in range(0,cols-1):
            for j in range(0,rows-1):
                values   = np.array(arr[...,i,j], dtype=np.float32)
                values_m = np.ma.masked_where(values == self.nodata, values)
                if calculation == 'mean':
                    new_val = np.mean(values_m)
                if calculation == 'median':
                    new_val = np.median(values_m)
                med[i,j] = new_val
        
        return med	


    def savearr(self, arr, outputname):
        """
        Saves the output file as a geotiff
        """
        
        outfile = gdal.GetDriverByName("GTiff")
        dst_ds  = outfile.Create(outputname, self.rows, self.cols, 1, gdal.GDT_Float32)
        dst_ds.SetProjection(self.proj)
        dst_ds.SetGeoTransform(self.outgeo)

        dst_ds.SetMetadataItem('UNITS', 'Percentage %')
        dt  = datetime.now()
        dts = dt.strftime('%Y-%m-%d')
        dst_ds.SetMetadataItem('CREATION_DATE', dts)

        band = dst_ds.GetRasterBand(1)
        band.WriteArray(arr)
        if self.nodata is not None:
            band.SetNoDataValue(self.nodata)



