# composite-rasters
Calculates mean/median raster composites from a list of files. 

Create instance of Composite() class with list of files, output file prefix and mean/median as arguments

`C = Composite([‘file1.tif’, 'file2.tif’], fileprefix=‘result_’, calculation=‘mean’)`

Call the composite() method, which chains together the other methods.

`C.composite()`
