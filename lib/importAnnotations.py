import os, shutil

# Create image masks from the project object
def importAnnotations(prj):
    if not os.path.isdir('projects/' + prj.name + '/annotations'):
        os.makedirs('projects/' + prj.name + '/annotations')

    maskFiles = sorted(os.listdir(prj.projectDir + '/annotations'))
    
    for mask in maskFiles:
        shutil.copy(prj.projectDir + '/annotations/' + mask, 'projects/' + prj.name + '/annotations')