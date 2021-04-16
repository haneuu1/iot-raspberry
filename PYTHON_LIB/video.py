import cv2

class Video:
    def __init__(self, **kargs):
        device = kargs.get('device', -1)# 카메라 index/ 없으면 -1
        file = kargs.get('file')        # 디폴트 None
        if device >= 0: # 카메라 index를 받았다
            self.cap = cv2.VideoCapture(device)
        elif file:      # 파일경로, ip url - 문자열
            self.cap = cv2.VideoCapture(file)
    
    def __iter__(self):
        return self

    def __next__(self):# for문 돌면서 호출
        ret, image = self.cap.read()
        if ret:
            return image
        else:
            raise StopIteration
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, trace_back):# with 블럭 끝날 때 호출
        if self.cap and self.cap.isOpened():
            print("Video Release------")
            self.cap.release()
    
    @staticmethod
    def to_jpg(frame, quality=80):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), quality]
        is_success, jpg= cv2.imencode(".jpg", frame, encode_param)
        return jpg
    
    @staticmethod
    def show(image, exit_char=ord('q')):
        cv2.imshow('frame',image)
        if cv2.waitKey(1) & 0xFF == exit_char:
            return False
        return True

    @staticmethod
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def resize_frame(frame, width, height):
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

# if __name__ == '__main__':
#     with Video(device=0) as v:
#         for image in v:
#             image = Video.resize_frame(image, 320, 240)
#             image = Video.rescale_frame(image, 50)
#             jpg = Video.to_jpg(image, 60)
#             if not Video.show(image): break
#             cv2.imshow('frame', image)
#             if(cv2.waitKey(1) == 27):
#                 break
