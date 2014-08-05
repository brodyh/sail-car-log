#usage
# python LidarReprojectCalibrate.py <dir-to-data> <basename> <start frame> 

from Q50_config import *
import sys, os
from GPSReader import *
from GPSTransforms import *
from VideoReader import *
from LidarTransforms import *
from ColorMap import *
from transformations import euler_matrix
import numpy as np
import cv2
import time
from ArgParser import *
import SocketServer
import random
import string
from scipy.spatial import cKDTree
from scipy.interpolate import UnivariateSpline
global rx, ry, rz, crx, crz, R, cR, paramInit


def ParametersToString(rx,ry,rz,crx,cry,crz):
    return "%f,%f,%f,%f,%f,%f\n" % (rx,ry,rz,crx,cry,crz)

        

def zDistances(self, distances, global_frame, starting_point, meters_per_point, points_fwd):
    output = []
    point_num = 1
    dist = 0
    for pt in xrange(points_fwd):
      dist = pt * meters_per_point+starting_point
      output.append((np.abs(distances-dist)).argmin()+global_frame)


def lanePos(map_pos, imu_transforms_t, cam, T_from_i_to_l):
    # load nearby map frames
    pts_wrt_imu_0 = array(map_pos).transpose()
    pts_wrt_imu_0 = np.vstack((pts_wrt_imu_0, np.ones((1,pts_wrt_imu_0.shape[1]))))
    # transform points from imu_0 to imu_t
    pts_wrt_imu_t = np.dot( np.linalg.inv(imu_transforms_t), pts_wrt_imu_0)
    # transform points from imu_t to lidar_t
    pts_wrt_lidar_t = np.dot(T_from_i_to_l, pts_wrt_imu_t);
    # transform points from lidar_t to camera_t
    pts_wrt_camera_t = pts_wrt_lidar_t.transpose()[:, 0:3] + cam['displacement_from_l_to_c_in_lidar_frame']
    pts_wrt_camera_t = np.dot(cR, np.dot(R_to_c_from_l_old(0),
            pts_wrt_camera_t.transpose()))    
    pts_wrt_camera_t = np.vstack((pts_wrt_camera_t,
        np.ones((1,pts_wrt_camera_t.shape[1]))))
    pts_wrt_camera_t = dot(cam['E'], pts_wrt_camera_t)
    pts_wrt_camera_t = pts_wrt_camera_t[0:3,:]
    return pts_wrt_camera_t

def cloudToPixels(cam, pts_wrt_cam): 

    width = 4
    if pts_wrt_cam is None or pts_wrt_cam.shape[-1]==0:
      return (None, None)
    (pix, J)  = cv2.projectPoints(pts_wrt_cam.transpose(), np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0]), cam['KK'], cam['distort'])
    pix = pix.transpose()
    pix = np.around(pix[:, 0, :])
    pix = pix.astype(np.int32)
    mask = np.logical_and(True, pix[0,:] > 0 + width/2)
    mask = np.logical_and(mask, pix[1,:] > 0 + width/2)
    mask = np.logical_and(mask, pix[0,:] < 1279 - width/2)
    mask = np.logical_and(mask, pix[1,:] < 959 - width/2)
    #mask = np.logical_and(mask, pix[1,:] < 1039 - width/2)
    #mask = np.logical_and(mask, pix[0,:] < 2079 - width/2)
    mask = np.logical_and(mask, pts_wrt_cam[2,:] > 0)
    dist_sqr = np.sum( pts_wrt_cam[0:3, :] ** 2, axis = 0)
    mask = np.logical_and(mask, dist_sqr > 3)

    return (pix, mask)

def lidarPtsToPixels(pts_wrt_imu_0, imu_transforms_t, T_from_i_to_l, cam):
    # Transform points back to imu_t
    pts_wrt_imu_t = np.dot(np.linalg.inv(imu_transforms_t), pts_wrt_imu_0)
    #pts_wrt_imu_t = pts_wrt_imu_0

    # transform points from imu_t to lidar_t
    pts_wrt_lidar_t = np.dot(T_from_i_to_l, pts_wrt_imu_t)

    # transform points from lidar_t to camera_t
    pts_wrt_camera_t = pts_wrt_lidar_t.transpose()[:, 0:3] + cam['displacement_from_l_to_c_in_lidar_frame']
    pts_wrt_camera_t = np.dot(cR, np.dot(R_to_c_from_l_old(0), 
            pts_wrt_camera_t.transpose()))

    pts_wrt_camera_t = np.vstack((pts_wrt_camera_t,
        np.ones((1, pts_wrt_camera_t.shape[1]))))
    pts_wrt_camera_t = dot(cam['E'], pts_wrt_camera_t)
    pts_wrt_camera_t = pts_wrt_camera_t[0:3,:]

    # reproject camera_t points in camera frame
    (pix, mask) = cloudToPixels(cam, pts_wrt_camera_t)

    return (pix, mask)

