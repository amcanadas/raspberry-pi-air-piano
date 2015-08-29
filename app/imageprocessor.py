import threading, time
import cv2

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        import rtopencv
        self.frame_size = rtopencv.RTOpenCV.camera.resolution[0]*\
                        rtopencv.RTOpenCV.camera.resolution[1]*3
        self.num_frames = 0
        self.start()

    def run(self):
        import rtopencv
        while not rtopencv.RTOpenCV.stop:
            # search the last captured frame
            ready = -1
            with rtopencv.RTOpenCV.status_lock:
                for i in range(3):
                    if rtopencv.RTOpenCV.streams[i].tell()==self.frame_size\
                            and rtopencv.RTOpenCV.status[i] == 'Capturing':
                        rtopencv.RTOpenCV.status[i] = 'Processing'
                        rtopencv.RTOpenCV._discard_frames(i)
                        ready = i
                        break
                if ready == -1:
                    for i in range(3):
                        if rtopencv.RTOpenCV.status[i] == 'Ready':
                            rtopencv.RTOpenCV.status[i] = 'Processing'
                            rtopencv.RTOpenCV._discard_frames(i)
                            ready = i
                            break
            # if frame found, process it
            if ready > -1:
		try:
                    rtopencv.RTOpenCV.callback(rtopencv.RTOpenCV, rtopencv.RTOpenCV.streams[ready].array)
		except:
		    print('Exception in image processor when callin callback')
                self.num_frames+=1
                # when processed, mark stream empty
                rtopencv.RTOpenCV.status[ready]='Empty'
            else:
                #no frame available
                time.sleep(0.002)
