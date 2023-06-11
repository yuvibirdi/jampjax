# Including Important libraries
import cv2
import mediapipe as mp
import numpy as np
import time
from tkinter import*
from PIL import Image, ImageTk
from datetime import timedelta
import tkinter.font as font
import socket
from datetime import datetime

import os
os.environ['TCL_LIBRARY'] = 'C:\\Users\\andar\\AppData\\Local\\Programs\\Python\\Python311\\tcl\\tcl8.6'
os.environ['Tk_LIBRARY'] = 'C:\\Users\\andar\\AppData\\Local\\Programs\\Python\\Python311\\tcl\\tk8.6'


# functions

def udp_send(ex_name:str):

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    MESSAGE = b"Jumping Jack"

    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))




# Creating a new tkinter window
win = Tk()
win.title("Jumping Jacks Trainer")    # setting title of window
win.geometry("900x600+200+30")        #setting geometry

# making a frame witin the window
frame_1 = Frame(win, width=900, height=700, bg="#ffdbac").place(x=0, y=0)

# make a label to insert our video within
w = 450
h = 300
L1 = Label(frame_1, width=w, height=h, relief=SUNKEN)
L1.place(x=200, y=260)

#List of video names that we can include in dropdown menu
# options = [
#     "Cam",
#     "Video 1.mkv",
#     "Video 2.mkv",
#     "Video 3.mkv",
#     "Video 4.mp4",
#     "Video 5.mp4",
#     "--->>"
# ]

# clicked=StringVar()
# clicked.set(options[0])  #setting default video as "Video 3.mkv"
# drop = OptionMenu(frame_1, clicked, *options).place(x=55, y=360) 

# to draw on pose using media pipe
mp_drawing  = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
   
# Function to calculate angle
def calculate_angle(a,b,c):
    a = np.array(a) #First
    b = np.array(b) #Mid
    c = np.array(c) #End
    
    # print(a)
    # print(b)
    # print(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0])-np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    # print(f'radians: {radians}')
    # print(f'angle: {angle}')

    if angle>180.0:
        angle=360-angle
    
    return angle

def calculate_vertical_distance(a,b):
    a = np.array(a)
    b = np.array(b)
    
    return np.abs(b[1]-a[1]);


def push_up_qualify1(hist_ind):
                    
    prev_time_stamp = (hist_ind-1)%max_time_frames
    dyf = np.abs(landmarks_xy_hist[hist_ind][0][1]-landmarks_xy_hist[hist_ind][4][1])
    dxf = np.abs(landmarks_xy_hist[hist_ind][0][0]-landmarks_xy_hist[hist_ind][4][0])
    dyi = np.abs(landmarks_xy_hist[prev_time_stamp][0][1]-landmarks_xy_hist[prev_time_stamp][4][1])
    dxi = np.abs(landmarks_xy_hist[prev_time_stamp][0][0]-landmarks_xy_hist[prev_time_stamp][4][0])
    
    if(dyi>dyf and np.abs(dyi-dyf)>=2*np.abs(dxi-dxf)):
        return True;
    else:
        return False;
    
    
# def push_up_qualify2(hist_ind):
                    
#     prev_time_stamp = (hist_ind-1)%max_time_frames
#     dyf = np.abs(landmarks_xy_hist[hist_ind][0][1]-landmarks_xy_hist[hist_ind][4][1])
#     dxf = np.abs(landmarks_xy_hist[hist_ind][0][0]-landmarks_xy_hist[hist_ind][4][0])
#     dyi = np.abs(landmarks_xy_hist[prev_time_stamp][0][1]-landmarks_xy_hist[prev_time_stamp][4][1])
#     dxi = np.abs(landmarks_xy_hist[prev_time_stamp][0][0]-landmarks_xy_hist[prev_time_stamp][4][0])
    
#     if(dyi>dyf and np.abs(dyi-dyf)>=2*np.abs(dxi-dxf)){
#         return True;
#     } else {
#         return False;
#     }


# REPS counter variables
jjcounter = 0  # counter for jumping jacks
sqcounter = 0  # counter for squats
hkcounter = 0  # counter for high knees
pucounter = 0
stage = None 
pTime=0

# if new getting video is not equal to already setted video
# if clicked.get()!= clicked.set(options[0]):
#     video=1

