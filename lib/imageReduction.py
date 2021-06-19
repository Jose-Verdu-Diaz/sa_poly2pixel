import os
from lib.aux import *
from lib.analyseProject_functions.analyseProject_Classes import *
from lib.analyseProject_functions.analyseProject_Images import *
from lib.analyseProject_functions.analyseProject_CheckErrors import *
from lib.analyseProject_functions.analyseProject_EditProject import *

import cv2
import numpy as np

def imageReduction(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'''
        {bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)} > {len(prj.images)*2}
        {bcolors.BOLD}Nº of classes:{bcolors.ENDC} {len(prj.classes) + 1} > {int(len(prj.classes)/2) + 1}
        ''')

        print("""
            This tool selects only the right/left leg to
            reduce the dimensions of the image and the
            amount of classes for image segmentation.

            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : TEST              ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        if choice == '0':
            return

        elif choice == '1':

            if not os.path.exists(f'projects/{prj.name}/reduction_test/L'):
                os.makedirs(f'projects/{prj.name}/reduction_test/L')
            if not os.path.exists(f'projects/{prj.name}/reduction_test/R'):
                os.makedirs(f'projects/{prj.name}/reduction_test/R')

            for file in sorted(os.listdir(f'projects/{prj.name}/img')):
        
                img = cv2.imread(f'projects/{prj.name}/img/{file}', cv2.IMREAD_GRAYSCALE)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                centroids = []

                success = False
                for th in np.arange(20, 101, 5).tolist():
                    ret, thresh = cv2.threshold(img,th,255,cv2.THRESH_BINARY)    

                    # Remove white noise in mask
                    kernel = np.ones((2,2),np.uint8)
                    thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1) 

                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    if len(contours)==2:                      
                        success = True
                        break

                if not success:
                    print(f'{bcolors.FAIL}ERROR ## {file} ## {len(contours)} contours{bcolors.ENDC}')
                    continue

                for i,c in enumerate(contours):
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    centroids.append((cX,cY))
                
                if len(centroids) > 2 or len(centroids) == 0:
                    print(f'Len of centroids is {len(centroids)}')
                else:
                    # Derecha: Azul
                    # Izquierda: Rojo
                        if centroids[0][0] > centroids[1][0]:
                            cv2.drawContours(img_rgb, [contours[1]], -1, (0, 0, 255), 2)
                            cv2.drawContours(img_rgb, [contours[0]], -1, (255, 0, 0), 2)
                            cv2.circle(img_rgb, centroids[1], 3, (0, 0, 255), -1)
                            cv2.circle(img_rgb, centroids[0], 3, (255, 0, 0), -1)
                
                        elif centroids[0][0] < centroids[1][0]:
                            cv2.drawContours(img_rgb, [contours[0]], -1, (0, 0, 255), 2)
                            cv2.drawContours(img_rgb, [contours[1]], -1, (255, 0, 0), 2)
                            cv2.circle(img_rgb, centroids[0], 3, (0, 0, 255), -1)
                            cv2.circle(img_rgb, centroids[1], 3, (255, 0, 0), -1)
                            
                        else: cv2.circle(img_rgb, (cX, cY), 3, (0, 255, 0), -1)

                background = np.zeros(img.shape, np.uint8)

                if centroids[0][0] > centroids[1][0]:
                    mask_L = cv2.drawContours(background.copy(), [contours[1]], -1, 255, -1)
                    mask_R = cv2.drawContours(background.copy(), [contours[0]], -1, 255, -1)

                elif centroids[0][0] < centroids[1][0]:
                    mask_L = cv2.drawContours(background.copy(), [contours[0]], -1, 255, -1)
                    mask_R = cv2.drawContours(background.copy(), [contours[1]], -1, 255, -1)

                else: pass

                img_L = cv2.bitwise_and(img,img,mask = mask_L)
                img_R = cv2.bitwise_and(img,img,mask = mask_R)

                if centroids[0][0] > centroids[1][0]:
                    x,y,w,h = cv2.boundingRect(contours[1])
                    box_L = cv2.rectangle(cv2.cvtColor(img_L, cv2.COLOR_GRAY2BGR),(x,y),(x+w,y+h),(0,255,0),2)
                    cropped_L = img_L[y:y+h, x:x+w]

                    x,y,w,h = cv2.boundingRect(contours[0])
                    box_R = cv2.rectangle(cv2.cvtColor(img_R, cv2.COLOR_GRAY2BGR),(x,y),(x+w,y+h),(0,255,0),2)
                    cropped_R = cv2.flip(img_R[y:y+h, x:x+w], 1)

                elif centroids[0][0] < centroids[1][0]:
                    x,y,w,h = cv2.boundingRect(contours[0])
                    box_L = cv2.rectangle(cv2.cvtColor(img_L, cv2.COLOR_GRAY2BGR),(x,y),(x+w,y+h),(0,255,0),2)
                    cropped_L = img_L[y:y+h, x:x+w]

                    x,y,w,h = cv2.boundingRect(contours[1])
                    box_R = cv2.rectangle(cv2.cvtColor(img_R, cv2.COLOR_GRAY2BGR),(x,y),(x+w,y+h),(0,255,0),2)
                    cropped_R = cv2.flip(img_R[y:y+h, x:x+w], 1)

                cv2.imwrite(f'projects/{prj.name}/reduction_test/L/{file.strip(".jpg")}_L.jpg', cropped_L, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                cv2.imwrite(f'projects/{prj.name}/reduction_test/R/{file.strip(".jpg")}_R.jpg', cropped_R, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            input(f'\n{bcolors.OKGREEN}END...{bcolors.ENDC}')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')