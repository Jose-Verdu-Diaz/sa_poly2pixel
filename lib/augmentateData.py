import os, cv2, itertools, multiprocessing
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

def aug_process(j,prmt,i,prjName,images,masks,counter,sum):
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
        cv2.imwrite(f'projects/{prjName}/augmented/{i}/{j}/img/{img}', image_aug)
        cv2.imwrite(f'projects/{prjName}/augmented/{i}/{j}/masks/{masks[k]}', segmap_aug)

        with counter.get_lock(): counter.value += 1
        printProgressBar(counter.value, sum*len(images), prefix = 'Augmenting:', suffix = f'({counter.value}/{sum*len(images)}) Complete', length = 50)

def augmentateData(prj):
    prjName = prj.name
    images = sorted(os.listdir(f'projects/{prjName}/img'))
    masks = sorted(os.listdir(f'projects/{prjName}/masks'))
    
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'{bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)}')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Augmentate        ┃
            ┃ 2 : TEST              ┃            
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

            if not os.path.exists(f'projects/{prjName}/augmented'):
                os.makedirs(f'projects/{prjName}/augmented')

            elements = [aug1,aug2,aug4,aug5,aug6,aug7,aug8]
            all_permutations = []
            for i,e in enumerate(elements):
                if i<1 or i>1: continue
                p = list(itertools.permutations(elements,i+1))
                all_permutations.append(p)

            sum = 0
            for e in all_permutations:
                sum += len(list(e))

            # Create a global variable.
            counter = multiprocessing.Value("i", 0, lock=True)

            printProgressBar(0, sum * len(images), prefix = 'Augmenting:', suffix = f'({counter.value}/{sum*len(images)}) Complete', length = 50)

            for i,prmt_list in enumerate(all_permutations):
                if not os.path.exists(f'projects/{prjName}/augmented/{i}'):
                    os.makedirs(f'projects/{prjName}/augmented/{i}')

                '''
                aug_process_i=partial(aug_process, i=i, prjName=prjName,images=images,masks=masks)

                pool = multiprocessing.Pool()
                pool.starmap(aug_process_i,enumerate(prmt_list))
                # Close pool.
                pool.close()

                # Wait for all thread.
                pool.join()
                '''

                processes =  []
                for j,prmt in enumerate(prmt_list):
                    p = multiprocessing.Process(target=aug_process, args=(j,prmt,i,prjName,images,masks,counter,sum))
                    processes.append(p)
                    p.start()

                for p in processes:
                    p.join()

            input(f'\nContinue...')

        elif choice == '2':
            ims = []
            for file in sorted(os.listdir(f'projects/{prjName}/augmented/0')):
                print(file)
                ims.append(cv2.imread(f'projects/{prjName}/augmented/0/{file}/img/0001-0054.jpg'))

            fig = plt.figure()
            sequence = []
            for img in ims:
                im = plt.imshow(img, animated=True)
                im.axes.xaxis.set_visible(False)
                im.axes.yaxis.set_visible(False)
                sequence.append([im])

            ani = animation.ArtistAnimation(fig, sequence, interval=50, blit=True, repeat_delay=0)
            plt.show()

            input('Continue...')           

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')