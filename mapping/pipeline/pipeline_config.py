import os
from os.path import dirname, join as pjoin
import multiprocessing

MAPPING_PATH = dirname(dirname(os.path.abspath(__file__)))
SAIL_CAR_LOG_PATH = dirname(MAPPING_PATH)

NUM_CPUS = multiprocessing.cpu_count() - 1

DATA_DIR = '/media/sdb'

DSET = '17N_b2'
#DSET = '280N_b2'
#DSET = 'sandhill_b2'
DSET_DIR = pjoin(DATA_DIR, DSET)
if not os.path.exists(DSET_DIR):
    os.mkdir(DSET_DIR)
DSET_AVI = DSET + '.avi'
CAM_NUM = int(DSET[-1])

# Stuff to scp over
REMOTE_DATA_DIR = 'robo:/scail/group/deeplearning/driving_data/q50_data/4-2-14-monterey'
#REMOTE_DATA_DIR = 'robo:/scail/group/deeplearning/driving_data/sameep/3-30-14-rosdatatest'
REMOTE_FILES = [
    'split_\\*_%s.avi' % DSET,
    #'%s_gps.out' % DSET[:-1],
    #'%s_frames' % DSET[:-1],
    #'%s.map' % DSET[:-1],
    '%s_*.bag' % DSET[:-1],
    '%s.pcap' % DSET[:-1],
    #'params.ini'
]

# Cluster management
CLUSTER_HOSTS = ['gorgon39']
CLUSTER_DATA_DIR = '/scr/scl'
CLUSTER_DSET_DIR = '%s/%s' % (CLUSTER_DATA_DIR, DSET)
FABRIC_PASS_FILE = '%s/pipeline/pass.txt' % MAPPING_PATH

PARAMS_TO_LOAD = 'q50_4_3_14_params'
PARAMS_FILE = pjoin(DSET_DIR, 'params.ini')
GPS_FILE = pjoin(DSET_DIR, '%s_gps.out' % DSET[:-1])
MAP_FILE = pjoin(DSET_DIR, '%s.map' % DSET[:-1])

PARAMS_H5_FILE = pjoin(DSET_DIR, 'params.h5')
LDR_DIR = pjoin(DSET_DIR, '%s_frames' % DSET[:-1])
POINTS_H5_DIR = pjoin(DSET_DIR, 'h5')
PCD_DIR = pjoin(DSET_DIR, 'pcd')
PCD_DOWNSAMPLED_DIR = pjoin(DSET_DIR, 'pcd_downsampled')
PCD_DOWNSAMPLED_NORMALS_DIR = pjoin(DSET_DIR, 'pcd_downsampled_normals')
ICP_TRANSFORMS_DIR = pjoin(DSET_DIR, 'icp_transforms')
COLOR_DIR = pjoin(DSET_DIR, 'color')
COLOR_CLOUDS_DIR = pjoin(DSET_DIR, 'color_clouds')
FILTERED_CLOUDS_DIR = pjoin(DSET_DIR, 'filtered_clouds')
MERGED_CLOUDS_DIR = pjoin(DSET_DIR, 'merged_clouds')
OCTOMAP_DIR = pjoin(DSET_DIR, 'octomaps')
COLOR_OCTOMAP_DIR = pjoin(DSET_DIR, 'color_octomaps')

EXPORT_FULL = False
LANE_FILTER = False
EXPORT_START = 1000
EXPORT_NUM = 400
EXPORT_STEP = 5

DOWNSAMPLE_LEAF_SIZE = 0.1
K_NORM_EST = 30

ICP_ITERS = 20
# NOTE set this parameter based on GPS delta spikes,
# downsampling voxel leaf size, and time steps between scans
ICP_MAX_DIST = 5.0

LIDAR_PROJECT_MIN_DIST = 3.0

CLOUD_MAX_STORE = 400
MAP_COLOR_WINDOW = 15

HANDLE_OCCLUSIONS = True
OCTOMAP_RES = 0.5
COLOR_OCTOMAP_RES = 0.5
PROB_HIT = 0.7
PROB_MISS = 0.4
OCCUPANCY_THRES = 0.5
CLAMPING_THRES_MAX = 0.97
CLAMPING_THRES_MIN = 0.12
RAYCAST_TOL = 3.0
CAST_ONCE = True
CAST_OCTOMAP_SINGLE = True

OCC_EXT = '_occ' if HANDLE_OCCLUSIONS else ''
OCTOMAP_FILE = '{0}/octomap_{1:.2f}{2}.ot'.format(OCTOMAP_DIR, OCTOMAP_RES, OCC_EXT)
CENTERED_OCTOMAP_FILE = os.path.splitext(OCTOMAP_FILE)[0] + '_centered.ot'
COLOR_OCTOMAP_FILE = '{0}/octomap_{1:.2f}{2}.ot'.format(COLOR_OCTOMAP_DIR, COLOR_OCTOMAP_RES, OCC_EXT)
CENTERED_COLOR_OCTOMAP_FILE = '{0}/octomap_{1:.2f}_{2}_centered.bt'.format(COLOR_OCTOMAP_DIR, COLOR_OCTOMAP_RES, OCC_EXT)
COLOR_OCTOMAP_BT = os.path.splitext(COLOR_OCTOMAP_FILE)[0] + '.bt'
COLOR_OCTOMAP_MESH = ''

OCTOMAP_H5_FILE = os.path.splitext(OCTOMAP_FILE)[0] + '.h5'
COLOR_OCTOMAP_H5_FILE = os.path.splitext(COLOR_OCTOMAP_FILE)[0] + '.h5'

OCTOMAP_SINGLE_FILES = list()
for k in range(EXPORT_NUM):
    OCTOMAP_SINGLE_FILES.append(os.path.splitext(OCTOMAP_FILE)[0] + '_%d.ot' % k)

MERGED_CLOUD_FILE = pjoin(MERGED_CLOUDS_DIR, 'merged_%d.pcd' % MAP_COLOR_WINDOW)
MERGED_VTK_FILE = os.path.splitext(MERGED_CLOUD_FILE)[0] + '.vtk'

STATIC_CLOUD_FILE = pjoin(MERGED_CLOUDS_DIR, 'static_%d.pcd' % MAP_COLOR_WINDOW)
STATIC_VTK_FILE = os.path.splitext(STATIC_CLOUD_FILE)[0] + '.vtk'
DYNAMIC_CLOUD_FILE = pjoin(MERGED_CLOUDS_DIR, 'dynamic_%d.pcd' % MAP_COLOR_WINDOW)
DYNAMIC_VTK_FILE = os.path.splitext(DYNAMIC_CLOUD_FILE)[0] + '.vtk'

'''
Print out variable values
'''

if __name__ == '__main__':
    local_vars = locals().copy()
    for k in local_vars:
        if not k.startswith('_') and '<module' not in str(local_vars[k]) and\
                '<function' not in str(local_vars[k]):
            print '{0}: {1}'.format(k, local_vars[k])