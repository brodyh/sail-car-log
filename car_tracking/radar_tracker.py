import cv
import sys, os
import copy
from AnnotationLib import *
process_dir = '/'.join(os.path.abspath('radar_tracker.py').split('/')[:-2])+'/process/';
sys.path.append(process_dir);
from Q50_config import *
from GPSReader import *
from GPSReprojection import *
from GPSTransforms import *
from VideoReader import *
from RadarTransforms import *
from LidarTransforms import *
from ColorMap import *
from transformations import euler_matrix
import numpy as np
import cv2
from ArgParser import *
from ProjectRadarOnVideo import *

from collections import defaultdict
from collections import Counter

def does_overlap(_rect, annotation): 
   Thr = .7; 
   rect1 = copy.deepcopy(_rect);
   for _rect2 in annotation.rects:
	   rect2 = copy.deepcopy(_rect2); 
	 
	   intersection_rect = rect1.intersection(rect2) 
	   a1 = rect1.width() * rect1.height(); 
	   a2 = rect2.width() * rect2.height(); 
	   a0 = intersection_rect[0] * intersection_rect[1]; 
	   if (a0 * 1.0) / a1 > Thr or (a0 * 1.0) / a2 > Thr: 
		return True; 
 
   return False 

def set_ids(annotations):
	gap_between_the_same_id_usage = 50;
        n = len(annotations)            
        available_id = 0;
	id_last_usage = [];     
        annotation = annotations[0];
        rects = annotation.rects;
        for rect in rects:      
                rect.classID = available_id;
		id_last_usage.append(0);
                available_id += 1;
        for anno_idx in range(1,n):
#		print str(1.0 * anno_idx / n *100).split('.')[0] + "%"
                new_annotation = annotations[anno_idx];
                new_rects = new_annotation.rects;
		if(len(new_rects)==0):
			annotation = new_annotation;
			rects = annotation.rects;
			continue;
		if(len(rects)==0):
			new_ids = [-1 for i in range(len(new_rects))];
		else:	
			dist_mat = [[0 for i in range(len(rects))] for j in range(len(new_rects))]
			# Finding the distance of rects in two consecutive frames
			for i, new_rect in enumerate(new_rects):
				for j, rect in enumerate(rects):
					dist_mat[i][j] = (new_rect.centerX()-rect.centerX())**2 + (new_rect.centerY()-rect.centerY())**2 \
							 + (new_rect.width()-rect.width())**2 + (new_rect.height()-rect.height())**2
#			print new_rects
			min_dist = [min(dist_mat[i]) for i in range(len(new_rects))];
			new_ids = [dist_mat[i].index(min(dist_mat[i])) for i in range(len(new_rects))];
			# Checking for confilicts in the matching
			for i in range(len(new_rects)):
				for j in range(i+1, len(new_rects)):
					if new_ids[i] == new_ids[j]:
						if min_dist[i] < min_dist[j]:
							new_ids[j] = -1;
						else:
							new_ids[i] = -1;
		# Updating the ids of rects in the new frame
                for i in range(len(new_rects)):
                        if new_ids[i] == -1:
				flag = False;
				for j in range(available_id):
					if(anno_idx-id_last_usage[j] > gap_between_the_same_id_usage):
						flag = True;
						break;
				if flag:
					new_rects[i].classID = j;
					id_last_usage[j] = anno_idx;
				else:
                               		new_rects[i].classID = available_id;
					id_last_usage.append(anno_idx);
                                	available_id += 1;
                        else:
                                new_rects[i].classID = rects[new_ids[i]].classID;
				id_last_usage[new_rects[i].classID] = anno_idx;
				
                annotation = new_annotation;
                rects = annotation.rects;
        
        return [available_id,gap_between_the_same_id_usage]; 
    
