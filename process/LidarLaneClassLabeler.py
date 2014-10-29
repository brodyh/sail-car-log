import numpy as np
import glob
import sys
from ArgParser import parse_args
from GPSTransforms import IMUTransforms
from LidarTransforms import utc_from_gps_log_all
from GPSReader import GPSReader
from scipy.spatial import cKDTree
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from LaneMarkingHelper import get_transforms, DataTree

class LaneClassifier(object):
    def __init__(self, args, multilane_npz):
        self.args = args

        lanes_npz = np.load(multilane_npz)
        self.num_lanes = lanes_npz['num_lanes']

        self.lanes = [None for x in range(self.num_lanes)]

        for i in xrange(self.num_lanes):
            self.lanes[i] = DataTree(lanes_npz['lane' + str(i)])

        self.imu, _, _ = get_transforms(args)
        self.pos = self.imu[:, :3, 3]
        self.nearest_pts = np.zeros((self.pos.shape, 2))

    def classifyNearbyLanes(self, pos_idx):
        # # Remove points that are outside the lanes
        xform = self.imu[pos_idx]
        inv_xform = np.linalg.inv(xform)

        pt_left = None
        pt_right = None

        for lane_num in xrange(self.num_lanes):
            _, idx = self.lanes[lane_num].tree.query(self.pos[pos_idx], k=1)
            hom_pt = np.hstack((self.lanes[lane_num].pts[idx, :], 1))
            closest_pt_wrt_car = np.dot(hom_pt, inv_xform.T)
            norm = np.linalg.norm(closest_pt_wrt_car)

            if closest_pt_wrt_car[1] >= 0:
                if pt_left == None or norm < pt_left[0]:
                    pt_left = (norm, idx, lane_num)
            if closest_pt_wrt_car[1] < 0:
                if pt_right == None or norm < pt_right[0]:
                    pt_right = (norm, idx, lane_num)

        nearest_pts = np.array((self.lanes[pt_left[-1]].pts[pt_left[1]],
                               (self.lanes[pt_right[-1]].pts[pt_right[1]])))

        # print pos_idx
        # print nearest_pts


if __name__ == '__main__':
    args = parse_args(sys.argv[1], sys.argv[2])
    lanes_file = glob.glob(sys.argv[1] + '/*done.npz')[0]
    lc = LaneClassifier(args, lanes_file)

    for i in xrange(0, lc.pos.shape[0], 10):
        if i % 1000 == 0:
            print '%d/%d' % (i, lc.pos.shape[0])
        lc.classifyNearbyLanes(i)
