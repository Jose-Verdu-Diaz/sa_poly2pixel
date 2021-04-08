import os, shutil

# Create image masks from the project object
def importImages(prj):
    if not os.path.isdir('projects/' + prj.name + '/img'):
        os.makedirs('projects/' + prj.name + '/img')

    imageFiles = sorted(os.listdir(prj.projectDir + '/img'))

    for img in imageFiles:
        shutil.copy(prj.projectDir + '/img/' + img, 'projects/' + prj.name + '/img')