# usage: 
# python LidarIntegrator.py <dir> <basename><camnum>.avi <export name>.npz <optional additional flags such as --export or --full>

# to change the type of data exported, see the function integrateClouds 


from Q50_config import *
from ArgParser import *
import sys, os
from GPSReader import *
from GPSTransforms import *
from VideoReader import *
from LidarTransforms import *
from VtkRenderer import *
from transformations import euler_matrix, quaternion_matrix, quaternion_from_matrix, quaternion_slerp
import numpy as np
from ColorMap import *
import vtk
import copy
import cv2
import math


global actors
global clouds 
global all_data
global cloud_r
global renderWindow
global rx
global ry
global rz
global R
global start_fn
global num_fn
global color_mode

actors =  []
clouds = [ ]
all_data = [ ] 
cloud_r = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()

#(rx,ry,rz) = (-0.1)
#R_from_i_to_l = euler_matrix(rx,ry,rz)[0:3,0:3]

# settings for 280N_e 
#start_fn = 1200 
#num_fn = 1000 
#step = 1

# settings for vail 
#start_fn = 0
#num_fn = 300
#step = 5

# settings for parking
#start_fn = 0
#num_fn = 200
#step = 2

start_fn = 0 # offset in frame numbers to start exporting data
num_fn = 60 # number of frames to export. this is changed if --full is enabled
step = 5 # step between frames

color_mode = 'INTENSITY'

def exportData():
        print 'exporting data'
        export_data = np.row_stack(all_data)
        print export_data
        print export_data.shape
        np.savez(sys.argv[3], data=export_data)
        print 'export complete'

def cloudToPixels(cam, pts_wrt_cam): 

    width = 4
    pix = np.around(np.dot(cam['KK'], np.divide(pts_wrt_cam[0:3,:], pts_wrt_cam[2, :])))
    pix = pix.astype(np.int32)
    mask = np.logical_and(True, pix[0,:] > 0 + width/2)
    mask = np.logical_and(mask, pix[1,:] > 0 + width/2)
    mask = np.logical_and(mask, pix[0,:] < 1279 - width/2)
    mask = np.logical_and(mask, pix[1,:] < 959 - width/2)
    mask = np.logical_and(mask, pts_wrt_cam[2,:] > 0)
    dist_sqr = np.sum( pts_wrt_cam[0:3, :] ** 2, axis = 0)
    mask = np.logical_and(mask, dist_sqr > 3)

    return (pix, mask)

def stepVideo(video_reader, step):
    if step == 1: 
        return None
    for t in range(step-1):
        (success, I) = video_reader.getNextFrame()
    return success


def interp_transforms(T1, T2, alpha):
    assert alpha <= 1
    T_avg = alpha * T1 + (1 - alpha) * T2
    q1 = quaternion_from_matrix(T1)
    q2 = quaternion_from_matrix(T2)
    q3 = quaternion_slerp(q1, q2, alpha)
    R = quaternion_matrix(q3)
    T_avg[0:3, 0:3] = R[0:3,0:3]
    return T_avg


def interp_transforms_backward(imu_transforms, ind):
    assert ind < 0, 'No need to call interp_transforms_backward'
    T_interp = imu_transforms[0, :, :] -\
        (imu_transforms[-1 * ind, :, :] - imu_transforms[0, :, :])
    R = T_interp[0:3, 0:3]
    R = np.linalg.qr(R, mode='complete')[0]
    T_interp[0:3, 0:3] = R
    return T_interp


def transform_points_in_sweep(pts, times, fnum, imu_transforms):
    for time in set(times):
        mask = times == time

        # FIXME PARAM
        offset = (time / float(1e6)) / 0.05
        offset = min(5, offset)

        ind1 = int(fnum - math.ceil(offset))
        ind2 = int(fnum - math.floor(offset))

        # FIXME Hack to interpolate before 0
        #ind1, ind2 = max(ind1, 0), max(ind2, 0)
        if ind1 < 0:
            T1 = interp_transforms_backward(imu_transforms, ind1)
        else:
            T1 = imu_transforms[ind1, :, :]
        if ind2 < 0:
            T2 = interp_transforms_backward(imu_transforms, ind2)
        else:
            T2 = imu_transforms[ind2, :, :]

        transform = interp_transforms(T1, T2, offset / 5.0)

        # transform data into imu_0 frame
        pts[:, mask] = np.dot(transform, pts[:, mask])