def set_annotations_ids_using_radar(annotations, rdr_map, args): # rect.classID: corresponding radar id, rect.score: distance
	print "Setting ids ..."
	max_id, block_size = set_ids(annotations);
	print "Importing radar information..."
	anno_len = len(annotations);
	rdr_len = len(rdr_map);
	sc = 10; # scaling factor between tracker and radar indices
	i = 0;
	while (i < anno_len and i < rdr_map):
		id_info = [[] for r in range(max_id)];
		for j in range(block_size):
			idx = i + j;
			frame_num = sc * idx;
			if idx >=len(annotations) or frame_num >= len(rdr_map):
				break;
			annotation = annotations[idx];
			radar_data = loadRDR(rdr_map[frame_num])[0]
	#		print "============" + str(len(radar_data)) + ", " +  str(len(radar_data[0]))
			if radar_data.shape[0] > 0:
			    # Remove points that have a low radar cross-section
			    mask = (radar_data[:, 5] > 0)
			    # Remove points that are moving too fast (fixed objects)
			    mask &= (radar_data[:, 6] > -20)
			    radar_data = radar_data[mask]
			
			ctr_pts = np.array(radar_data);
			if len(ctr_pts)==0:
				continue;
		        center_proj = projectPoints(ctr_pts, args)
		        cn_rdr = center_proj[:, 7:10].astype(np.int32);
			cn_trk = np.array([[rect.classID, int(rect.centerX()), int(rect.bottom())] 
					for rect in annotation.rects if rect.width() > 40]);
			for r in range(len(cn_trk)):
				id_r = cn_rdr[0,0];
				dis = (cn_rdr[0,1]-cn_trk[r,1])**2 + (cn_rdr[0,2]-cn_trk[r,2])**2;
				for s in range(1,len(cn_rdr)):
					dis_new = (cn_rdr[s,1]-cn_trk[r,1])**2 + (cn_rdr[s,2]-cn_trk[r,2])**2;
					if dis_new < dis:
						dis = dis_new;
						id_r = cn_rdr[s,0];
				id_info[cn_trk[r,0]].append([id_r, dis]);
		
		max_ID = [0 for r in range(max_id)];
		for r in range(max_id):
			arr = np.array(id_info[r]);
			if len(arr) > 0:
				result = Counter(arr[:,0]).most_common(1)[0]
				if result[1] > .5 * len(arr):
					max_ID[r] = result[0];
				else:
					max_ID[r] = -1;
		
		# Checking for mismatching (matching two tracker results to one radar result)
		for j in range(block_size):
			idx = i + j;
			frame_num = sc * idx;
			if idx >= len(annotations) or frame_num >= len(rdr_map):
				break;
			annotation = annotations[idx]
			radar_data = loadRDR(rdr_map[frame_num])[0]
			if radar_data.shape[0] > 0:
			    # Remove points that have a low radar cross-section
			    mask = (radar_data[:, 5] > 0)
			    # Remove points that are moving too fast (fixed objects)
			    mask &= (radar_data[:, 6] > -20)
			    radar_data = radar_data[mask]
			
			ctr_pts = np.array(radar_data);
			
			new_ids = [max_ID[rect.classID] for rect in annotation.rects];
			if(len(ctr_pts)>0):
				center_proj = projectPoints(ctr_pts, args)
				cn_rdr = center_proj[:, 7:10].astype(np.int32);
				
				for r in range(len(new_ids)):
					for s in range(r+1,len(new_ids)):
						if new_ids[r] == new_ids[s] and new_ids[r] > 0:
							cn_idx = 0;
							flag = False;
							while(True):
								if cn_rdr[cn_idx][0] == new_ids[r]:
									flag = True;
									break;
								cn_idx += 1;
								if cn_idx > len(cn_rdr)-1:
									break;
							if flag:
							 
								r_pnt = [int(annotation.rects[r].centerX()), int(annotation.rects[r].bottom())]	
								s_pnt = [int(annotation.rects[s].centerX()), int(annotation.rects[s].bottom())]	
								dis_r = (cn_rdr[cn_idx,1]-r_pnt[0])**2 + (cn_rdr[cn_idx,2]-r_pnt[1])**2;
								dis_s = (cn_rdr[cn_idx,1]-s_pnt[0])**2 + (cn_rdr[cn_idx,2]-s_pnt[1])**2;
								if(dis_r < dis_s):
									new_ids[s] = -1;
								else:
									new_ids[r] = -1;
		        for r, rect in enumerate(annotation.rects):
				r_id = new_ids[r];
				rect.score = -1;
				if r_id == -1:
					rect.classID = -abs(rect.classID);
				else:
					rect.classID = r_id;
					if len(ctr_pts)>0 :
						cn_idx = 0;
						flag = False;
						while(True):
							if radar_data[cn_idx][7] == r_id:
								flag = True;
								break;
							cn_idx += 1;
							if cn_idx >= len(radar_data):
								break;
						if flag:
							rect.score = radar_data[cn_idx][0];
		i += block_size;
	return annotations;
