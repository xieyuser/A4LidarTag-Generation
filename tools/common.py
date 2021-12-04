import os
import os.path as osp
import numpy as np
import cv2
import math as M
from shapely.geometry import Polygon

def to_gray(img):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    return img.astype('u1')

def ham_dis(c, binary):
    return sum(el1 != el2 for el1, el2 in zip(c, binary))

def blob_detector(config, img):
    imgray = to_gray(img)
    gray = cv2.medianBlur(imgray, 3)
    gray = cv2.erode(gray, np.ones((5, 5), np.uint8),iterations = 1)
    gray = cv2.dilate(gray, kernel=np.ones((5, 5), np.uint8))

    _, w = gray.shape[:2]

    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.filterByArea = config.enable_filterby_gray
    params.minThreshold = config.min_gray_thresh
    params.maxThreshold = config.max_gray_thresh

    # Filter by Area.
    params.filterByArea = config.enable_filterby_area
    params.minArea = 3.14* config.min_r **2
    params.maxArea = 3.14* config.max_r **2

    # Filter by Circularity
    params.filterByCircularity = config.enable_filterby_circularity
    params.minCircularity = config.min_circularity
    params.maxCircularity = config.max_circularity

    # Filter by Convexity
    params.filterByConvexity = config.enable_filterby_convexity
    params.minConvexity = config.min_convexity
    params.maxConvexity = config.max_convexity

    # Filter by Inertia
    params.filterByInertia = config.enable_filterby_inertiaradio
    params.minInertiaRatio = config.min_inertiaradio
    params.maxInertiaRatio = config.max_inertiaradio

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(gray)
    info = []
    for kp in keypoints:
        (x, y) = kp.pt
        r = kp.size
        info.append([x, y, r])
    result = np.array(info)
    return result

def read_video(path):
    capture = cv2.VideoCapture(path)
    imgs = []
    if capture.isOpened():
        while True:
            ret,img=capture.read()
            if not ret:break
            imgs.append(img)
    return imgs

def video_write(path, frames):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    h, w = frames[0].shape[:2]
    out = cv2.VideoWriter(path, fourcc, 20.0, (w,h),True)
    for frame in frames:
        out.write(frame)
    print(f'saved to {path}')

def path_to_name(im_p):
    # return im_p.split('/')[-1]
    return osp.basename(im_p)

def get_corners(p):
    p_result = convex_hull(p)
    corners = []
    for i, p in enumerate(p_result):
        p1 = p_result[i-1]
        p = p_result[i]
        if i+1 == len(p_result):
            p2 = p_result[0]
        else:
            p2 = p_result[i+1]

        theta = angle_of_vector([p[0]-p1[0], p[1]-p1[1]], [p[0]-p2[0], p[1]-p2[1]])
        if theta<170:
            corners.append(p)
    corners = np.array(corners)
    return corners

def convex_hull(ps):
    p = Polygon(ps)
    x = p.convex_hull
    a, b = x.exterior.coords.xy
    re = list(zip(a,b))
    assert re[0]==re[-1]
    return re[1:]

def angle_of_vector(v1, v2):
    vector_prod = v1[0] * v2[0] + v1[1] * v2[1]
    length_prod = M.sqrt(pow(v1[0], 2) + pow(v1[1], 2)) * M.sqrt(pow(v2[0], 2) + pow(v2[1], 2))
    cos = vector_prod * 1.0 / (length_prod * 1.0 + 1e-6)
    return (M.acos(cos) / M.pi) * 180

def calc_distance(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return M.sqrt(x**2 + y**2)

