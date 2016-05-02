import download_dhaga
import os

ru="https://video.fdel1-1.fna.fbcdn.net/v/t42.3356-2/12846742_1132460786764677_1149149623_n.mp4/video-1457605378.mp4?vabr=56316&oh=8231e1bfc7c22f992b2672f8bf61c765&oe=57286C17&dl=1"

start=0
end=3268183
download_dhaga.download(ru,start,end,".mp4")
os.rename("final.mp4","f1.mp4")

start=3268184
end=6536367
download_dhaga.download(ru,start,end,".mp4")
os.rename("final.mp4","f2.mp4")

f=open("ans.mp4","wb")
f1=open("f1.mp4","rb")
f2=open("f2.mp4","rb")
f.write(f1.read())
f.write(f2.read())
f1.close()
f2.close()
f.close()
