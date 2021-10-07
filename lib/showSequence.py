import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2, os
from datetime import datetime


def showSequence(prj, dir, classId, interval, save=False):
    ims = []
    for file in sorted(os.listdir(f'{os.getcwd()}/projects/{prj.name}/{dir}')):
        ims.append(cv2.imread(f'{os.getcwd()}/projects/{prj.name}/{dir}/{file}'))

    if not classId == None:
        for i,img in enumerate(ims):
            black_pixels_mask = np.all(img != [classId, classId, classId], axis=-1)
            non_black_pixels_mask = ~black_pixels_mask

            img[black_pixels_mask] = [0, 0, 0]
            img[non_black_pixels_mask] = [255, 255, 255]

    fig = plt.figure()

    sequence = []
    for img in ims:
        im = plt.imshow(img, animated=True)
        im.axes.xaxis.set_visible(False)
        im.axes.yaxis.set_visible(False)
        sequence.append([im])

    ani = animation.ArtistAnimation(fig, sequence, interval=interval, blit=True, repeat_delay=0)

    
    if save:
        timestamp = datetime.timestamp(datetime.now())
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        ani.save(f'{timestamp}.mp4', writer=writer)
    
    plt.show()


