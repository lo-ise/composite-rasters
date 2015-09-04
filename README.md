# composite-rasters

[![Code Climate](https://codeclimate.com/github/lo-ise/composite-rasters/badges/gpa.svg)](https://codeclimate.com/github/lo-ise/composite-rasters)

[![circleci](https://circleci.com/gh/lo-ise/composite-rasters.png?style=shield)](https://circleci.com/gh/lo-ise/composite-rasters)

Calculates mean/median raster composites from a list of files. 

Create instance of Composite() class with list of files, output file prefix and mean/median as arguments

`C = Composite([‘file1.tif’, 'file2.tif’], fileprefix=‘result_’, calculation=‘mean’)`

Call the composite() method, which chains together the other methods.

`C.composite()`
