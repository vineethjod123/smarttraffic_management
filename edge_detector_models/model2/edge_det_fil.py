import numpy as np
import cv2
import math
# from matplotlib import pyplot as plt
import sys

def sobelOperator(img):
    container = np.copy(img)
    container = container.tolist()
    size = [len(container),len(container[0])]
    # print(1,size)
    gx = 0
    gy = 0
    for i in range(1, size[0] - 1):
        for j in range(1, size[1] - 1):
            gx = (img[i - 1][j - 1] + 2*img[i][j - 1] + img[i + 1][j - 1]) - (img[i - 1][j + 1] + 2*img[i][j + 1] + img[i + 1][j + 1])
            gy = (img[i - 1][j - 1] + 2*img[i - 1][j] + img[i - 1][j + 1]) - (img[i + 1][j - 1] + 2*img[i + 1][j] + img[i + 1][j + 1])
            # gx = 0

            container[i][j] = min(255, math.sqrt(gx**2 + gy**2))
    # print(2)
    return container
    pass

# img = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2GRAY)
#print(img.shape)
# img = sobelOperator(img)
#print(img.shape)
# cv2.imshow("temp",img)
# arr = sys.argv[1].split(".")
# cv2.imwrite((arr[0]+"_edge2.png"),img)
#img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
#plt.imshow(img)
#plt.show()
#plt.savefig(arr[0]+"_edge.jpg")