# start calculating time for displaying
start = time.time()
# start = datetime.now()



# main while loop
while True:
    # print("0.")
    # if clicked.get()=="Cam":
    #     print("camera")
    #     cap = cv2.VideoCapture(0)     # if Cam is selected from menu
    # else:
    #     cap = cv2.VideoCapture(clicked.get())     # is a vedio is selected from menu

    time_rec_delay = 0.2
    push_up_delay = 0.4
    max_time_frames = 100
    hist_ind = 0
    # landmarks_xy_hist = {}
    landmarks_xy_hist = [0 for i in range(0, max_time_frames)]
    last_time_update = -1

    cap = cv2.VideoCapture(0)
    

    with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        
        # print("1.")
        while cap.isOpened():
            
            # print("Time: "+datetime.now().strftime("%H:%M:%S")) 
            # now = datetime.now()
            # print("Time: "+now.strftime("%S"))
            # print("Elapsed: {:.1f}".format(start.timestamp()))
            # print("1.0")

            image = cap.read()[1]      # reading images from video
            image = cv2.resize(image, (w, h))          #resizing our video according to the label

            # Recolor image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Extract Landmarks
            try:
                
                # print("1")
                landmarks = results.pose_landmarks.landmark

                # "1" is left (or right side of received image)
                # "2" is right (or left side of received image)

                # Get coordinates
                shoulder1=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip1=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                wrist1=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                ankle1=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                knee1=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                elbow1=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                index1=[landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]
                
                
                # print("2")

                shoulder2=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip2=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                wrist2=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                ankle2=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                knee2=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                elbow2=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                
                
                
                # print("3")

                # Calculate angle
                hip_shoulder_wrist1 = calculate_angle(hip1, shoulder1, wrist1)
                hip_shoulder_wrist2 = calculate_angle(hip2, shoulder2, wrist2)
                shoulder_hip_ankle1 = calculate_angle(shoulder1, hip1, ankle1)
                shoulder_hip_ankle2 = calculate_angle(shoulder2, hip2, ankle2)
                
                hip_knee_ankle1 = calculate_angle(hip1, knee1, ankle1)
                hip_knee_ankle2 = calculate_angle(hip2, knee2, ankle2)
                shoulder_hip_knee1 = calculate_angle(shoulder1, hip1, knee1)
                shoulder_hip_knee2 = calculate_angle(shoulder2, hip2, knee2)
                
                shoulder_ankle_wrist1 = calculate_angle(shoulder1, ankle1, wrist1)
                shoulder_ankle_wrist2 = calculate_angle(shoulder2, ankle2, wrist2)
                shoulder_elbow_wrist1 = calculate_angle(shoulder1, elbow1, wrist1)
                shoulder_elbow_wrist2 = calculate_angle(shoulder2, elbow2, wrist2)
                # print("4")

                # Visualize angle
                cv2.putText(image, str(int(hip_shoulder_wrist1)),
                                tuple(np.multiply(shoulder1, [300, 480]).astype(int)),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                            )
                # print("5")

                cv2.putText(image, str(int(hip_shoulder_wrist2)),
                                tuple(np.multiply(shoulder2, [600, 480]).astype(int)),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                            )
                # print("6")

                cv2.putText(image, str(int(shoulder_hip_ankle1)),
                                tuple(np.multiply(hip1, [300, 480]).astype(int)),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                            )
                # print("7")

                cv2.putText(image, str(int(shoulder_hip_ankle2)),
                                tuple(np.multiply(hip2, [600, 480]).astype(int)),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                            )
                # print("8")
                
                # print(f'stage: {stage}')
                # print(f'Angle 1: {hip_shoulder_wrist1}\nAngle 2: {hip_shoulder_wrist2}\nAngle 3: {shoulder_hip_ankle1}\nAngle 4: {shoulder_hip_ankle2}')
                # print("Requirements:")
                # print(f'Up: <30 <30 >170 >170')
                # print(f'Down: >160 >160 <160 <160')

                #  counter logic

                # detect jumping jack:
                #  detect down
                # regular jumping jack
                
                # print(f'ankles: {ankle1}')
                print(f'Left index: {index1}')
                
                # print(f'start stage: {stage}')
                if hip_shoulder_wrist1 < 30 and hip_shoulder_wrist2 < 30 and shoulder_hip_ankle1 > 170 and shoulder_hip_ankle2 > 170 :
                    if(stage=='jjup1'):
                        jjcounter+=1

                        # standard output indicating jumping jack completion
                        # print("Jumping Jack\n\n\n\nbbbbbb\n\n\n\n")
                        udp_send("Jumping Jack")
                    stage = 'jjdown1'

                # inverse jumping jack          
                if hip_shoulder_wrist1 < 30 and hip_shoulder_wrist2 < 30 and shoulder_hip_ankle1 < 170 and shoulder_hip_ankle2 < 170 :
                    if(stage=='jjup2'):
                        jjcounter+=1

                        # standard output indicating jumping jack completion
                        
                        # print("Jumping Jack\n\n\n\nbbbbbb\n\n\n\n")
                        udp_send("Jumping Jack")
                    
                    stage = 'jjdown2'
                    
                    
                    
                #  detect up
                #  regular jumping jack
                if hip_shoulder_wrist1 > 150 and hip_shoulder_wrist2 > 150 and shoulder_hip_ankle1 < 170 and shoulder_hip_ankle2 < 170 and stage == 'jjdown1':
                    stage = 'jjup1'
                    
                
                # inverse jumping jack
                if hip_shoulder_wrist1 > 150 and hip_shoulder_wrist2 > 150 and shoulder_hip_ankle1 > 170 and shoulder_hip_ankle2 > 170 and stage == 'jjdown2':
                    stage = 'jjup2'
                    
                    
                
                # print(f'{hip_knee_ankle1} {hip_knee_ankle2}')
                
                # detect squat:
                # detect down
                if hip_knee_ankle1<=130 and hip_knee_ankle2<=130:
                    stage='sqdown'
                # detect up
                if hip_knee_ankle1>=110 and hip_knee_ankle2>=110 and stage=='sqdown':
                    stage='squp'
                    sqcounter+=1
                    # print("Squat\n\n\n\n\n\n\n")
                    udp_send("Squat")
                # if hip_to_knee1<=knee_to_ankle1*0.7 and hip_to_knee2<=knee_to_ankle2*0.7:
                #     stage = 'sqdown'
                # # detect up
                # if hip_to_knee1>=knee_to_ankle1*0.5 and hip_to_knee2>=knee_to_ankle2*0.5 and stage=='sqdown':
                #     stage = 'squp'
                #     sqcounter+=1
                #     print("Squat")
                
                # detect high knees:
                # detect high knee left
                
                # print(f'{shoulder_hip_knee1} {hip_knee_ankle1} {shoulder_hip_knee2} {hip_knee_ankle2}')
                if shoulder_hip_knee1<=130 and hip_knee_ankle1<=110 and shoulder_hip_knee2>=150 and hip_knee_ankle2>=150:
                    if(stage=='hkright'):
                        hkcounter+=1
                        # print("High knee cycle ended left\n\naaaaaaaaaaaaaaaa\n\n")
                        udp_send("High Knee")
                    stage='hkleft'
                    
                if shoulder_hip_knee1>=150 and hip_knee_ankle1>=150 and shoulder_hip_knee2<=130 and hip_knee_ankle2<=110:
                    if(stage=='hkleft'):
                        hkcounter+=1
                        # print("High knee cycle ended right\n\naaaaaaaaaaaaaaaa\n\n")
                        udp_send("High Knee")
                    stage='hkright'
                    
                # print(f'end stage: {stage}')
                


                # if ((shoulder_ankle_wrist1<=30 and shoulder_ankle_wrist2<=30)or(shoulder_elbow_wrist1<=20 and shoulder_elbow_wrist2<=20)) and push_up_qualify1(hist_ind):
                #     pucounter+=1
                #     print("\n\n\n\nPush Up\n\n\n\n")
                #     udp_send("Push Up")
                
                
                # detect push ups
                # if shoulder_ankle_wrist1<=20
                
                
                
                    
            except:
                # print("passed")
                pass

            # fonts for label text
            f = font.Font(family='Agency FB', size=20, weight="bold")  
            f1= font.Font(family='Agency FB', size=34, weight="bold")
            
            mylabel = Label(frame_1, text="JUMPING",font= f1, bg="#ffdbac", fg="black").place(x=280, y=50)
            mylabel7 = Label(frame_1, text="JACKS",font= f1, bg="#ffdbac", fg="black").place(x=300, y=110)
            mylabel8 = Label(frame_1, text="TRAINER",font= f1, bg="#ffdbac", fg="black").place(x=290, y=170)
            mylabel9 = Label(frame_1, text="SELECT",font= f, bg="#ffdbac", fg="black").place(x=60, y=280)
            mylabel10 = Label(frame_1, text="VIDEO",font= f, bg="#ffdbac", fg="black").place(x=65, y=312)
            mylabel1 = Label(frame_1, text="REPS: " + str(jjcounter) +"   ", font=f ,bg="#ffdbac", fg="black").place(x=700, y=280)  # display REPS
            mylabel2 = Label(frame_1, text="STAGE: DOWN",font=f, bg="#ffdbac", fg="black").place(x=700, y=350)  # Display stage
            if stage=='up':
                mylabel2 = Label(frame_1, text="STAGE: UP    ",font=f, bg="#ffdbac", fg="black").place(x=700, y=350)
                
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )

            cTime = time.time()
            fps = 1/(cTime-pTime)       # calculate fps of video
            pTime = cTime
            end = time.time()
            
            # dt = timedelta(seconds= int(end-start)).total_seconds()
            dt = end-start
            
            # if(dt-last_time_update>=push_up_delay):
            #     last_time_update=dt;
            #     # print("\naaaaaaaa\naaaaaaaaa\naaaaaaaa\naaaaaaaaaa")
            #     landmarks_xy_hist[hist_ind]=[
            #         shoulder1,
            #         shoulder2,
            #         hip1,
            #         hip2,
            #         wrist1,
            #         wrist2,
            #         ankle1,
            #         ankle2,
            #         knee1,
            #         knee2,
            #         elbow1,
            #         elbow2
            #     ]
            #     hist_ind=(hist_ind+1)%max_time_frames
            #     # print(landmarks_xy_hist)
                

            mylabel3 = Label(frame_1, text="FPS: " + str(int(fps)) +"    ",font=f, bg="#ffdbac", fg="black").place(x=700, y=430)    # display fps
            mylabel4 = Label(frame_1, text="TIME: " + str(timedelta(seconds= int(end-start))) + "   ",font=f, bg="#ffdbac", fg="black").place(x=700, y=500)  #display time

            # Display Image of logo
            my_img = ImageTk.PhotoImage(Image.open("jump.png"))
            myLabel5=Label(frame_1, bg="#ffdbac", image=my_img).place(x=430,y=50)

            # putting videom in label
            image = ImageTk.PhotoImage(Image.fromarray(image))
            L1['image']=image     

            # if video is changed, start time and REPS from zero
            # if video==1:
            #     if clicked.get()=="Cam":
            #         start=time.time()
            #         jjcounter=0
            #         cap = cv2.VideoCapture(0)
            #         clicked.set(options[6])
                # if clicked.get()=="Video 1.mkv":
                #     start=time.time()
                #     jjcounter=0
                #     cap = cv2.VideoCapture("Video 1.mkv")
                #     clicked.set(options[6])
                # if clicked.get()=="Video 2.mkv":
                #     start=time.time()
                #     jjcounter=0
                #     cap = cv2.VideoCapture("Video 2.mkv")
                #     clicked.set(options[6])
                # if clicked.get()=="Video 3.mkv":
                #     start=time.time()
                #     jjcounter=0
                #     cap = cv2.VideoCapture("Video 3.mkv")
                #     clicked.set(options[6])
                # if clicked.get()=="Video 4.mp4":
                #     start=time.time()
                #     jjcounter=0
                #     cap = cv2.VideoCapture("Video 4.mp4")
                #     clicked.set(options[6])
                # if clicked.get()=="Video 5.mp4":
                #     start=time.time()
                #     jjcounter=0
                #     cap = cv2.VideoCapture("Video 5.mp4")
                #     clicked.set(options[6])
                # if clicked.get()=="--->>":
                #     pass

            win.update()

            # if user press "q" exit the loop
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
        cap.release()
        win.mainloop()
                