#!/usr/bin/env python
import site
import os
import sys

# import the ciop functtons (e.g. copy, log)
sys.path.append('/usr/lib/ciop/python/')
import cioppy as ciop

# add the local packages where ndvi package is deployed
site.addsitedir('/application/share/python/lib/python2.6/site-packages')
# import the ndvi package 
import ndvi

# write a log entry
ciop.log('INFO', 'Calculating NDVI')

# create a local output folder for the NDVI results
output_path = os.environ['TMPDIR'] + '/' + 'output' 
os.makedirs(output_path)

# input comes from STDIN (standard input)
for line in sys.stdin:

    # line contains a reference to a catalogue entry
    ciop.log('INFO', 'input: ' + line)
    
    # ciop.copy extracts the path from the reference and downloads the Landsat product
    res = ciop.copy(line, os.environ['TMPDIR'])
    local_path = res[0].rstrip('\n')

    # print the Landsat local path in the log
    ciop.log('DEBUG', 'local path:' + local_path)    
    
    # create the output name using the dc:identifier metadata field
    identifier = ciop.casmeta("dc:identifier", line)[0].rstrip('\n')
    output_name = output_path + '/' + identifier + "_ndvi.tif"
    
    # calculate the NDVI
    obj = ndvi.GDALCalcNDVI()
    obj.calc_ndvi(local_path, output_name)

    # use ciop.publish to publish the NDVI result 
    # use the URL returned by ciop.publish as the catalogue online resource info
    pub = ciop.publish(output_name, driver='s3')

    ciop.log('DEBUG', pub[0])
    # create the NDVI result metadata information 
    # using ciop.casmeta function to access the input product metadata
    metadata = [ "ical:dtstart=" + ciop.casmeta("ical:dtstart", line)[0].rstrip('\n'), 
                "ical:dtend=" + ciop.casmeta("ical:dtend", line)[0].rstrip('\n'),
                "dc:identifier=" + identifier + "_NDVI",
                "dct:spatial=" + ciop.casmeta("dct:spatial", line)[0].rstrip('\n'), 
                "dclite4g:onlineResource=" + pub[0].rstrip()]

    #metadata = [ "ical:dtstart=" + ciop.casmeta("ical:dtstart", line)[0].rstrip('\n'), 
    #            "ical:dtend=" + ciop.casmeta("ical:dtend", line)[0].rstrip('\n'),
    #            "dc:identifier=" + identifier + "_NDVI",
    #            "dct:spatial=" + ciop.casmeta("dct:spatial", line)[0].rstrip('\n'), 
    #            "dclite4g:onlineResource=http://some.host.com/myproduct.tif"]   
 
 
    ciop.log('DEBUG', 'Register the result in the sandbox catalogue')

    # use ciop.register providing the sandbox local catalogue and 
    # a series template
    ciop.register('http://localhost/catalogue/sandbox/rdf',
                    'file:///application/py-ndvi/etc/series.rdf',
                    metadata)

    #ciop.publish(output_name, metalink = True)

ciop.log('INFO', 'Done my share of the work!')
