import cv2
import numpy as np
import pymysql as db

def check_region(x,y,w,h,frame):
    newf = frame[y:y+h,x:x+w]
    sw = np.sum(newf==255)
    sb = np.sum(newf==0)
    # print("sw" ,sw)
    # print("sb" , sb)
    if (sw > sb):
        #print("Region is white ") #1
        x=1
    else:
        #print("Region is black")
        x=0
    return x

connection = db.connect(host="localhost", user="root", passwd="kareem2000", database="park_db")
cursor = connection.cursor()
frame = cv2.imread("./newframe3.png")
greenframe = cv2.imread("./greenFrame.png")
list = []
greenList = []
low_white = np.array([0,0,0])
hi_white = np.array([0,0,0])
mask = cv2.inRange(frame , low_white , hi_white)
green_mask = cv2.inRange(greenframe, (0, 255, 0), (0, 255,0))

contours,_ = cv2.findContours(mask , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for  cnt in contours:
    area = cv2.contourArea(cnt)
    if (area > 1000) and (area < 400000):
        x,y,w,h = cv2.boundingRect(cnt)
        list.append([x,y,w,h])
        #cv2.rectangle(frame , (x,y),(x+w,y+h),(255,0,0),2)
        #cv2.drawContours(frame, contours=cnt , contourIdx=-1 , color=(0,255,0) , thickness= 1)

greencontours,_ = cv2.findContours(green_mask , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for index, cnt in enumerate(greencontours):
    area = cv2.contourArea(cnt)
    if area < 7000:
        xx,yy,ww,hh = cv2.boundingRect(cnt)
        greenList.append([xx,yy,ww,hh])
        #cv2.rectangle(frame , (xx,yy),(xx+ww,yy+hh),(255,0,0),2)
        #cv2.drawContours(frame, contours=cnt , contourIdx=-1 , color=(255,0,0) , thickness= 1)

#1 to 7 t7t   #               X           Y           (X     +     W)      (Y     +     H) 

#1,2
for i in range(5,7):
    cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(255,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1], list[i][2], list[i][3],frame)
    cv2.imshow("newf ", frame)
    cv2.waitKey(0)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    print(list[i])
    connection.commit()

#3,4
for i in range(0,2):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    #print(list[i])
    connection.commit()

#5,6
for i in range(3,5):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    #print(list[i])
    connection.commit()



# 7 
query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
x = check_region(list[2][0], list[2][1],list[2][2],list[2][3],frame)
val = (list[2][0],list[2][1],list[2][0]+list[2][2] , list[2][1]+list[2][3] , x )
cursor.execute(query , val )
connection.commit()

#middle saf mn 8 to 19
for i in range(7,10):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    #print(list[i])
    connection.commit()

query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
x = check_region(list[12][0], list[12][1],list[12][2],list[12][3],frame)
val = (list[12][0],list[12][1],list[12][0]+list[12][2] , list[12][1]+list[12][3] , x )
cursor.execute(query , val )
connection.commit()

x = check_region(list[10][0], list[10][1],list[10][2],list[10][3],frame)
val = (list[10][0],list[10][1],list[10][0]+list[10][2] , list[10][1]+list[10][3] , x )
cursor.execute(query , val )
connection.commit()

x = check_region(list[17][0], list[17][1],list[17][2],list[17][3],frame)
val = (list[17][0],list[17][1],list[17][0]+list[17][2] , list[17][1]+list[17][3] , x )
cursor.execute(query , val )
connection.commit()

for i in range(14,17,2):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    connection.commit()

for i in range(4):
    #cv2.rectangle(frame , (greenList[i][0],greenList[i][1]),(greenList[i][0]+greenList[i][2],greenList[i][1]+greenList[i][3]),(0,255,0),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(greenList[i][0], greenList[i][1],greenList[i][2],greenList[i][3],frame)
    val = (greenList[i][0],greenList[i][1],greenList[i][0]+greenList[i][2] , greenList[i][1]+greenList[i][3] , x )
    cursor.execute(query , val )
    #print(greenList[i])
    connection.commit()

#20 to 31
#a5r saff 
#awl 3
for i in range(11,16,2):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    #print(list[i])
    connection.commit()

for i in range(18,26):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    #print(list[i])
    connection.commit()

for i in range(28,33):
    #cv2.rectangle(frame , (list[i][0],list[i][1]),(list[i][0]+list[i][2],list[i][1]+list[i][3]),(0,0,255),2)
    query = """INSERT INTO  garage (x,y,w,h,free) VALUES (%s, %s, %s, %s, %s)"""
    x = check_region(list[i][0], list[i][1],list[i][2],list[i][3],frame)
    val = (list[i][0],list[i][1],list[i][0]+list[i][2] , list[i][1]+list[i][3] , x )
    cursor.execute(query , val )
    #print(list[i])
    connection.commit()


cv2.imshow('Fram image', frame)
cv2.waitKey(0)
