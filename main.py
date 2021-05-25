import cv2
import numpy as np
import glob
import time

for img in glob.glob("Images/Samples/*.BMP"):

    frame = cv2.imread(img,0)
    #rotate_frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame_copy = frame.copy()

    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    current_val = 0
    current_loc = []
    current_string = ''
    region1 = frame[218:387, 0:162]
    region2 = frame[218:387, 162:326]
    region3 = frame[218:387, 326:477]
    region4 = frame[218:387, 477:638]

    for A in glob.glob("Images/A_Template/*.jpg"):
        template_A = cv2.imread(A,0)
        #template_A = cv2.rotate(template_A, cv2.ROTATE_180)
        h_A, w_A = template_A.shape

        result_A_R1 = cv2.matchTemplate(region1, template_A, cv2.TM_CCOEFF_NORMED)

        min_val_A, max_val_A, min_loc_A, max_loc_A = cv2.minMaxLoc(result_A_R1)
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #     location_A = min_loc_A
        # else:
        if max_val_A > current_val:
            current_loc = max_loc_A
            current_val = max_val_A
            current_string = 'A'
        #bottom_right_A = (location_A[0] + w_A, location_A[1] + h_A)

    for B in glob.glob("Images/B_Template/*.jpg"):
        template_B = cv2.imread(B, 0)
        #template_B_bin = cv2.inRange(template_B, 0, 60)
        #template_B = cv2.rotate(template_B, cv2.ROTATE_180)

        h_B, w_B = template_B.shape
        result_B = cv2.matchTemplate(region1, template_B, cv2.TM_CCOEFF_NORMED)

        min_val_B, max_val_B, min_loc_B, max_loc_B = cv2.minMaxLoc(result_B)
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #     location_B = min_loc_B
        # else:

        if max_val_B > current_val:
            current_loc = max_loc_B
            current_val = max_val_B
            current_string = 'B'

        #bottom_right_B = (location_B[0] + w_B, location_B[1] + h_B)

    # if current_val_A > current_val_B:
    #     current_loc = location_A
    #     bottom_right = bottom_right_A
    #     current_string = 'A'
    # else:
    #     current_loc = location_B
    #     bottom_right = bottom_right_B
    #     current_string = 'B'

    cv2.rectangle(frame_copy, (0,218), (162,387), 255, 2)
    cv2.rectangle(frame_copy, (162, 218), (326, 387), 255, 2)
    cv2.rectangle(frame_copy, (326, 218), (477, 387), 255, 2)
    cv2.rectangle(frame_copy, (477, 218), (638, 387), 255, 2)

    cv2.putText(frame_copy, current_string, (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2);
    cv2.putText(frame_copy, current_string, (182, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2);
    cv2.putText(frame_copy, current_string, (346, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2);
    cv2.putText(frame_copy, current_string, (497, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2);
    print(current_loc, current_string, current_val)

    cv2.imshow('Region1', result_B)
    cv2.imshow('Match', frame_copy)


    time.sleep(1)
    key = cv2.waitKey(1)
    if key == 32:
        cv2.waitKey()
    elif key == ord('q'):
        break
