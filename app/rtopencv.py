import threading, time, io
import picamera, picamera.array, cv2
import imageprocessor


class RTOpenCV(threading.Thread):

    status_lock = threading.Lock()

    def __init__(self, camera, callback):
        super(RTOpenCV, self).__init__()
        RTOpenCV.camera = camera

        # three streams will be used
        #   only one is in Processing/Capturing at a time
        RTOpenCV.streams = [picamera.array.PiRGBArray(self.camera),
                            picamera.array.PiRGBArray(self.camera),
                            picamera.array.PiRGBArray(self.camera)]
        # possible frame status: Empty, Capturing, Ready, Processing
        RTOpenCV.status = ['Empty','Empty','Empty']
        # stop condition for the thread
        RTOpenCV.stop = False
        RTOpenCV.processor = imageprocessor.ImageProcessor()
        RTOpenCV.callback = staticmethod(callback)
        self.start()

    def run(self):
        self.start_time = time.time()
        RTOpenCV.camera.capture_sequence(RTOpenCV._streams(), use_video_port=True, format='bgr')

    def close(self):
        RTOpenCV.stop = True
        self.join()
        RTOpenCV.processor.join()
        self.stop_time = time.time()

    def get_fps(self):
        return self.processor.num_frames/(time.time()-self.start_time)

    @staticmethod
    def _discard_frames(last_frame):
        # check if another frame is Ready
        # in that case, discard it (only last frame is usefull)
        if RTOpenCV.status[(last_frame+1)%3] == 'Ready':
            RTOpenCV.status[(last_frame+1)%3] = 'Empty'
        if RTOpenCV.status[(last_frame+2)%3] == 'Ready':
            RTOpenCV.status[(last_frame+2)%3] = 'Empty'

    @staticmethod
    def _streams():
        # yield a stream for capture_sequence
        frames=0
        # first select an non used stream
        while not RTOpenCV.stop:
            free_stream = -1
            with RTOpenCV.status_lock:
                for i in range(3):
                    if RTOpenCV.status[i] == 'Empty':
                        RTOpenCV.status[i] = 'Capturing'
                        free_stream = i
                        break
                if free_stream == -1:
                    for i in range(3):
                        if RTOpenCV.status[i] == 'Ready':
                            RTOpenCV.status[i] = 'Capturing'
                            free_stream = i
                            break
                RTOpenCV.streams[free_stream].seek(0)

            yield RTOpenCV.streams[free_stream]

            # if stream have not been used, mark it ready
            with RTOpenCV.status_lock:
                if RTOpenCV.status[free_stream]=='Capturing':
                    RTOpenCV.status[free_stream]='Ready'
                    RTOpenCV._discard_frames(free_stream)
            frames+=1
        return
