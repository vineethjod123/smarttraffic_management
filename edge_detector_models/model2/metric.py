import numpy as np
import cv2
import sys
import os
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from edge_det_fil import *
import time
def count_white(image1,image2):
    ans= 0
    ans1 = 0
    image1 = sobelOperator(image1)
    print("ok")
    sz = [len(image1),len(image1[0])]
    # print(sz) 
    for i in range(sz[0]):
        for j in range(sz[1]):
            if(image1[i][j]>=150 and image2[i][j][0]==0 and image2[i][j][1]==0 and image2[i][j][2]==0):
                ans+=1
    return ans;


def count_white_ref(image1,image2):
    ans= 0
    a = 0
    b = c = d = e = 0
    ans1 = 0
    color = [0,0,0]
    sz = image1.shape
    image1 = image1.tolist()
    image2 = image2.tolist()
    for i in range(sz[0]):
        for j in range(sz[1]):
            if(image2[i][j][0]==0 and image2[i][j][1]==0 and image2[i][j][2]==0):
                ans1+=1;
                if(image1[i][j]>0):
                    ans+=1
                if(image1[i][j]>=50):
                    a+=1
                if(image1[i][j]>=100):
                    b+=1
                if(image1[i][j]>=150):
                    c+=1
                if(image1[i][j]>=200):
                    d+=1
    print(ans,a,b,c,d,ans1)
    return [ans,a,b,c,d];


def compare(image1,image2):
    cnt1 = count_white(image1)
    cnt2 = count_white(image2)
    print("compe",cnt2)
    print(image2.shape[1]*image2.shape[0])
    return (cnt2-cnt1)/cnt1;

def states(image):
    arr = np.zeros((image.shape[0]*image.shape[1]));
    temp = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            arr[temp] = image[i][j]
            temp+=1
    return (np.mean(arr),np.median(arr),stats.mode(arr))




def control():
    img1 = cv2.cvtColor(cv2.imread(sys.argv[1]),cv2.COLOR_BGR2GRAY)#yyp sys.argv[1]
    img2 = cv2.cvtColor(cv2.imread(sys.argv[2]),cv2.COLOR_BGR2GRAY)#yyp sys.argv[1]
    #img2 = cv2.imread(sys.argv[2])#yyp sys.argv[1]
    print(img1.shape)
    print(states(img1))
    print(states(img2))
    print(compare(img1,img2))


def distribution(ref):
    images = os.listdir("./data")
    cnt = 0
    f = open("distribution1.txt", "a")
    for image in images:
        name = './data/'+image
        print(image)
        print(cnt)
        img = cv2.cvtColor(cv2.imread(name),cv2.COLOR_BGR2GRAY)
        img = sobelOperator(img.tolist())
        print("ok")
        img = np.array(img)
        data = count_white_ref(img,ref)
        f.write(image+" ")
        for val in data:
            f.write(str(val)+" ")
        f.write("\n")
        cnt+=1
    f.close()
    return 



def run():
    img1 = cv2.cvtColor(cv2.imread(sys.argv[1]),cv2.COLOR_BGR2GRAY)#yyp sys.argv[1]
    img2 = cv2.imread(sys.argv[2])#yyp sys.argv[1]
    count_white_ref(img1,img2)

def extract_data():
    img2 = cv2.imread(sys.argv[2])#yyp sys.argv[1]
    distribution(img2)

def calc_density():
    img2 = cv2.imread(sys.argv[2]).tolist()#yyp sys.argv[1]
    img1 = cv2.cvtColor(cv2.imread(sys.argv[1]),cv2.COLOR_BGR2GRAY).tolist()
    return count_white(img1,img2)/21600*62

start = time.time()
print(calc_density())
# extract_data()
end = time.time()
print(f"Runtime of the program is {end - start}")


# extract_data()
#run()
