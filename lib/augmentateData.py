import os, cv2, itertools, multiprocessing, random
import imgaug as ia
import imgaug.augmenters as iaa
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from lib.aux import *
from lib.analyseProject_functions.analyseProject_Classes import *
from lib.analyseProject_functions.analyseProject_Images import *
from lib.analyseProject_functions.analyseProject_CheckErrors import *
from lib.analyseProject_functions.analyseProject_EditProject import *

aug1 = iaa.ElasticTransformation(alpha=70.0, sigma=13.0)
aug2 = iaa.Fliplr(1)
aug3 = iaa.GaussianBlur(sigma=4)
aug4 = iaa.AveragePooling(kernel_size=2)
aug5 = iaa.PerspectiveTransform(scale=0.05)
aug6 = iaa.PiecewiseAffine(scale=0.05,nb_rows=2,nb_cols=2)
aug7 = iaa.pillike.EnhanceSharpness(factor=5)
aug8 = iaa.GammaContrast(gamma=1.5)

def augment_seg(img,seg,seq):
    aug_det = seq.to_deterministic() 
    image_aug = aug_det.augment_image(img)
    segmap = ia.SegmentationMapsOnImage( seg , shape=img.shape )
    segmap_aug = aug_det.augment_segmentation_maps( segmap )
    segmap_aug = segmap_aug.get_arr()

    return image_aug , segmap_aug

def aug_process(j,prmt,i,prjName,images,masks,counter,permutations):
    if not os.path.exists(f'projects/{prjName}/augmented/{i}/{j}/img'):
        os.makedirs(f'projects/{prjName}/augmented/{i}/{j}/img')
    if not os.path.exists(f'projects/{prjName}/augmented/{i}/{j}/masks'):
        os.makedirs(f'projects/{prjName}/augmented/{i}/{j}/masks')

    seq = iaa.Sequential(prmt)

    for k,img in enumerate(images):
        image_aug,segmap_aug = augment_seg(
            cv2.imread(f'projects/{prjName}/img/{img}'),
            cv2.imread(f'projects/{prjName}/masks/{masks[k]}'),
            seq
        )
        cv2.imwrite(f'projects/{prjName}/augmented/{i}/{j}/img/{img}_{i}-{j}-{k}', image_aug)
        cv2.imwrite(f'projects/{prjName}/augmented/{i}/{j}/masks/{masks[k]}_{i}-{j}-{k}', segmap_aug)

        with counter.get_lock(): counter.value += 1
        printProgressBar(counter.value, permutations*len(images), prefix = 'Augmenting:', suffix = f'({counter.value}/{permutations*len(images)}) Complete', length = 50)


def augmentateData(prj):

    # Stores tick and cross symbols for the menu 
    tick = dict([(True, f'{bcolors.OKGREEN}{bcolors.BOLD}✔{bcolors.ENDC}'), (False, f'{bcolors.FAIL}{bcolors.BOLD}✘{bcolors.ENDC}')])

    #Global vars
    prjName = prj.name
    images = sorted(os.listdir(f'projects/{prjName}/img'))
    masks = sorted(os.listdir(f'projects/{prjName}/masks'))

    #Stores the augmenters
    augmenters = [aug1,aug2,aug3,aug4,aug5,aug6,aug7,aug8]

    #Stores which augmenters will be used
    parameters = [True for aug in augmenters]
    
    while True:
        all_permutations = []
        chose_augmenters = [aug for i,aug in enumerate(augmenters) if parameters[i]]

        for i,e in enumerate(chose_augmenters):
            #if i<1: continue
            p = list(itertools.permutations(chose_augmenters,i+1))
            all_permutations.append(p)

        permutations = 0
        for e in all_permutations:
            permutations += len(list(e))

        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'{bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)}')
        print(f'{bcolors.BOLD}Permutations:{bcolors.ENDC} {permutations}')

        print("""
            \n
            Toggle options
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            {0} 1 : Elastic Transformation    
            {1} 2 : Flip vertical axis      
            {2} 3 : Gaussian Blur           
            {3} 4 : Average Pooling         
            {4} 5 : Perspective ransform    
            {5} 6 : Piecewise Affine    
            {6} 7 : Enhance Sharpness      
            {7} 8 : Gamma Contrast          

            9 : Augmentate     
            0 : Exit""".format(*(''.join(tick[opt]) for opt in parameters)))

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif 1 <= int(choice) <= 8:
            parameters[int(choice)-1] = not parameters[int(choice)-1]

        elif choice == '9':

            if not os.path.exists(f'projects/{prjName}/augmented'):
                os.makedirs(f'projects/{prjName}/augmented')

            # Create a global variable.
            counter = multiprocessing.Value("i", 0, lock=True)

            printProgressBar(0, permutations * len(images), prefix = 'Augmenting:', suffix = f'({counter.value}/{permutations*len(images)}) Complete', length = 50)

            for i,prmt_list in enumerate(all_permutations):
                if not os.path.exists(f'projects/{prjName}/augmented/{i}'):
                    os.makedirs(f'projects/{prjName}/augmented/{i}')

                
                processes =  []
                for j,prmt in enumerate(prmt_list):
                    p = multiprocessing.Process(target=aug_process, args=(j,prmt,i,prjName,images,masks,counter,permutations))
                    processes.append(p)
                    p.start()

                for p in processes:
                    p.join()

            input(f'\nContinue...')      

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')