import os, cv2, itertools, multiprocessing, shutil
import imgaug as ia
import imgaug.augmenters as iaa

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

def aug_process(j,prmt,i,prjName,images,masks,counter,permutations,aug_key, projectDir):
    name = ''
    for aug in prmt:
        name += str(aug_key[aug.__class__.__name__])

    if not os.path.exists(f'{projectDir}/{prjName}/augmented/{i+1}_prmt/{name}/img'):
        os.makedirs(f'{projectDir}/{prjName}/augmented/{i+1}_prmt/{name}/img')

    if not os.path.exists(f'{projectDir}/{prjName}/augmented/{i+1}_prmt/{name}/masks'):
        os.makedirs(f'{projectDir}/{prjName}/augmented/{i+1}_prmt/{name}/masks')

    seq = iaa.Sequential(prmt)

    for k,img in enumerate(images):
        image_aug,segmap_aug = augment_seg(
            cv2.imread(f'{projectDir}/{prjName}/img/{img}'),
            cv2.imread(f'{projectDir}/{prjName}/masks/{masks[k]}'),
            seq
        )
        cv2.imwrite(f'{projectDir}/{prjName}/augmented/{i+1}_prmt/{name}/img/{img.strip(".jpg")}-{i+1}_prmt-{name}-{k}.bmp', image_aug)
        cv2.imwrite(f'{projectDir}/{prjName}/augmented/{i+1}_prmt/{name}/masks/{masks[k].strip(".jpg")}-{i+1}_prmt-{name}-{k}.bmp', segmap_aug)

        with counter.get_lock(): counter.value += 1
        printProgressBar(counter.value, permutations*len(images), prefix = 'Augmenting:', suffix = f'({counter.value}/{permutations*len(images)}) Complete', length = 50)


def augmentateData(prj, config):

    # Stores tick and cross symbols for the menu 
    tick = dict([(True, f'{bcolors.OKGREEN}{bcolors.BOLD}✔{bcolors.ENDC}'), (False, f'{bcolors.FAIL}{bcolors.BOLD}✘{bcolors.ENDC}')])

    #Global vars
    prjName = prj.name
    images = sorted(os.listdir(f'{config["projectDir"]}/{prjName}/img'))
    masks = sorted(os.listdir(f'{config["projectDir"]}/{prjName}/masks'))

    #Stores the augmenters
    augmenters = [aug1,aug2,aug3,aug4,aug5,aug6,aug7,aug8]

    #Stores which augmenters will be used
    parameters = [True for aug in augmenters]
    
    while True:
        all_permutations = []
        chosen_augmenters = [aug for i,aug in enumerate(augmenters) if parameters[i]]

        for i,e in enumerate(chosen_augmenters):
            #if i<1: continue
            p = list(itertools.permutations(chosen_augmenters,i+1))
            all_permutations.append(p)

        permutations = 0
        for e in all_permutations:
            permutations += len(list(e))

        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'{bcolors.BOLD} Nº of input images:{bcolors.ENDC} {len(prj.images)}')
        print(f'{bcolors.BOLD}       Permutations:{bcolors.ENDC} {permutations}')
        print(f'{bcolors.BOLD}Nº of output images:{bcolors.ENDC} {len(prj.images) * permutations}')

        print("""
            \n
            Toggle options
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            {0} 1 : Elastic Transformation    
            {1} 2 : Flip vertical axis      
            {2} 3 : Gaussian Blur           
            {3} 4 : Average Pooling         
            {4} 5 : Perspective ransform    
            {5} 6 : Piecewise Affine (Slow)
            {6} 7 : Enhance Sharpness      
            {7} 8 : Gamma Contrast          

            9 : Augmentate     
            0 : Exit""".format(*(''.join(tick[opt]) for opt in parameters)))

        try:
            choice = int(input("\nEnter your choice : "))
        except:
            choice = -1

        if choice == -1:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')

        elif choice == 0:
            return

        elif 1 <= int(choice) <= 8:
            parameters[int(choice)-1] = not parameters[int(choice)-1]

        elif choice == 9:

            if os.path.exists(f'{config["projectDir"]}/{prjName}/augmented'):
                shutil.rmtree(f'{config["projectDir"]}/{prjName}/augmented')
            os.makedirs(f'{config["projectDir"]}/{prjName}/augmented')

            aug_key = {k.__class__.__name__: v for v, k in enumerate(chosen_augmenters)}

            with open(f'{config["projectDir"]}/{prjName}/augmented/augmenters.txt', 'w') as aug_file:
                for aug, i in aug_key.items():
                    aug_file.write(f'({i}) : {aug}\n')

            # Create a global variable.
            counter = multiprocessing.Value("i", 0, lock=True)

            printProgressBar(0, permutations * len(images), prefix = 'Augmenting:', suffix = f'({counter.value}/{permutations*len(images)}) Complete', length = 50)

            for i,prmt_list in enumerate(all_permutations):             
                processes =  []
                for j,prmt in enumerate(prmt_list):
                    p = multiprocessing.Process(target=aug_process, args=(j,prmt,i,prjName,images,masks,counter,permutations,aug_key,config["projectDir"]))
                    processes.append(p)
                    p.start()

                for p in processes:
                    p.join()

            input(f'\nContinue...')        

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')