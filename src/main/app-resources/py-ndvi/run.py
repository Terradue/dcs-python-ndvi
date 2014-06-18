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
output.path = os.environ['TMPDIR'] + '/output' 
os.makedirs(output.path)

# input comes from STDIN (standard input)
for line in sys.stdin:

    # line contains a reference to a catalogue entry
    ciop.log('INFO', 'input: ' + line)
    
    # ciop.copy extracts the path from the reference and downloads the Landsat product
    res = ciop.copy(line, os.environ['TMPDIR'])
    local.path = res[0].rstrip('\n')

    # print the Landsat local path in the log
    ciop.log('DEBUG', 'local path:' + local.path )    
    
    # create the output name 
    output.name = output.path + '/' + os.path.splitext(os.path.basename(local.path))[0] + "_ndvi.tif"
    
    # calculate the NDVI
    obj = ndvi.GDALCalcNDVI()
    obj.calc_ndvi(local.path, output.name)

    # use ciop.publish to publish the NDVI result 
    # use the URL returned by ciop.publish as the catalogue online resource info
    pub = ciop.publish(output.name)

    # create the NDVI result metadata information 
    # using ciop.casmeta
    metadata = [ "ical:dtstart=2001-01-10T14:00:00", 
                "ical:dtend=2001-01-10T14:05:00",
                "dc:identifier=mydataset",
                "dct:spatial=MULTIPOLYGON(((25.55215 36.97701,24.740512 37.091395,24.496927 35.950137,25.284346 35.839142,25.55215 36.97701)))",
                "dclite4g:onlineResource=" + pub[0].rstrip()]

    metadata = [ "ical:dtstart=2001-01-10T14:00:00",
                "ical:dtend=2001-01-10T14:05:00",
                "dc:identifier=mydataset",
                "dct:spatial=MULTIPOLYGON(((25.55215 36.97701,24.740512 37.091395,24.496927 35.950137,25.284346 35.839142,25.55215 36.97701)))",
                "dclite4g:onlineResource=http://some.host.com/myproduct.tif"]   
 
    ciop.log('DEBUG', 'Going to register')

    ciop.register('http://localhost/catalogue/sandbox/rdf',
                    'file:///application/py-ndvi/etc/series.rdf',
                    metadata)

    ciop.publish('/tmp/pippo.tif', metalink = True)

ciop.log('INFO', 'Done my share of the work!')