def integrateClouds(ldr_map, IMUTransforms, renderer, offset, num_steps, step, calibrationParameters):
    start = offset
    end = offset + num_steps*step
    
    if color_mode == 'CAMERA':  
        video_reader1.setFrame(start)
        video_reader2.setFrame(start)

    trans_wrt_imu = IMUTransforms[start:end,0:3,3]
    gpsPointCloud = VtkPointCloud(trans_wrt_imu[:,0:3], 0*trans_wrt_imu[:,0])
    clouds.append(gpsPointCloud)
    actors.append(gpsPointCloud.get_vtk_cloud())
    renderer.AddActor(actors[-1])
    for t in range(num_steps):
        fnum = offset+t*step
        print fnum

        
        data = loadLDR(ldr_map[fnum])
        # filter out the roof rack
        dist = np.sqrt(np.sum( data[:, 0:3] ** 2, axis = 1))

        # check out the commented out section below to figure out how this is filtering.
        data_filter_mask = (dist > 3)                 & \
                           (data[:,3] > 30)            
                           #&\
                           #(np.abs(data[:,1]) < 2.2)   & \
                           #(np.abs(data[:,1]) > 1.2)   & \
                           #(data[:,2] < -1.8)          & \
                           #(data[:,2] > -2.5)        
        data = data[data_filter_mask, :]
        """
        # filter out on intensity
        data = data[ data[:,3] > 60 , :]
        # only points ahead of the car
        data = data[ data[:,0] > 0, :]
        # within 2.2 meters laterally of the lidar
        data = data[ np.abs(data[:,1]) < 2.2]

        # farther than 1.2 meters laterally of the lidar
        data = data[ np.abs(data[:,1]) > 1.2]

        # between -2.5 and -1.5 meters below the lidar
        data = data[ data[:,2] < -1.5]
        data = data[ data[:,2] > -2.5]
        """

        if color_mode == 'CAMERA':
        
            (success, I1) = video_reader1.getNextFrame()
            (success, I2) = video_reader2.getNextFrame()
            stepVideo(video_reader1, step)
            stepVideo(video_reader2, step)
            """
            pts_wrt_cam1 = array(data[:, 0:3])
            pts_wrt_cam1[:, 0:3] += cam1['displacement_from_l_to_c_in_lidar_frame'];
            pts_wrt_cam1 = dot(R_to_c_from_l(cam1), pts_wrt_cam1.transpose())
            (pix1, mask1) = cloudToPixels(cam1, pts_wrt_cam1)

        
            colors = 0*pts_wrt_cam1.transpose() + 0
            print I1[pix1[1,mask1], pix1[0,mask1], :].shape
            print colors[mask1, :].shape
        
            # BGR -> RGB
            colors[ mask1, 0] = I1[pix1[1,mask1], pix1[0,mask1], 2] 
            colors[ mask1, 1] = I1[pix1[1,mask1], pix1[0,mask1], 1] 
            colors[ mask1, 2] = I1[pix1[1,mask1], pix1[0,mask1], 0]            """ 

            pts_wrt_cam2 = array(data[:, 0:3])
            pts_wrt_cam2[:, 0:3] += cam2['displacement_from_l_to_c_in_lidar_frame'];
            pts_wrt_cam2 = dot(R_to_c_from_l(cam2), pts_wrt_cam2.transpose())
            (pix2, mask2) = cloudToPixels(cam2, pts_wrt_cam2)

            colors = 0*pts_wrt_cam2.transpose() + 0
            # BGR -> RGB
            colors[ mask2, 0] = I2[pix2[1,mask2], pix2[0,mask2], 2] 
            colors[ mask2, 1] = I2[pix2[1,mask2], pix2[0,mask2], 1] 
            colors[ mask2, 2] = I2[pix2[1,mask2], pix2[0,mask2], 0]              
        
            intensity = data[mask2, 3]
            heat_colors = heatColorMapFast(intensity, 0, 100)
            I2[pix2[1,mask2], pix2[0,mask2], :] = heat_colors[0,:,:]

            #cv2.imshow('vid', I2)
            #cv2.waitKey(5)

        # transform data into IMU frame at time t
        pts = data[:,0:3].transpose()
        pts = np.vstack((pts,np.ones((1,pts.shape[1]))))
        T_from_l_to_i = calibrationParameters['lidar']['T_from_l_to_i']
        pts = np.dot(T_from_l_to_i, pts)

        # Microseconds till end of the sweep
        times = data[:, 5]
        transform_points_in_sweep(pts, times, fnum, imu_transforms)

        ## transform data into imu_0 frame
        #pts = np.dot(IMUTransforms[fnum,:,:], pts);
        pts = pts.transpose()

        # for exporting purposes
        pts_copy = array(pts[:,0:3])
        pts_copy = np.column_stack((pts_copy, array(data[:,3])))
        pts_copy = np.column_stack((pts_copy, fnum*np.ones((pts.shape[0],1))))
        all_data.append(pts_copy)


        if color_mode == 'CAMERA':
            lidarCloud = VtkPointCloud(pts[ mask2 ,0:3], colors[ mask2,:])
            actors.append(lidarCloud.get_vtk_color_cloud())
        elif color_mode == 'INTENSITY': 
            lidarCloud = VtkPointCloud(pts[:,0:3], data[:,3])
            actors.append(lidarCloud.get_vtk_cloud(zMin=0, zMax=255))
        clouds.append(lidarCloud)
        renderer.AddActor(actors[-1])


