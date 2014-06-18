#!/usr/bin/env python
import site
import os
import sys

site.addsitedir('/application/share/python/lib/python2.6/site-packages')
#print sys.path
#os.environ['PYTHONUSERBASE'] = '/application/share/python'

#print 'Base:', site.USER_BASE
#print 'Site:', site.USER_SITE

import ndvi

sys.path.append('/usr/lib/ciop/python/')

import cioppy as ciop

ciop.log('INFO', 'Hello World')

#myvar = ciop.getparam('param1')

#ciop.log('DEBUG', 'value is: ' + myvar)

# input comes from STDIN (standard input)
for line in sys.stdin:
    ciop.log('INFO', 'input: ' + line)

    res = ciop.copy(line, os.environ['TMPDIR'])

    ciop.log('DEBUG', 'local path:' + res[0].rstrip('\n'))    
  
    obj = ndvi.GDALCalcNDVI()
  
    obj.calc_ndvi(res[0].rstrip(), '/tmp/pippo.tif')

    pub = ciop.publish('/tmp/pippo.tif')

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