def fill_gaps(annotations, rdr_map):
	anno_size = len(annotations);
	rdr_map_size = len(rdr_map);
	ind = 0;
	search_area = 10;
	while(True):
		frame_num = ind * 10;
		if(ind >= anno_size or frame_num >=len(rdr_map)):
			break;
		annotation = annotations[ind];
		radar_data = loadRDR(rdr_map[frame_num])[0];
		if radar_data.shape[0] > 0:
		    # Remove points that have a low radar cross-section
		    mask = (radar_data[:, 5] > 0)
		    # Remove points that are moving too fast (fixed objects)
		    mask &= (radar_data[:, 6] > -20)
		    radar_data = radar_data[mask]
		if radar_data.shape[0] > 0:
			radar_array = np.array(radar_data);
			radar_ids = radar_data[:,7];
			anno_ids = [rect.classID for rect in annotation.rects];
			for r, rId in enumerate(radar_ids):
				if rId not in anno_ids:
					flagb = False;
					flagf = False;
					temp_arr = range(max(0,ind-search_area), ind);
					temp_arr.reverse();
					for jb in temp_arr:
						back_anno = annotations[jb];
						b_ids = [rect.classID for rect in back_anno.rects];
						if rId in b_ids:
							flagb = True;
							break;
					for jf in range(ind, min(anno_size, ind + search_area)):
						forward_anno = annotations[jf];
						f_ids = [rect.classID for rect in forward_anno.rects];
						if rId in f_ids:
							flagf = True;
							break;
					if flagb and flagf:
						back_rects = back_anno.rects;
						forward_rects = forward_anno.rects;
						for rect in back_rects:
							if rect.classID == rId:
								brect = rect;
								break;
							
						for rect in forward_rects:
							if rect.classID == rId:
								frect = rect;
								break;
						ratio = (1.0*(ind-jb))/(jf-jb);
						b_x1 = brect.x1; f_x1 = frect.x1;
						b_x2 = brect.x2; f_x2 = frect.x2;
						b_y1 = brect.y1; f_y1 = frect.y1;
						b_y2 = brect.y2; f_y2 = frect.y2;
						n_x1 = b_x1*(1-ratio) + f_x1*ratio;
						n_x2 = b_x2*(1-ratio) + f_x2*ratio;
						n_y1 = b_y1*(1-ratio) + f_y1*ratio;
						n_y2 = b_y2*(1-ratio) + f_y2*ratio;
						
						new_rect = AnnoRect(int(n_x1), int(n_y1), int(n_x2), int(n_y2));
						new_rect.classID = int(rId);
						new_rect.score = 0;
						if not does_overlap(new_rect, annotations[ind]):
							annotations[ind].rects.append(new_rect)
							print('Added');
					elif flagb and jb > 0 and False:
						back_rects = back_anno.rects;
						for rect in back_rects:
							if rect.classID == rId:
								brect = rect;
								break;
						back_2_rects = annotations[jb-1].rects;
						flagg = False;
						for rect in back_2_rects:
							if rect.classID == rId:
								flagg = True;
								b2rect = rect;
								break;
						if flagg:
							k = ind - jb;
							print k;
							b_x1 = brect.x1; b2_x1 = b2rect.x1;
							b_x2 = brect.x2; b2_x2 = b2rect.x2;
							b_y1 = brect.y1; b2_y1 = b2rect.y1;
							b_y2 = brect.y2; b2_y2 = b2rect.y2;
							n_x1 = b_x1* (k+1) - b2_x1* k;
							n_x2 = b_x2* (k+1) - b2_x2* k;
							n_y1 = b_y1* (k+1) - b2_y1* k;
							n_y2 = b_y2* (k+1) - b2_y2* k;
							new_rect = AnnoRect(int(n_x1), int(n_y1), int(n_x2), int(n_y2));
							new_rect.classID = rId;
							new_rect.score = 0;
							if does_overlap(new_rect, annotations[ind]):
								annotations[ind].rects.append(new_rect)
								print('Added');

					elif flagf and jf < anno_size - 2 and False:
						forward_rects = forward_anno.rects;
						for rect in forward_rects:
							if rect.classID == rId:
								frect = rect;
								break;
						forward_2_rects = annotations[jf+1].rects;
						flagg = False;
						for rect in forward_2_rects:
							if rect.classID == rId:
								flagg = True;
								f2rect = rect;
								break;
						if flagg:
							k = jf - ind ;
							f_x1 = frect.x1; f2_x1 = f2rect.x1;
							f_x2 = frect.x2; f2_x2 = f2rect.x2;
							f_y1 = frect.y1; f2_y1 = f2rect.y1;
							f_y2 = frect.y2; f2_y2 = b2rect.y2;
							n_x1 = f_x1* (k+1) - f2_x1* k;
							n_x2 = f_x2* (k+1) - f2_x2* k;
							n_y1 = f_y1* (k+1) - f2_y1* k;
							n_y2 = f_y2* (k+1) - f2_y2* k;
							new_rect = AnnoRect(int(n_x1), int(n_y1), int(n_x2), int(n_y2));
							new_rect.classID = rId;
	#						new_rect.score =
							if does_overlap(new_rect, annotations[ind]):
								annotations[ind].rects.append(new_rect)
								print('Added');
		
		ind += 1;
		