def keypress(obj, event):
    global actors
    global clouds 
    global cloud_r
    global all_data
    global renderWindow
    global rx
    global ry
    global rz
    global R
    global start_fn
    global color_mode
    key = obj.GetKeySym()
    rerender = True
    if key == 'i':
        ry += 0.0005
    elif key == 'k':
        ry -= 0.0005
    elif key == 'l':
        rx += 0.005
    elif key == 'j':
        rx -= 0.005
    elif key == 'o':
        rz += 0.0005
    elif key == 'u':
        rz -= 0.0005
    elif key == 'c':
        color_mode = 'CAMERA'
    elif key == 'v':
        color_mode = 'INTENSITY'
    elif key == 'x':
        exportData()

    else:
        rerender = False
    if rerender:
        for a in actors:
            cloud_r.RemoveActor(a)
        actors = [ ]
        clouds = [ ]
        all_data = [ ]
        #start_fn = start_fn + 5
        integrateClouds(ldr_map, imu_transforms, cloud_r, start_fn, num_fn, step, params)
        renderWindow.Render()
    print key
    #print (rx,ry,rz)

if __name__ == '__main__': 
    vfname = sys.argv[2]
    vidname = vfname.split('.')[0]
    vidname2 = vidname[:-1] + '2'
    video_filename2 = sys.argv[1] + '/' + vidname2 + '.avi'
    
    args = parse_args(sys.argv[1], sys.argv[2])

    gps_reader = GPSReader(args['gps'])
    params = args['params']
    cam1 = params['cam'][0]
    cam2 = params['cam'][1]
    video_reader1 = VideoReader(args['video'])
    video_reader2 = VideoReader(video_filename2)
    gps_reader = GPSReader(args['gps'])
    GPSData = gps_reader.getNumericData()
    imu_transforms = IMUTransforms(GPSData)
    ldr_map = loadLDRCamMap(args['map'])

    
    if '--full' in sys.argv:
      total_num_frames = GPSData.shape[0]
      start_fn = 0
      step = 10
      num_fn = int(total_num_frames / step)


    # this has been flipped for the q50
    
    cloud_r.SetBackground(0., 0., 0.)
    cloud_r.SetViewport(0,0,1.0,1.0)
    integrateClouds(ldr_map, imu_transforms, cloud_r, start_fn, num_fn, step, params)

    if '--export' in sys.argv:
      exportData()
      sys.exit(0)

    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(cloud_r)
    renderWindow.SetSize(1200, 600)

    axisActor = vtk.vtkAxisActor()
    axisActor.SetGridlineXLength(5)
    axisActor.SetGridlineYLength(5)
    axisActor.SetGridlineZLength(5)
    #axisActor.DrawGridpolysOn()
    #axisActor.DrawInnerGridlinesOn()
    cloud_r.AddActor(axisActor)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    mouseInteractor = vtk.vtkInteractorStyleTrackballCamera()
    renderWindowInteractor.SetInteractorStyle(mouseInteractor)
    renderWindow.Render()

    renderWindowInteractor.AddObserver('KeyPressEvent', keypress)
    #renderWindowInteractor.AddObserver('TimerEvent', keypress)
    #timerId = renderWindowInteractor.CreateRepeatingTimer(1)
    renderWindowInteractor.Start()
