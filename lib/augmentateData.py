import os, cv2
import imgaug as ia
import imgaug.augmenters as iaa

from lib.aux import *
from lib.analyseProject_functions.analyseProject_Classes import *
from lib.analyseProject_functions.analyseProject_Images import *
from lib.analyseProject_functions.analyseProject_CheckErrors import *
from lib.analyseProject_functions.analyseProject_EditProject import *

seq1 = iaa.Sequential([
    iaa.Crop(px=(0, 16)), # crop images from each side by 0 to 16px (randomly chosen)
    iaa.Fliplr(0.5), # horizontally flip 50% of the images
    iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
])
seq2 = iaa.Sequential([
    iaa.Fliplr(1), # horizontally flip 50% of the images
])
seq3 = iaa.Sequential([
    iaa.GaussianBlur(sigma=4) # blur images with a sigma of 0 to 3.0
])

def augment_seg(img,seg):
    aug_det = seq3.to_deterministic() 
    image_aug = aug_det.augment_image(img)
    segmap = ia.SegmentationMapsOnImage( seg , shape=img.shape )
    segmap_aug = aug_det.augment_segmentation_maps( segmap )
    segmap_aug = segmap_aug.get_arr()

    return image_aug , segmap_aug

def augmentateData(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'{bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)}')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : TEST              ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':

            img = cv2.imread('/home/pepv/Practiques/Segm/MRIs/Tracked/RM1/img/0001-0050.jpg')
            print(img.shape)
            seg = cv2.imread('/home/pepv/Practiques/Segm/Software/sa_poly2pixel/projects/RM1/masks/0001-0050.bmp')
            image_aug,segmap_aug = augment_seg(img,seg)
            cv2.imwrite(f'projects/{prj.name}/img_test.bmp', image_aug)
            cv2.imwrite(f'projects/{prj.name}/seg_test.bmp', segmap_aug)

            input(f'\nContinue...')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')