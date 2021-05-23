import cv2
import numpy as np
import glob
import time

for img in glob.glob("Images/*.BMP"):

    frame = cv2.imread(img, 0)
    rotate_frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame_copy = rotate_frame.copy()

    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    current_val_A = 0
    current_val_B = 0
    current_loc = 0
    bottom_right = 0
    current_string = ''
    region1 = rotate_frame[100:280, 0:200]
    region1_bin = cv2.inRange(region1, 0, 60)
    region2 = rotate_frame[50:300, 180:330]
    region3 = rotate_frame[50:300, 320:460]
    region4 = rotate_frame[50:300, 460:640]
    cv2.arrowedLine(frame_copy, (460, 100), (640, 280), (220, 170, 0), 2)

    for A in glob.glob("Images/Templates/A/*.jpg"):
        template_A = cv2.imread(A, 0)
        template_A = cv2.rotate(template_A, cv2.ROTATE_180)
        h_A, w_A = template_A.shape

        result_A_R1 = cv2.matchTemplate(region1, template_A, cv2.TM_CCORR_NORMED)
        min_val_A, max_val_A, min_loc_A, max_loc_A = cv2.minMaxLoc(result_A_R1)
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #     location_A = min_loc_A
        # else:
        if max_val_A > current_val_A:
            location_A = max_loc_A
            current_val_A = max_val_A
        bottom_right_A = (location_A[0] + w_A, location_A[1] + h_A)

    for B in glob.glob("Images/Templates/B/*.jpg"):
        template_B = cv2.imread(B, 0)
        template_B_bin = cv2.inRange(template_B, 0, 60)
        template_B = cv2.rotate(template_B, cv2.ROTATE_180)

        h_B, w_B = template_B.shape
        frame_copy = rotate_frame.copy()
        result_B = cv2.matchTemplate(region1, template_B, cv2.TM_CCORR_NORMED)
        min_val_B, max_val_B, min_loc_B, max_loc_B = cv2.minMaxLoc(result_B)
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #     location_B = min_loc_B
        # else:

        if max_val_B > current_val_B:
            location_B = max_loc_B
            current_val_B = max_val_B

        bottom_right_B = (location_B[0] + w_B, location_B[1] + h_B)

    if current_val_A > current_val_B:
        current_loc = location_A
        bottom_right = bottom_right_A
        current_string = 'A'
    else:
        current_loc = location_B
        bottom_right = bottom_right_B
        current_string = 'B'

    cv2.rectangle(region1, current_loc, bottom_right, 255, 5)
    cv2.putText(region1, current_string, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (35, 100, 150), 2)
    print(current_loc, current_string, max_val_B)
    cv2.imshow("region 1", region1)

    cv2.imshow('Match', frame_copy)

    # cv2.imshow('Sample', rotate_frame)

    # time.sleep(0.5)
    key = cv2.waitKey(1)
    if key == 32:
        cv2.waitKey()
    elif key == ord('q'):
        break
