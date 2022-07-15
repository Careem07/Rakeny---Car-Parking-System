import cv2


video_capture = cv2.VideoCapture("./lastdemo_.mp4")
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#background_image = cv2.imread("./org.png")
#org = cv2.imread("./org.png")
fourcc =  cv2.VideoWriter_fourcc(*'DVID') #DVID #DIVX
out_diff = cv2.VideoWriter("./lastdemo1111.mp4", fourcc, 20.0, (width,height))

while(True):
    ret, frame = video_capture.read()    
    
    blured_frame = cv2.GaussianBlur(frame , (5,5), 0)
    img_gray = cv2.cvtColor(blured_frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow('Binary image', thresh)

    out_diff.write(thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'): break


video_capture.release()