def show_3D(annotations,rdr_map, args, save_video = False, with_options=False, with_radar=False):
	if (save_video):
		writer = cv2.VideoWriter('edited_sequence_test3D.avi', cv.CV_FOURCC('X','V', 'I', 'D'),
			    20.0, (1280,960) )	
	ind = 0;
	anno_size = len(annotations);
	while True:
		frame_num = ind * 10
		if(ind >= anno_size or frame_num >=len(rdr_map)):
			break;
		if (with_options):
			choice = raw_input("> ");
		else:
			choice = 'f';
		if choice=='f': di = 1;
		elif choice=='b': di = -1;
		elif choice == 'x': break;
		annotation = annotations[ind];	
		ImgName =  annotation.filename();
		ex_dir = '/scail/group/deeplearning/driving_data/andriluka/IMAGES/driving_data_q50_data/all_extracted/'
		ImgName = ex_dir +'/'.join(ImgName.split('/')[-2:])
		print ImgName;
		
		radar_data = loadRDR(rdr_map[frame_num])[0]
		 
		rects = annotation.rects;
		I = cv2.imread(ImgName);
			

		if radar_data.shape[0] > 0:
		    # Remove points that have a low radar cross-section
		    mask = (radar_data[:, 5] > 0)
		    # Remove points that are moving too fast (fixed objects)
		    mask &= (radar_data[:, 6] > -20)
		    radar_data = radar_data[mask]

		if radar_data.shape[0] > 0:
		    front_right_pts = np.array(radar_data)
		    front_right_pts[:,0] += radar_data[:,3]
		    front_right_pts[:,1] += radar_data[:,4] / 2.

		    front_left_pts = np.array(radar_data)
		    front_left_pts[:,0] += radar_data[:,3]
		    front_left_pts[:,1] -= radar_data[:,4] / 2.

		    right_pts = np.array(radar_data)
		    right_pts[:,1] += radar_data[:,4] / 2.

		    left_pts = np.array(radar_data)
		    left_pts[:,1] -= radar_data[:,4] / 2.

		    # reproject camera_t points in camera frame
		    front_right_proj = projectPoints(front_right_pts, args)
		    front_left_proj = projectPoints(front_left_pts, args)
		    left_proj = projectPoints(left_pts, args)
		    right_proj = projectPoints(right_pts, args)
		    center_proj = projectPoints(np.array(radar_data), args)
		    for r, rect in enumerate(rects):
				cn_idx = 0;
				flag = False;
				while(True):
					if left_proj[cn_idx][7] == rect.classID:
						flag = True;
						break;
					cn_idx += 1;
					if cn_idx > len(left_proj)-1:
						break;
				if not flag:
					cv2.rectangle(I, (int(rect.x1),int(rect.y1)), (int(rect.x2), int(rect.y2)), (0,0,255),2);
				else:
					radar_width_1 = front_right_proj[cn_idx][8]-left_proj[cn_idx][8];
					radar_width_2 = front_left_proj[cn_idx][8]-right_proj[cn_idx][8];
					radar_width = max(abs(radar_width_1), abs(radar_width_2));
					if radar_width < 4: 
						cv2.rectangle(I, (int(rect.x1),int(rect.y1)), (int(rect.x2), int(rect.y2)), (0,0,255),2);
						break;
					else:
						scale_factor = rect.width()/radar_width;
						flag0 = False;
						#cv2.circle(I, tuple(front_left_proj[cn_idx][8:10].astype(np.int32)), 4, (255,255,0))
						if front_right_proj[cn_idx][8] > right_proj[cn_idx][8]:
							flag0 = True;
						#	cv2.circle(I, tuple(left_proj[cn_idx][8:10].astype(np.int32)), 4, (255,255,0))
							pnt0 = [int(rect.x1), int(rect.y2)];
							#print right_proj[cn_idx][8:10], left_proj[cn_idx][8:10]
							r_vector = [int(scale_factor * (left_proj[cn_idx][8]-right_proj[cn_idx][8])), 0];
							f_vector = [int(scale_factor * (front_left_proj[cn_idx][8]-left_proj[cn_idx][8])), 
									int(scale_factor * (front_left_proj[cn_idx][9] - left_proj[cn_idx][9]))]
							t_vector = [0, -int(rect.height())];
							
						else:
							r_vector = [int(scale_factor * (left_proj[cn_idx][8]-right_proj[cn_idx][8])), 0];
							f_vector = [int(scale_factor * (front_right_proj[cn_idx][8]-right_proj[cn_idx][8])), 
									int(scale_factor * (front_right_proj[cn_idx][9] - right_proj[cn_idx][9]))]
							t_vector = [0, -int(rect.height())];
							pnt0 = [int(rect.x2)- r_vector[0] , int(rect.y2)];
							
						bbl = pnt0;
						bbr = [pnt0[0] + r_vector[0], pnt0[1]];
						bfl = [pnt0[0] + f_vector[0], pnt0[1] + f_vector[1]];
						bfr = [pnt0[0] + f_vector[0] + r_vector[0], pnt0[1] + f_vector[1]];
						tbl = [pnt0[0], pnt0[1] + t_vector[1]];
						tbr = [pnt0[0] + r_vector[0], pnt0[1] + t_vector[1]];
						tfl = [pnt0[0] + f_vector[0], pnt0[1] + int(-.2*f_vector[1]) + t_vector[1]];
						tfr = [pnt0[0] + f_vector[0] + r_vector[0], pnt0[1] + int(-.2*f_vector[1]) + t_vector[1]];
							 
							
				#		cv2.line(I, tuple(bfr), tuple(bfl), (255,255,0))
						if not flag0:
							cv2.line(I, tuple(bfl), tuple(bbl), (255,255,0))
						if rect.score==0:
							cv2.line(I, tuple(bbl), tuple(bbr), (0,255,0))
						else:
							cv2.line(I, tuple(bbl), tuple(bbr), (255,0,0))
						if flag0: 
							cv2.line(I, tuple(bbr), tuple(bfr), (255,255,0))
							
						cv2.line(I, tuple(tfr), tuple(tfl), (255,255,0),1)
						cv2.line(I, tuple(tfl), tuple(tbl), (255,255,0),1)
						if rect.score==0:
							cv2.line(I, tuple(tbl), tuple(tbr), (0,255,0),2)
						else:
							cv2.line(I, tuple(tbl), tuple(tbr), (255,0,0),2)
						cv2.line(I, tuple(tbr), tuple(tfr), (255,255,0),1)
						if flag0:
							cv2.line(I, tuple(tfr), tuple(bfr), (255,255,0))
						if not flag0:
							cv2.line(I, tuple(tfl), tuple(bfl), (255,255,0))
						if rect.score==0:
							cv2.line(I, tuple(tbl), tuple(bbl), (0,255,0),2)
						else:
							cv2.line(I, tuple(tbl), tuple(bbl), (255,0,0),2)

						if rect.score==0:
							cv2.line(I, tuple(tbr), tuple(bbr), (0,255,0),2)
						else:
							cv2.line(I, tuple(tbr), tuple(bbr), (255,0,0),2)
						
						cv2.putText(I, str(rect.classID), tuple(tbr),
						    cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,255), thickness=1)
	#	    mmap = RadarTrackerMapping(right_proj[:,8:10], np.array(bottom_right_pnt));
		    if with_radar:
			for j in xrange(front_right_proj.shape[0]):
				fr = front_right_proj[j, 8:10].astype(np.int32)
				fl = front_left_proj[j, 8:10].astype(np.int32)
				bl = left_proj[j, 8:10].astype(np.int32)
				br = right_proj[j, 8:10].astype(np.int32)

				cv2.line(I, tuple(fr), tuple(fl), (255,255,0))
				cv2.line(I, tuple(fl), tuple(bl), (255,255,0))
				cv2.line(I, tuple(bl), tuple(br), (255,0,0))
				cv2.line(I, tuple(br), tuple(fr), (255,255,0))
		ind += 1;
		cv2.imshow('img1',I);
		if(save_video):
			writer.write(I);

		cv2.waitKey(20)
