from Q50_config import *
import sys, os
from GPSReader import *
from GPSReprojection import *
from GPSTransforms import *
from VideoReader import *
from LidarTransforms import *
from ColorMap import *
from transformations import euler_matrix
import numpy as np
import cv2
from ArgParser import *

WINDOW = 50*5

def cloudToPixels(cam, pts_wrt_cam): 

    width = 4
    (pix, J)  = cv2.projectPoints(pts_wrt_cam.transpose(), np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0]), cam['KK'], cam['distort'])

    pix = pix.transpose()
    pix = np.around(pix[:, 0, :])
    pix = pix.astype(np.int32)
    mask = np.logical_and(True, pix[0,:] > 0 + width/2)
    mask = np.logical_and(mask, pix[1,:] > 0 + width/2)
    mask = np.logical_and(mask, pix[0,:] < 1279 - width/2)
    mask = np.logical_and(mask, pix[1,:] < 959 - width/2)
    mask = np.logical_and(mask, pts_wrt_cam[2,:] > 0)
    dist_sqr = np.sum( pts_wrt_cam[0:3, :] ** 2, axis = 0)
    mask = np.logical_and(mask, dist_sqr > 3)

    return (pix, mask)

def localMapToPixels(map_data, imu_transforms_t, T_from_i_to_l, cam):
    # load nearby map frames
    pts_wrt_imu_0 = array(map_data[:,0:3]).transpose()
    pts_wrt_imu_0 = np.vstack((pts_wrt_imu_0, 
        np.ones((1,pts_wrt_imu_0.shape[1]))))
    # transform points from imu_0 to imu_t
    pts_wrt_imu_t = np.dot( np.linalg.inv(imu_transforms_t), pts_wrt_imu_0)
    # transform points from imu_t to lidar_t
    pts_wrt_lidar_t = np.dot(T_from_i_to_l, pts_wrt_imu_t);
    # transform points from lidar_t to camera_t
    pts_wrt_camera_t = pts_wrt_lidar_t.transpose()[:, 0:3] + cam['displacement_from_l_to_c_in_lidar_frame']
    pts_wrt_camera_t = dot(R_to_c_from_l(cam), 
            pts_wrt_camera_t.transpose())
    # reproject camera_t points in camera frame
    (pix, mask) = cloudToPixels(cam, pts_wrt_camera_t)

    return (pix, mask)


def trackbarOnchange(t, prev_t):
    if abs(t - prev_t) > 1:
        video_reader.setFrame(t)


if __name__ == '__main__':
    args = parse_args(sys.argv[1], sys.argv[2])
    cam_num = int(sys.argv[2][-5])
    video_file = args['video']

    params = LoadParameters('q50_4_3_14_params')
    cam = params['cam'][cam_num-1]
    video_reader = VideoReader(video_file)
    gps_reader = GPSReader(args['gps'])
    GPSData = gps_reader.getNumericData()
    imu_transforms = IMUTransforms(GPSData)

    imu_transforms_smoothed = np.load('imu_transforms_smoothed.npz')['data']
    print imu_transforms.shape
    print imu_transforms_smoothed.shape
    print np.max(np.max(np.abs(imu_transforms - imu_transforms_smoothed)))

    '''
    import matplotlib.pyplot as plt
    plt.figure()
    zs = list()
    zs_smoothed = list()
    for k in range(imu_transforms.shape[0]):
        zs.append(imu_transforms[k, 2, 3])
        zs_smoothed.append(imu_transforms_smoothed[k, 2, 3])
    plt.plot(range(len(zs)), zs, 'r-')
    plt.plot(range(len(zs)), zs_smoothed, 'g-')
    plt.show()
    stop
    '''

    
    T_from_i_to_l = np.linalg.inv(params['lidar']['T_from_l_to_i'])

    all_data = np.load(sys.argv[3])
    map_data = all_data['data']
    print map_data.shape

    all_data_smoothed = np.load(sys.argv[4])
    map_data_smoothed = all_data_smoothed['data']
    print map_data_smoothed.shape

    print np.max(np.max(np.abs(map_data - map_data_smoothed)))

    #map_data = map_data[map_data[:,3] > 60, :]
    # map points are defined w.r.t the IMU position at time 0
    # each entry in map_data is (x,y,z,intensity,framenum). 

    print "Hit 'q' to quit"
    trackbarInit = False

    # bgr
    red = [0, 0, 255]
    green = [0, 255, 0]

    while True:
        for count in range(2):
            (success, I) = video_reader.getNextFrame()

        if not success:
            break

        t = video_reader.framenum - 1
        print t

        mask_window = (map_data[:,4] < t + WINDOW) & (map_data[:,4] > t );
        map_data_copy = array(map_data[mask_window, :]);

        mask_window = (map_data_smoothed[:,4] < t + WINDOW) & (map_data_smoothed[:,4] > t );
        map_data_smoothed_copy = array(map_data_smoothed[mask_window, :]);

        # reproject
        (pix, mask) = localMapToPixels(map_data_copy, imu_transforms[t,:,:], T_from_i_to_l, cam)
        (pix_smoothed, mask_smoothed) = localMapToPixels(map_data_smoothed_copy, imu_transforms_smoothed[t,:,:], T_from_i_to_l, cam)

        # draw 
        intensity = map_data_copy[mask, 3]
        intensity_smoothed = map_data_smoothed_copy[mask_smoothed, 3]
        #heat_colors = heatColorMapFast(np.zeros(intensity.shape), 0, 100)
        heat_colors = np.tile(red, (intensity.shape[0], 1))
        #heat_colors_smoothed = heatColorMapFast(np.ones(intensity_smoothed.shape), 0, 100)
        heat_colors_smoothed = np.tile(green, (intensity_smoothed.shape[0], 1))
        for p in range(2):
            I[pix[1,mask]+p, pix[0,mask], :] = heat_colors
            I[pix[1,mask], pix[0,mask]+p, :] = heat_colors
            I[pix[1,mask]+p, pix[0,mask], :] = heat_colors
            I[pix[1,mask], pix[0,mask]+p, :] = heat_colors

            I[pix_smoothed[1,mask_smoothed]+p, pix_smoothed[0,mask_smoothed], :] = heat_colors_smoothed
            I[pix_smoothed[1,mask_smoothed],   pix_smoothed[0,mask_smoothed]+p, :] = heat_colors_smoothed
            I[pix_smoothed[1,mask_smoothed]+p, pix_smoothed[0,mask_smoothed], :] = heat_colors_smoothed
            I[pix_smoothed[1,mask_smoothed],   pix_smoothed[0,mask_smoothed]+p, :] = heat_colors_smoothed

        cv2.imshow(video_file, cv2.pyrDown(I))
        if not trackbarInit:
            cv2.createTrackbar('trackbar', video_file, 0, int(video_reader.total_frame_count), lambda x: trackbarOnchange(x, t))
            trackbarInit = True
        else:
            cv2.setTrackbarPos('trackbar', video_file, t)

        keycode = cv2.waitKey(1)
        if keycode == 113:
            break

    print 'Played %d frames' % t
