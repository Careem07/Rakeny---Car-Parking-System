
import cv2
import numpy as np
import pymysql as db

connection = db.connect(host="localhost", user="root", passwd="kareem2000", database="park_db")
cursor = connection.cursor()

# video_capture = cv2.VideoCapture("./lastdemo_.mp4")
# height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
# width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
# #background_image = cv2.imread("./org.png")
# #org = cv2.imread("./org.png")
# fourcc =  cv2.VideoWriter_fourcc(*'DVID') #DVID #DIVX
# out_diff = cv2.VideoWriter("./lastdemo1111.mp4", fourcc, 20.0, (width,height))

# while(True):
#     ret, frame = video_capture.read()    
    
#     blured_frame = cv2.GaussianBlur(frame , (5,5), 0)
#     img_gray = cv2.cvtColor(blured_frame, cv2.COLOR_BGR2GRAY)
#     ret, thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
#     cv2.imshow('Binary image', thresh)

#     out_diff.write(thresh)
#     if cv2.waitKey(1) & 0xFF == ord('q'): break


# video_capture.release()

def check_region(x,y,w,h,frame):
    newf = frame[y:h,x:w]
    sw = np.sum(newf==255)
    sb = np.sum(newf==0)
    totalpix = sw + sb
    black = int((sb / totalpix) *100)
    white = int((sw / totalpix) *100)
    print("BLACK ", black)
    print("WHITE ", white)
    print("total pixels " , totalpix)
    print("sw" ,sw)
    print("sb" , sb)
    
    if (sw > sb) and (black < 30):
        #print("Region is white ") #1
        x=1
    else:
        #print("Region is black")
        x=0
    return x

def update_region(oldfree,newfree,id):
    if oldfree != newfree:
        oldfree = newfree
        query = """UPDATE garage SET free = %s WHERE id = %s"""
        value = (newfree,id)
        cursor.execute(query,value)
        connection.commit()
        print("Record Updated")
    else:
        oldfree = oldfree
    
    
    

#connection = db.connect(host="localhost", user="root", passwd="kareem2000", database="park_db")
#cursor = connection.cursor()
query = "SELECT x,y,w,h,id,free FROM garage"
cursor.execute(query)

results = cursor.fetchall()
records = np.array(results)
#print(records[0])
#sel = cursor.execute(query)

cap =cv2.VideoCapture("./lastdemo1111.mp4")
x,y,w,h,_,_ = records[0]

#cap= cv2.VideoCapture(0)

while(True):
    _,frame=cap.read()

    for i in range(0,33):
        #x,y,w,h,_,_ = records[i]
        x = records[i][0]
        y = records[i][1]
        w = records[i][2]
        h = records[i][3]
        id = records[i][4]
        free = records[i][5]
        #print(id)
        cv2.rectangle(frame , (records[i][0],records[i][1]),(records[i][2],records[i][3]),(0,0,255),2)
        newval = check_region(x,y,w,h,frame)
        update_region(free,newval,id)
        print("Value " , newval)
        

    cv2.imshow('Fram image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #array.append(check)
        cv2.imwrite("Output frame ", frame)
        break