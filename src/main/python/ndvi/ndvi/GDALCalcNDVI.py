#! /usr/bin/env python

# Import required libraries from python
import sys
import struct
# Import gdal
import osgeo.gdal as gdal

# Define the class GDALCalcNDVI
class GDALCalcNDVI(object):

    # A function to create the output image
    @staticmethod
    def create_output_image(out_filename, in_dataset):
        # Define the image driver to be used 
        # This defines the output file format (e.g., GeoTiff)
        driver = gdal.GetDriverByName("GTiff")
        # Check that this driver can create a new file.
        metadata = driver.GetMetadata()
        if metadata.has_key(gdal.DCAP_CREATE) \
        and metadata[gdal.DCAP_CREATE] == 'YES':
            print 'Driver GTiff supports Create() method.'
        else:
            print 'Driver GTIFF does not support Create()'
            sys.exit(-1)
        # Get the spatial information from the input file
        geo_transform = in_dataset.GetGeoTransform()
        geo_projection = in_dataset.GetProjection()
        # Create an output file of the same size as the inputted 
        # image but with only 1 output image band.
        new_dataset = driver.Create(out_filename, in_dataset.RasterXSize, \
                     in_dataset.RasterYSize, 1, gdal.GDT_Float32)
        # Define the spatial information for the new image.
        new_dataset.SetGeoTransform(geo_transform)
        new_dataset.SetProjection(geo_projection)
        return new_dataset
        
    # The function which loops through the input image and
    # calculates the output NDVI value to be outputted.    
    def calc_ndvi(self, file_path, out_file_path):
        # Open the inputted dataset
        dataset = gdal.Open(file_path, gdal.GA_ReadOnly)
        # Check the dataset was successfully opened
        if dataset is None:
            print "The dataset could not openned"
            sys.exit(-1)

        # Create the output dataset
        out_dataset = self.create_output_image(out_file_path, dataset)
        # Check the datasets was successfully created.
        if out_dataset is None:
            print 'Could not create output image'
            sys.exit(-1)

        # Get hold of the RED and NIR image bands from the image
        # Note that the image bands have been hard coded
        # in this case for the Landsat sensor. RED = 3
        # and NIR = 4 this might need to be changed if 
        # data from another sensor was used.
        red_band = dataset.GetRasterBand(3) # RED BAND
        nir_band = dataset.GetRasterBand(4) # NIR BAND
       
        num_lines = red_band.YSize 
        # Loop through each line in turn.
        for line in range(num_lines):
            # Define variable for output line.
            output_line = ''
            # Read in data for the current line from the 
            # image band representing the red wavelength
            red_scanline = red_band.ReadRaster(0, line, red_band.XSize, 1, \
                           red_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            red_tuple = struct.unpack('f' * red_band.XSize, red_scanline)
            
            # Read in data for the current line from the 
            # image band representing the NIR wavelength
            nir_scanline = nir_band.ReadRaster(0, line, nir_band.XSize, 1, \
                           nir_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            nir_tuple = struct.unpack('f' * nir_band.XSize, nir_scanline)

            # Loop through the columns within the image
            for i in range(len(red_tuple)):
                # Calculate the NDVI for the current pixel.
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi = 0
                # Be careful of zero divide 
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    ndvi = ndvi_upper/ndvi_lower
                # Add the current pixel to the output line
                output_line = output_line + struct.pack('f', ndvi)
            # Write the completed line to the output image
            out_dataset.GetRasterBand(1).WriteRaster(0, line, red_band.XSize, 
                        1, output_line, buf_xsize=red_band.XSize, 
                        buf_ysize=1, buf_type=gdal.GDT_Float32)
            # Delete the output line following write
            del output_line
        print 'NDVI Calculated and Outputted to File'
