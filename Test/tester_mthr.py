import unittest
import download_dhaga
import urllib2

class TestDownloadfn(unittest.TestCase):
  def test_dwth(self):
    rurl=raw_input()
    ext=raw_input()
    site = urllib2.urlopen(rurl)
    meta= site.info()
    size= meta.getheaders("Content-Length")[0]
    size=int(size)
    print "Total File size to be downloaded: "+str(size)
    download_dhaga.download(rurl,0,size-1,ext)
    f=open('final'+ext,'r')
    self.assertEqual(len(f.read()),size)

if __name__ == '__main__':
    unittest.main()