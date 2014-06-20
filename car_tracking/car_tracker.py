

class CarTracker(object):
    def __init__(self, tracker, annolist, track_frames=20):
        self.tracker
        self.annolist
        self.track_frames = track_frames
        
    def run(self):
        for idx, anno in enumerate(self.annolist):
            stop_imgname = self.get_stop_img(idx)

            img_seq = [self.inc_image_name(anno, i) \
                           for i in 
            #self.tracker.run(
            
        return tracked_annotations

    def get_stop_img(self, idx):
        if idx < len(self.annolist) - 1:
            return self.annolist[idx+1].imageName
        else:
            return self.inc_image_name(self.annolist[idx].imageName)
            
    def inc_image_name(self, s, n=None):
        if n == None:
            n = self.track_frames
        pos1 = s.rfind('_')
        pos2 = s.rfind('.')

        num = int(s[pos1+1:pos2]) + n
        numlen = pos2 - pos1 - 1
        res = s[:pos1+1] + str(num).zfill(numlen) + s[pos2:]
        return res        
        
