import unittest
from composite import Composite
import numpy as np
import os
from osgeo import gdal
from osgeo import osr
import shutil

class TestComp(unittest.TestCase):
    
    def setUp(self):
        """
        Sets up 3 2x2 arrays (self.arr1, self.arr2, self.arr3), 
        and from these:
        
          - writes 3 2x2 georeferenced geotiffs of different 
          values in a directory called 'test_composites'. 
          - creates a 3D array of these 3 arrays (self.arr)


        An instance of Composite (C) made with the a list of the 
        three geotiffs as input. 

        """

        self.arr1 = np.zeros((2, 2))
        count = 1
        for i in range(0, 2):
            for j in range(0, 2):
                self.arr1[i,j] = count
                count += 1

        self.arr2 = np.zeros((2, 2))
        count = 5
        for i in range(0, 2):
            for j in range(0, 2):
                self.arr2[i,j] = count
                count += 1

        self.arr3 = np.zeros((2, 2))
        count = 9
        for i in range(0, 2):
            for j in range(0, 2):
                self.arr3[i,j] = count
                count += 1

        self.arr = np.zeros((3, 2, 2))
        self.arr[0,...] = self.arr1
        self.arr[1,...] = self.arr2
        self.arr[2,...] = self.arr3

        os.mkdir('test_composites')

        self.outproj = osr.SpatialReference()
        self.outproj.SetWellKnownGeogCS("WGS84")        
        self.geotrans = [-180.0, 5, 0.0, 90.0, 0.0, -5]

        file_no = 1
        for a in [self.arr1, self.arr2, self.arr3]:
            
            outfile = gdal.GetDriverByName("GTiff")
            dst_ds  = outfile.Create('test_composites/file_{}.tif'.format(file_no), 2, 2, 1, gdal.GDT_Byte)
            
            dst_ds.SetProjection(self.outproj.ExportToWkt())
            dst_ds.SetGeoTransform(self.geotrans)

            band = dst_ds.GetRasterBand(1)
            band.WriteArray(a)
            file_no += 1

        self.filelist = ['test_composites/file_1.tif', 
                         'test_composites/file_2.tif',
                         'test_composites/file_3.tif']
        
        self.C = Composite(self.filelist)


    def test_create_arr(self):
        """
        Test to create a 3D array from input files. 

        Tests against self.arr which was created in 
        self.setUp()

        """
        test_arr = self.C.getarray(self.filelist)

        self.assertEqual(test_arr.all(), self.arr.all(), 'Composite.getarray produced wrong result')


    def test_average_arr(self):
        """
        Tests the mean and median calculation
        """
        
        av_arr_expected = np.array([[5, 6],[7, 8]])
        mean_arr_result = self.C.averagearr(self.arr, calculation='mean')
        median_arr_result = self.C.averagearr(self.arr, calculation='median')
        self.assertEqual(av_arr_expected.all(), mean_arr_result.all(), 'Mean calculation failed')
        self.assertEqual(av_arr_expected.all(), median_arr_result.all(), 'Median calculation failed')
       

    def test_save_arr(self):
        """
        Test whether the composite.savearr() method actually
        saves an array to a geotiff
        """

        self.C.savearr(self.arr1, 'test_composites/test_write.tif')
        self.assertTrue(os.path.exists('test_composites/test_write.tif'))


    def tearDown(self):
        shutil.rmtree('test_composites')



if __name__ == "__main__":
    unittest.main()
