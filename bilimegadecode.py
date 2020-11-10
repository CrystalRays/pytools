import os
import sys
def decode(path="."):
    for each in os.listdir(path):
        if ".py" in each:continue
        a=open(path+"/"+each,"rb")
        b=open(path+"/"+each+".webp","wb")
        b.write(a.read()[9:])

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv)<2:
        decode()
    else:
        decode(sys.argv[1])
        