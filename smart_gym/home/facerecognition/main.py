import cv2, csv

from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
import argparse
import sys, os
import json
import time
import numpy as np
import subprocess

BASE_DIR = os.getcwd()
if 'home/facerecognition' not in BASE_DIR:
    print("DIRECTORY IS", BASE_DIR)
    BASE_DIR += '/home/facerecognition'

TIMEOUT = 10


def main(args):
    mode = args.mode
    if mode == "camera":
        camera_recog()
    elif mode == "input":
        create_manual_data(args.profession, args.name)
    else:
        raise ValueError("Unimplemented mode")


def camera_recog():

    print("[INFO] camera sensor warming up...")
    vs = cv2.VideoCapture(0)
    cv2.namedWindow("get focus", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("get focus", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("get focus", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    subprocess.call(["/usr/bin/osascript", "-e", 'tell app "Finder" to set frontmost of process "Python" to true'])
    cv2.destroyWindow("get focus")

    detect_time = time.time()

    file = csv.reader(open('{}/current.csv'.format(BASE_DIR)))
    newValues = list(file)[:2]
    newValues[1][4] = 'No'
    newValues[1][5] = 0
    peopleAtGym = {}
    lastRow = 2

    while True:
        _,frame = vs.read()

        rects, landmarks = face_detect.detect_face(frame, 80)
        aligns = []
        positions = []

        for (i, rect) in enumerate(rects):
            aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
            else: 
                print("Align face failed")
        if(len(aligns) > 0):
            features_arr = extract_feature.get_features(aligns)
            recog_data = findPeople(features_arr,positions)

            for (i,rect) in enumerate(rects):
                cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(255,0,0))
                cv2.putText(frame,recog_data[i][0]+" ({0})".format(recog_data[i][2])+" - "+str(recog_data[i][1])+"%",(rect[0],rect[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)

                if newValues[1][4] == 'Yes':
                    if newValues[1][5] > 0:
                        newValues[1][5] = round(newValues[1][5] - 0.1, 1)
                    else:
                        newValues[1][4] = 'No'
                else:
                    if (recog_data[i][2] != "Unknown") & (recog_data[i][2] != "Teacher"):
                        if recog_data[i][0] not in peopleAtGym:
                            peopleAtGym[recog_data[i][0]] = lastRow
                            lastRow += 1
                            newValues.append([recog_data[i][0], 1, 'None'])
                        else:
                            pointToEdit = peopleAtGym[recog_data[i][0]]
                            flag = 'None'
                            if newValues[pointToEdit][1] >= 120:
                                flag = 'Yellow'
                            elif newValues[pointToEdit][1] >= 360:
                                flag = 'Orange'
                            elif newValues[pointToEdit][1] >= 480:
                                flag = 'Red'
                            newValues[pointToEdit] = [recog_data[i][0], round(newValues[pointToEdit][1]+0.1, 1), flag]
                    elif recog_data[i][2] == "Teacher":
                        newValues[1][4] = 'Yes'
                        newValues[1][5] = 600



        cv2.imshow("Live Footage",frame)
        cv2.moveWindow("Live Footage", 90, 70)
        key = cv2.waitKey(1) & 0xFF
        writer = csv.writer(open('{}/current.csv'.format(BASE_DIR), 'w'))
        writer.writerows(newValues)
        if key == ord("q"):
            break


def findPeople(features_arr, positions, thres = 0.6, percent_thres = 70):

    f = open('{}/facerec_128D.txt'.format(BASE_DIR),'r')
    data_set = json.loads(f.read())
    returnRes = []
    for (i, features_128D) in enumerate(features_arr):
        result = "Unknown"
        profession = "Unknown"
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][1][positions[i]]
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data-features_128D)))
                if distance < smallest:
                    smallest = distance
                    result = person
        percentage = min(100, 100 * thres / smallest)
        if percentage <= percent_thres:
            result = "Unknown"
        if result != "Unknown":
            profession = data_set[result][0]
        returnRes.append((result, percentage, profession))

    return returnRes    


def create_manual_data(profession, new_name):
    vs = cv2.VideoCapture(0)
    cv2.namedWindow("get focus", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("get focus", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("get focus", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    subprocess.call(["/usr/bin/osascript", "-e", 'tell app "Finder" to set frontmost of process "Python" to true'])
    cv2.destroyWindow("get focus")
    cv2.namedWindow("Add new user")
    cv2.moveWindow("Add new user", 192, 295)
    f = open('{}/facerec_128D.txt'.format(BASE_DIR), 'r')
    data_set = json.loads(f.read())
    person_imgs = {"Left" : [], "Right": [], "Center": []}
    person_features = {"Left" : [], "Right": [], "Center": []}
    print("Please start turning slowly. Press 'q' to save and add this new user to the dataset")
    while True:
        _, frame = vs.read()
        rects, landmarks = face_detect.detect_face(frame, 80)
        for (i, rect) in enumerate(rects):
            aligned_frame, pos = aligner.align(160, frame, landmarks[:, i])
            if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                person_imgs[pos].append(aligned_frame)
                cv2.imshow("Add new user", cv2.resize(aligned_frame, (350, 350)))
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    for pos in person_imgs:
        person_features[pos] = [np.mean(extract_feature.get_features(person_imgs[pos]),axis=0).tolist()]
    data_set[new_name] = [profession, person_features]
    f = open('{}/facerec_128D.txt'.format(BASE_DIR), 'w')
    f.write(json.dumps(data_set))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, help="Run camera recognition", default="camera")
    parser.add_argument("--profession", type=str)
    parser.add_argument("--name", type=str)
    args = parser.parse_args(sys.argv[1:])
    FRGraph = FaceRecGraph()
    MTCNNGraph = FaceRecGraph()
    aligner = AlignCustom()
    extract_feature = FaceFeature(FRGraph)
    face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2)
    main(args)
