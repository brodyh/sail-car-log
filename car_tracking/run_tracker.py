import glob
import multiprocessing
import os
import shutil
import main as m
import radar_tracker as rt
import AnnotationLib as al

def main():
    create_tracking_files()
    # get_depth()
    # move_files()
    # clean_al_files()

def create_tracking_files():
    # files = glob.glob('/scail/group/deeplearning/driving_data/andriluka/IMAGES/driving_data_q50_data/all_extracted/*.al')
    # files = [f for f in files if f.find('edit') == -1 and f.find('track') == -1]
    
    files = glob.glob('/scail/group/deeplearning/driving_data/andriluka/IMAGES/driving_data_q50_data/all_extracted/4-9-14-concord-split_0_280N_d2_edit-every20-relpath.pal')

    all_args = []
    for f in files:
        all_args.append(('-a %s -o ./ ' % f).split(' '))
    
    pool = multiprocessing.Pool(processes=9)
    for i, result in enumerate( pool.imap_unordered(m.main, all_args) ):
        print "done %0.1f%%" % (float(i+1) * 100 / len(all_args))
    pool.close()
    pool.join()
    
    # remove partials
    partials = glob.glob('*partial.pal')
    for p in partials:
        os.remove(p)
        
    # change paths
    for f in files:
        tracked_file = os.path.basename(f).replace('.pal','-track.pal')
        imgs = al.parse(tracked_file)
        for img in imgs:
            img.imageName = os.path.basename(img.imageName)
        al.save(tracked_file, imgs)

    for f in files:
        tracked_file = f.replace('.pal','-track.pal')
        shutil.move(os.path.basename(tracked_file), tracked_file)
        
def get_depth():
    files = glob.glob('*-track.al')
    files = [f for f in files if f.find('edit') == -1]
    
    pool = multiprocessing.Pool(processes=9)
    for i, result in enumerate( pool.imap_unordered(rt.main, files) ):
        print "done %0.1f%%" % (float(i+1) * 100 / len(files))
    pool.close()
    pool.join()


def move_files():
    files = glob.glob('*with-depth.al')
    for f in files:
        shutil.move(f, '/scail/group/deeplearning/driving_data/andriluka/IMAGES/driving_data_q50_data/all_extracted/' + \
                        os.path.basename(f))

def clean_al_files():
    files = glob.glob('./*.al')
    for f in files:
        os.remove(f)


if __name__=='__main__':
    main()

