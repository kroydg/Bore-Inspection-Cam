import cv2
import numpy as np
import glob
import time


def findpattern(region):
    current_val = 0
    current_loc = []
    current_string = ''

    current_result = []

    for A in glob.glob("Images/A_Template/*.jpg"):
        template_A = cv2.imread(A)
        template_A = cv2.cvtColor(template_A, cv2.COLOR_BGR2GRAY)

        result_A = cv2.matchTemplate(region, template_A, cv2.TM_CCOEFF_NORMED)
        min_val_A, max_val_A, min_loc_A, max_loc_A = cv2.minMaxLoc(result_A)

        if max_val_A > current_val:
            current_loc = max_loc_A
            current_val = max_val_A
            current_string = 'A'
            current_result = result_A
            h, w = template_A.shape
        # bottom_right_A = (location_A[0] + w_A, location_A[1] + h_A)

    for B in glob.glob("Images/B_Template/*.jpg"):
        template_B = cv2.imread(B)
        template_B = cv2.cvtColor(template_B, cv2.COLOR_BGR2GRAY)

        result_B = cv2.matchTemplate(region, template_B, cv2.TM_CCOEFF_NORMED)
        min_val_B, max_val_B, min_loc_B, max_loc_B = cv2.minMaxLoc(result_B)

        if max_val_B > current_val:
            current_loc = max_loc_B
            current_val = max_val_B
            current_string = 'B'
            current_result = result_B
            h, w = template_B.shape

    return current_val, current_loc, current_string, current_result, h, w


for img in glob.glob("Images/Samples/*.BMP"):

    frame = cv2.imread(img)
    frame_copy = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    WHITE = (255, 255, 255)
    # methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    # Define 4 search regions
    region1 = frame[218:387, 0:162]
    region2 = frame[218:387, 162:326]
    region3 = frame[218:387, 326:477]
    region4 = frame[218:387, 477:638]

    cv2.rectangle(frame_copy, (0, 218), (162, 387), 255, 2)
    cv2.rectangle(frame_copy, (162, 218), (326, 387), 255, 2)
    cv2.rectangle(frame_copy, (326, 218), (477, 387), 255, 2)
    cv2.rectangle(frame_copy, (477, 218), (638, 387), 255, 2)

    # Search within the 4 defined regions using defined function
    current_val_r1, current_loc_r1, current_string_r1, current_result_r1, h1, w1 = findpattern(region1)
    current_val_r2, current_loc_r2, current_string_r2, current_result_r2, h2, w2 = findpattern(region2)
    current_val_r3, current_loc_r3, current_string_r3, current_result_r3, h3, w3 = findpattern(region3)
    current_val_r4, current_loc_r4, current_string_r4, current_result_r4, h4, w4 = findpattern(region4)

    # Display result and score
    cv2.putText(frame_copy, 'Matched Str = %s' % current_string_r1, (5, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    cv2.putText(frame_copy, 'Matched Str = %s' % current_string_r2, (167, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    cv2.putText(frame_copy, 'Matched Str = %s' % current_string_r3, (331, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    cv2.putText(frame_copy, 'Matched Str = %s' % current_string_r4, (490, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)

    cv2.putText(frame_copy, 'Confidence = %.1f' % (current_val_r1 * 100), (5, 170), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, WHITE, 1)
    cv2.putText(frame_copy, 'Confidence = %.1f' % (current_val_r2 * 100), (167, 170), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, WHITE, 1)
    cv2.putText(frame_copy, 'Confidence = %.1f' % (current_val_r3 * 100), (331, 170), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, WHITE, 1)
    cv2.putText(frame_copy, 'Confidence = %.1f' % (current_val_r4 * 100), (490, 170), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, WHITE, 1)

    cv2.putText(frame_copy, 'Current Image: %s' % img, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)

    # Show letter positions
    cv2.rectangle(frame_copy, (current_loc_r1[0], current_loc_r1[1] + 218),
                  (current_loc_r1[0] + w1, current_loc_r1[1] + h1 + 218), (0, 255, 0), 2)
    cv2.rectangle(frame_copy, (current_loc_r2[0] + 162, current_loc_r2[1] + 218),
                  (current_loc_r2[0] + 162 + w2, current_loc_r2[1] + h2 + 218), (0, 255, 0), 2)
    cv2.rectangle(frame_copy, (current_loc_r3[0] + 326, current_loc_r3[1] + 218),
                  (current_loc_r3[0] + 326 + w3, current_loc_r3[1] + h3 + 218), (0, 255, 0), 2)
    cv2.rectangle(frame_copy, (current_loc_r4[0] + 477, current_loc_r4[1] + 218),
                  (current_loc_r4[0] + 477 + w4, current_loc_r4[1] + h4 + 218), (0, 255, 0), 2)

    cv2.imshow('Region1', current_result_r1)
    cv2.imshow('Region2', current_result_r2)
    cv2.imshow('Region3', current_result_r3)
    cv2.imshow('Region4', current_result_r4)
    cv2.imshow('Matching Result', frame_copy)
    #cv2.imwrite('Example_Result.jpg', frame_copy)
    cv2.moveWindow('Region 4', 340, 300)


    print(img)
    print(current_string_r1, current_string_r2, current_string_r3, current_string_r4)

    time.sleep(1)
    key = cv2.waitKey(1)
    if key == 32:
        cv2.waitKey()
    elif key == ord('q'):
        break
