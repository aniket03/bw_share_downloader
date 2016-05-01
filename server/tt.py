import download_dhaga
import os

ru="http://apps.appolice.gov.in/ips/Templates/MajorHeadTemplates/Harry%20Potter%20and%20the%20Deathly%20Hallows%20[REAL]%20[PDF]%20[CLEAN].pdf"

start=0
end=747234
download_dhaga.download(ru,start,end,".pdf")
os.rename("final.pdf","f1.pdf")

start=747235
end=1494469
download_dhaga.download(ru,start,end,".pdf")
os.rename("final.pdf","f2.pdf")

f=open("ans.pdf","wb")
f1=open("f1.pdf","rb")
f2=open("f2.pdf","rb")
f.write(f1.read())
f.write(f2.read())
f1.close()
f2.close()
f.close()
