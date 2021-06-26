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

            prj_path = f'projects/{prj.name}'
            output_path = f'{prj_path}/reduction_test'

            if not os.path.exists(f'{output_path}/L/img'): os.makedirs(f'{output_path}/L/img')
            if not os.path.exists(f'{output_path}/L/masks'): os.makedirs(f'{output_path}/L/masks')
            if not os.path.exists(f'{output_path}/R/img'): os.makedirs(f'{output_path}/R/img')
            if not os.path.exists(f'{output_path}/R/masks'): os.makedirs(f'{output_path}/R/masks')

            for file in sorted(os.listdir(f'{prj_path}/img')):
        
                img = cv2.imread(f'{prj_path}/img/{file}', cv2.IMREAD_GRAYSCALE)
                mask = cv2.imread(f'{prj_path}/masks/{file.strip(".jpg")}.bmp', cv2.IMREAD_GRAYSCALE)

                centroids = []

                success = False
                for th in np.arange(20, 101, 5).tolist():
                    ret, thresh = cv2.threshold(img,th,255,cv2.THRESH_BINARY)    

                    # Remove white noise in mask
                    kernel = np.ones((2,2),np.uint8)
                    thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1) 

                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    if len(contours)==2:
                        # Make sure that both contours are legs
                        if cv2.contourArea(contours[0])*0.8 <= cv2.contourArea(contours[1]) <= cv2.contourArea(contours[0])*1.2:                  
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
                        legs = {'left':contours[1], 'right':contours[0]}
                        centroids = {'left':centroids[1], 'right':centroids[0]}

                    elif centroids[0][0] < centroids[1][0]:
                        legs = {'left':contours[0], 'right':contours[1]}
                        centroids = {'left':centroids[0], 'right':centroids[1]}
                            
                    else: print('Error')

                background = np.zeros(img.shape, np.uint8)

                leg_L = cv2.drawContours(background.copy(), [legs['left']], -1, 255, -1)
                leg_R = cv2.drawContours(background.copy(), [legs['right']], -1, 255, -1)

                img_L = cv2.bitwise_and(img,img,mask = leg_L)
                img_R = cv2.bitwise_and(img,img,mask = leg_R)

                mask_L = cv2.bitwise_and(mask,mask,mask = leg_L)
                mask_R = cv2.bitwise_and(mask,mask,mask = leg_R)

                x_L,y_L,w_L,h_L = cv2.boundingRect(legs['left'])
                x_R,y_R,w_R,h_R = cv2.boundingRect(legs['right'])

                cropped_img_L = img_L[y_L:y_L+h_L, x_L:x_L+w_L]
                cropped_img_R = cv2.flip(img_R[y_R:y_R+h_R, x_R:x_R+w_R], 1)

                cropped_mask_L = mask_L[y_L:y_L+h_L, x_L:x_L+w_L]
                cropped_mask_R = cv2.flip(mask_R[y_R:y_R+h_R, x_R:x_R+w_R], 1)

                cv2.imwrite(f'{output_path}/L/img/{file.strip(".jpg")}_L.jpg', cropped_img_L, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                cv2.imwrite(f'{output_path}/R/img/{file.strip(".jpg")}_R.jpg', cropped_img_R, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

                cv2.imwrite(f'{output_path}/L/masks/{file.strip(".jpg")}_L.bmp', cropped_mask_L)
                cv2.imwrite(f'{output_path}/R/masks/{file.strip(".jpg")}_R.bmp', cropped_mask_R)

            input(f'\n{bcolors.OKGREEN}END...{bcolors.ENDC}')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')