def compute_statistics(annotations, rdr_map):
	idx = 0;
	anno_size = len(annotations);
	hasnt_radar_w = [];
	all_w = [];
	hasnt_tracker_d = [];
	all_d = [];
	while(True):
		if(idx >= anno_size):
			break;
		annotation = annotations[idx];
		frame_num = idx * 10
		radar_data = loadRDR(rdr_map[frame_num])[0]
		if radar_data.shape[0] > 0:
		    # Remove points that have a low radar cross-section
		    mask = (radar_data[:, 5] > 0)
		    # Remove points that are moving too fast (fixed objects)
		    mask &= (radar_data[:, 6] > -20)
		    radar_data = radar_data[mask]

		 
		rects = annotation.rects;
		for i, rect in enumerate(rects):
			cn_idx = 0;
			flag = False;
			while(True):
				if radar_data[cn_idx][7] == rect.classID:
					flag = True;
					break;
				cn_idx += 1;
				if cn_idx > len(radar_data)-1:
					break;
			all_w.append(rect.width());
			if not flag:
				hasnt_radar_w.append(rect.width());
		
		for i, rdr in enumerate(radar_data):
			cn_idx = 0;
			flag = False;
			while(True):
				if rects[cn_idx].classID == rdr[7]:
					flag = True;
					break;
				cn_idx += 1;
				if cn_idx > len(rects)-1:
					break;
			all_d.append(rdr[0]);
			if not flag:
				hasnt_tracker_d.append(rdr[0]);
		idx += 1;
	hist_hasnt_radar_w = np.histogram(hasnt_radar_w,20);  
	hist_all_w = np.histogram(all_w,20);  
	
	hist_hasnt_tracker_d = np.histogram(hasnt_tracker_d,10);  
	hist_all_d = np.histogram(all_d,10);  

	ratio_w = [1.0*hist_hasnt_radar_w[0][i]/hist_all_w[0][i] for i in range(20)];	
	ratio_d = [1.0*hist_hasnt_tracker_d[0][i]/hist_all_d[0][i] for i in range(10)];	
	print hist_hasnt_radar_w;
	print hist_all_w;
	print hist_hasnt_tracker_d;
	print hist_all_d;
	
	print(ratio_w);	
	print(ratio_d);

if __name__ == "__main__":
	if (len(sys.argv) < 4):
		print "python radar_tracker.py <.al file> <directory of .avi> <video file>"
		sys.exit();
	
	filename = (sys.argv[1]);
	print "Loading annotation file . . .";
	annotations = parseXML(filename);
	print len(annotations);
	
	args = parse_args(sys.argv[2], sys.argv[3])
  	params = args['params']
   
  	video_reader = VideoReader(args['video'])
   	rdr_map = loadRDRCamMap(args['map'])
	
	set_annotations_ids_using_radar(annotations, rdr_map, args);   
	fill_gaps(annotations, rdr_map);
	for annotation in annotations:
		for rect in annotation.rects:
			rect.classID = int(rect.classID);
	save_filename = filename.split('.')[0] + "_new.al";
	saveXML(save_filename, annotations);
#	compute_statistics(annotations, rdr_map);
#	show_3D(annotations, rdr_map,args, True, False, True);
#	print "Writing new annotations into a file..."
#	saveXML(filename.split('.')[1] + "_with_distance.al", annotations);