def lidarPtsToPixels_old(pts_wrt_lidar_t, imu_transforms_t, cam):
    # transform points from lidar_t to camera_t
    pts_wrt_camera_t = pts_wrt_lidar_t.transpose()[:, 0:3] + cam['displacement_from_l_to_c_in_lidar_frame']
    pts_wrt_camera_t = np.dot(cR, np.dot(R_to_c_from_l_old(0), 
            pts_wrt_camera_t.transpose()))

    pts_wrt_camera_t = np.vstack((pts_wrt_camera_t,
        np.ones((1,pts_wrt_camera_t.shape[1]))))
    pts_wrt_camera_t = dot(cam['E'], pts_wrt_camera_t)
    pts_wrt_camera_t = pts_wrt_camera_t[0:3,:]

    # reproject camera_t points in camera frame
    (pix, mask) = cloudToPixels(cam, pts_wrt_camera_t)

    return (pix, mask)

if __name__ == '__main__':
    # costumized at each frame rotations to make reprejection better
    rx = []
    ry = []
    rz = []
    # frames at which manual adjustments are made
    mframes = []
    # current status of rotation
    crx=0.042000
    cry=0.022000
    crz=0.015000
    cR = euler_matrix(crx, cry, crz)[0:3,0:3]
    # stardard arg parsing
    args = parse_args(sys.argv[1], sys.argv[2])
    cam_num = int(sys.argv[2][-5])
    video_file = args['video']
    video_reader = VideoReader(video_file)
    params = args['params'] 
    cam = params['cam'][cam_num-1]
    #gps_reader = GPSReader(args['gps_mark2'])
    gps_filename= args['gps']
    gps_reader = GPSReader(gps_filename)
    prefix = gps_filename[0:-8]
    gps_data = gps_reader.getNumericData()
    lidar_loader = LDRLoader(args['frames'])
    imu_transforms = IMUTransforms(gps_data)
    gps_times = utc_from_gps_log_all(gps_data)
    
    lane_filename = string.replace(prefix+'_multilane_points_done.npz', 'q50_data', '640x480_Q50')
    lanes = np.load(lane_filename)

    T_from_l_to_i = params['lidar']['T_from_l_to_i']
    T_from_i_to_l = np.linalg.inv(T_from_l_to_i)
    fwd_range=100
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(128,128,255),(128,255,128),(255,128,128),(128,128,0),(128,0,128),(0,128,128),(0,128,255),(0,255,128),(128,0,255),(128,255,0),(255,0,128),(255,128,0)]
    counter = 0 
    frame_step=int(sys.argv[3])
    bg_filename = string.replace(prefix+'2_bg.npz', 'q50_data', '640x480_Q50')
    savename = string.replace(prefix+'_camRot', 'q50_data', '640x480_Q50')
    success = True
    playing=False
    frames_per_second=50
    seconds_ahead=5
    frames_ahead=frames_per_second*seconds_ahead
    num_frames = imu_transforms.shape[0]
    while success and counter+frames_ahead<=num_frames:
      video_reader.setFrame(counter)
      (success, orig) = video_reader.getNextFrame()
      if not success:
        continue
      I = orig.copy()
      fnum = video_reader.framenum
      t = gps_times[fnum]
      '''
      data, data_times = lidar_loader.loadLDRWindow(t-50000, 0.1)
      bg_data = np.load(bg_filename)['data']
      tree = cKDTree(bg_data[:,:3])
      nearby_idx = np.array(tree.query_ball_point(imu_transforms[fnum,0:3,3], r=100.0))
      #print bg_data
      #print imu_transforms[fnum,0:3,3]
      #print nearby_idx
      bg_pts=bg_data[nearby_idx,:3].transpose()
      bg_pts = np.vstack((bg_pts, np.ones((1, bg_pts.shape[1]))))
      
      # Transform data into IMU frame at time t
      pts = data[:, 0:3].transpose()
      pts = np.vstack((pts, np.ones((1, pts.shape[1]))))
      pts = np.dot(T_from_l_to_i, pts)

      # Shift points according to timestamps instead of using transform of full sweep
      #transform_points_by_times(pts, t_data, imu_transforms_mark1, gps_times_mark1)
      transform_points_by_times(pts, data_times, imu_transforms, gps_times)
      (pix, mask) = lidarPtsToPixels(bg_pts, imu_transforms[fnum,:,:], T_from_i_to_l,cam); 
      #(pix, mask) = lidarPtsToPixels(pts, imu_transforms[fnum,:,:], T_from_i_to_l,cam); 
      #intensity = data[mask, 3]
      #heat_colors = heatColorMapFast(intensity, 0, 100)
      if pix is not None:
        for p in range(4):
          I[pix[1,mask]+p, pix[0,mask], :] = [255,255,255]#heat_colors[0,:,:]
          I[pix[1,mask], pix[0,mask]+p, :] = [255,255,255]#heat_colors[0,:,:]
          I[pix[1,mask]+p, pix[0,mask], :] = [255,255,255]#heat_colors[0,:,:]
          I[pix[1,mask], pix[0,mask]+p, :] = [255,255,255]#heat_colors[0,:,:]
      '''
      # now draw interpolated lanes
      ids = range(fnum, fnum+frames_ahead)
      for l in range(lanes['num_lanes']):
        lane_key = 'lane'+str(l)
        lane = lanes[lane_key]
        # find the appropriate portion on the lane (close to the position of car, in front of camera, etc)
        # find the closest point on the lane to the two end-points on the trajectory of car. ideally this should be done before-hand to increase efficiency.
        dist_near = np.sum((lane-imu_transforms[ids[0],0:3,3])**2, axis=1) # find distances of lane to current 'near' position.
        dist_far = np.sum((lane-imu_transforms[ids[-1],0:3,3])**2, axis=1) # find distances of lane to current 'far' position.
        dist_mask = np.where(dist_near<=(fwd_range**2))[0]# only consider points to be valid within fwd_range from the 'near' position
        if len(dist_mask)==0:
          continue
        nearid = np.argmin(dist_near[dist_mask]) # for those valid points, find the one closet to 'near' position.
        farid = np.argmin(dist_far[dist_mask]) #and far position
        lids = range(dist_mask[nearid], dist_mask[farid]+1) # convert back to global id and make it into a consecutive list. 
        #lane3d = lanePos(lane[lids,:], imu_transforms[fnum,:,:], cam,T_from_i_to_l) # lane markings in current camera frame
        #if np.all(lane3d[2,:]<=0):
        #  continue
        #lane3d = lane3d[:,lane3d[2,:]>0] # make sure in front of camera
        #(pix, mask) = cloudToPixels(cam, lane3d)
        pts = lane[lids, :].transpose()
        pts = np.vstack((pts, np.ones((1, pts.shape[1]))))
        (pix, mask) = lidarPtsToPixels(pts, imu_transforms[fnum,:,:], T_from_i_to_l,cam);
        if pix is not None:
          for p in range(4):
            I[pix[1,mask]+p, pix[0,mask], :] = colors[(l)%18]
            I[pix[1,mask], pix[0,mask]+p, :] = colors[(l)%18]
            I[pix[1,mask]+p, pix[0,mask], :] = colors[(l)%18]
            I[pix[1,mask], pix[0,mask]+p, :] = colors[(l)%18]
      if playing:
        cv2.putText(I, 'playing frame '+ str(fnum)+', press P to pause', (360,50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0,255,0),thickness=2)
      else:
        cv2.putText(I, 'paused  frame '+ str(fnum)+', press P to play', (360,50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0,0,255),thickness=2)
      #I=cv2.resize(I, (640, 480))
      cv2.imshow('vid', I)
      key = cv2.waitKey(2)
      if key == -1:
        counter+=frame_step*int(playing)
        continue
      key = chr(key & 255)
      if key == 'd':
        cry += 0.001
      elif key == 'a':
        cry -= 0.001
      elif key == 'w':
        crx += 0.001
      elif key == 's':
        crx -= 0.001
      elif key == '=':
        crz += 0.002
      elif key == '-':
        crz -= 0.002
      elif key == 'p' or key == 'P':
        playing = not playing
        if playing:
          rx.append(crx)
          ry.append(cry)
          rz.append(crz)
          mframes.append(fnum)
      else:
        counter+=frame_step*int(playing)
        continue
    
      #print (crx, cry, crz)
      cR = euler_matrix(crx, cry, crz)[0:3,0:3]
      counter+=frame_step*int(playing)
    # interpolate to get full sequence of customized rotations
    print 'Manual Correction Done! Interpolating...'
    rx = np.array(rx)
    ry = np.array(ry)
    rz = np.array(rz)
    mframes=np.array(mframes)
    polynomial_fit=1
    smoothing = 3
    spline_rx = UnivariateSpline(mframes, rx, k=polynomial_fit, s=smoothing)
    spline_ry = UnivariateSpline(mframes, ry, k=polynomial_fit, s=smoothing)
    spline_rz = UnivariateSpline(mframes, rz, k=polynomial_fit, s=smoothing)
    rx=spline_rx(np.arange(0,num_frames))
    ry=spline_ry(np.arange(0,num_frames))
    rz=spline_rz(np.arange(0,num_frames))
    print 'Filling rotations...'
    R = np.zeros([num_frames,3,3])
    for i in range(num_frames):
      R[i,:,:]=euler_matrix(rx[i], ry[i], rz[i])[0:3,0:3]
    print 'Saving to '+ savename
    np.save(savename, R)
