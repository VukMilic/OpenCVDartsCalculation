import math
import numpy as np
import cv2


def find_farthest_point(hull, dot):
    max_distance = 0
    farthest_point = None

    for point in hull:
        distance = math.sqrt((point[0][0] - dot[0][0]) ** 2 + (point[0][1] - dot[0][1]) ** 2)
        if distance > max_distance:
            max_distance = distance
            farthest_point = point

    return farthest_point


def find_nearest_point(hull, dot):
    min_distance = 0
    nearest_point = None

    for point in hull:
        distance = math.sqrt((point[0][0] - dot[0]) ** 2 + (point[0][1] - dot[1]) ** 2)
        if min_distance == 0:
            min_distance = distance
            nearest_point = point
        elif distance < min_distance:
            min_distance = distance
            nearest_point = point

    return nearest_point


def findTipOfDart(blueCenters, yellowCenters):
    yell_x = yellowCenters[0][0]
    yell_y = yellowCenters[0][1]

    numOfBlues = len(blueCenters)

    if numOfBlues == 0:
        # If there is no blue recognized, return x,y of yellow mask
        return yell_x, yell_y

    elif numOfBlues == 1:
        # If there is only 1 blue mask, I will get the center of that mask
        # From the perspective where we can see only one blue (it is the highest blue on the dart)
        # the tip is in the middle of that mask
        return blueCenters[0][0], blueCenters[0][1]

    elif numOfBlues == 2:
        # If there are 2 blue masks, I will get the center of the lowest mask
        # From the perspective where we can see two blue masks (two of the highest blue on the dart)
        # the tip is in the middle of the lower mask
        distance1 = math.sqrt((yell_x - blueCenters[0][0]) ** 2 + (yell_y - blueCenters[0][1]) ** 2)
        distance2 = math.sqrt((yell_x - blueCenters[1][0]) ** 2 + (yell_y - blueCenters[1][1]) ** 2)

        if distance1 > distance2:
            return blueCenters[0][0], blueCenters[0][1]
        else:
            return blueCenters[1][0], blueCenters[1][1]

    elif numOfBlues == 3:
        # If there are 3 blue masks, I will get the center of the lowest mask
        # TODO: try to find the point on the edge (not the center)
        distance1 = math.sqrt((yell_x - blueCenters[0][0]) ** 2 + (yell_y - blueCenters[0][1]) ** 2)
        distance2 = math.sqrt((yell_x - blueCenters[1][0]) ** 2 + (yell_y - blueCenters[1][1]) ** 2)
        distance3 = math.sqrt((yell_x - blueCenters[2][0]) ** 2 + (yell_y - blueCenters[2][1]) ** 2)
        dist_max = max(distance1, distance2, distance3)

        if dist_max == distance1:
            return blueCenters[0][0], blueCenters[0][1]
        elif dist_max == distance2:
            return blueCenters[1][0], blueCenters[1][1]
        else:
            return blueCenters[2][0], blueCenters[2][1]

    return 0, 0


def findTipOfDartWithoutYellow(blueCenters, w, h):
    numOfBlues = len(blueCenters)

    if numOfBlues == 0:
        return 0, 0

    if numOfBlues == 1:
        return blueCenters[0][0], blueCenters[0][1]

    if numOfBlues == 2:
        # If the number of blue masks are two and there is no yellow:
        # we need to find in what part of the image are those masks
        blue_x = (blueCenters[0][0] + blueCenters[1][0]) / 2
        blue_y = (blueCenters[0][1] + blueCenters[1][1]) / 2

        if blue_x < w / 4:
            # if the blues are in the first fourth of the table horizontally
            # then we get the dot that is the maximum x
            x_max = max(blueCenters[0][0], blueCenters[1][0])
            for bc in blueCenters:
                if bc[0] == x_max:
                    return bc[0], bc[1]
        elif blue_x > (3 * w / 4):
            # if the blues are in the last fourth of the table horizontally
            # then we get the dot that is the minimum x
            x_min = min(blueCenters[0][0], blueCenters[1][0])
            for bc in blueCenters:
                if bc[0] == x_min:
                    return bc[0], bc[1]
        elif blue_y < h / 4:
            # if the blues are in the first fourth of the table vertically
            # then we get the dot that is the maximum y
            y_max = max(blueCenters[0][1], blueCenters[1][1])
            for bc in blueCenters:
                if bc[1] == y_max:
                    return bc[0], bc[1]
        elif blue_y > (3 * h / 4):
            # if the blues are in the last fourth of the table vertically
            # then we get the dot that is the minimum y
            y_min = min(blueCenters[0][1], blueCenters[1][1])
            for bc in blueCenters:
                if bc[1] == y_min:
                    return bc[0], bc[1]

    if numOfBlues == 3:
        # If the number of blue masks are three and there is no yellow:
        # we need to find in what part of the image are those masks
        blue_x = (blueCenters[0][0] + blueCenters[1][0] + blueCenters[2][0]) / 3
        blue_y = (blueCenters[0][1] + blueCenters[1][1] + blueCenters[2][1]) / 3

        if blue_x < w / 4:
            # if the blues are in the first fourth of the table horizontally
            # then we get the dot that is the maximum x
            x_max = max(blueCenters[0][0], blueCenters[1][0], blueCenters[2][0])
            for bc in blueCenters:
                if bc[0] == x_max:
                    return bc[0], bc[1]
        elif blue_x > (3 * w / 4):
            # if the blues are in the last fourth of the table horizontally
            # then we get the dot that is the minimum x
            x_min = min(blueCenters[0][0], blueCenters[1][0], blueCenters[2][0])
            for bc in blueCenters:
                if bc[0] == x_min:
                    return bc[0], bc[1]
        elif blue_y < h / 4:
            # if the blues are in the first fourth of the table vertically
            # then we get the dot that is the maximum y
            y_max = max(blueCenters[0][1], blueCenters[1][1], blueCenters[2][1])
            for bc in blueCenters:
                if bc[1] == y_max:
                    return bc[0], bc[1]
        elif blue_y > (3 * h / 4):
            # if the blues are in the last fourth of the table vertically
            # then we get the dot that is the minimum y
            y_min = min(blueCenters[0][1], blueCenters[1][1], blueCenters[2][1])
            for bc in blueCenters:
                if bc[1] == y_min:
                    return bc[0], bc[1]

    return 0, 0


def calculateMultiplicator(tip_x, tip_y, center_x, center_y, centerForDouble_x, centerForDouble_y, radiusCI, radiusCO, radiusTI, radiusTO, radiusDI, radiusDO):
    distance_tip_center = np.sqrt((tip_x - center_x)**2 + (tip_y - center_y)**2)
    distance_tip_center_double = np.sqrt((tip_x - centerForDouble_x) ** 2 + (tip_y - centerForDouble_y) ** 2)

    multiplicator = 0

    if distance_tip_center < radiusCI:
        return 50
    elif distance_tip_center < radiusCO:
        return 25
    elif distance_tip_center < radiusTI:
        multiplicator = 1
    elif distance_tip_center < radiusTO:
        multiplicator = 3
    elif distance_tip_center_double < radiusDI:
        multiplicator = 1
    elif distance_tip_center_double < radiusDO:
        multiplicator = 2
    else:
        return 0

    return multiplicator


def calculateSinglePoint(tip_x, tip_y, center_x, center_y, tops_x, tops_y):
    tops_line = (tops_x - center_x, tops_y - center_y)
    tip_line = (tip_x - center_x, tip_y - center_y)

    tops_angle = math.atan2(tops_line[1], tops_line[0])
    tip_angle = math.atan2(tip_line[1], tip_line[0])

    angle = math.degrees(tip_angle - tops_angle)

    if angle < 0:
        angle = 360 + angle

    print(f'Angle of the point is {angle}')

    if angle < 9 or angle > 351:
        return 20
    elif angle < 27:
        return 1
    elif angle < 45:
        return 18
    elif angle < 63:
        return 4
    elif angle < 81:
        return 13
    elif angle < 99:
        return 6
    elif angle < 117:
        return 10
    elif angle < 135:
        return 15
    elif angle < 153:
        return 2
    elif angle < 171:
        return 17
    elif angle < 189:
        return 3
    elif angle < 207:
        return 19
    elif angle < 225:
        return 7
    elif angle < 243:
        return 16
    elif angle < 261:
        return 8
    elif angle < 279:
        return 11
    elif angle < 297:
        return 14
    elif angle < 315:
        return 9
    elif angle < 333:
        return 12
    elif angle < 351:
        return 5
    else:
        return 0


def calculateDartMesures(yellow_dot, blue_dots, dartboard_virtual):
    # in my case these are the original dimensions:
    # - dartboard     - 34 cm
    # - dart          - 13 cm
    # - yellow->blue1 - 7 cm
    # - blue1->blue2  - 2 cm
    # - blue2->blue3  - 2 cm
    # - blue3->tip    - 2 cm

    dartboard_real = 34
    dart_real = 13
    yb_real = 7
    bb_real = 2
    # 1 * x / 34
    one_cm = 1 * dartboard_virtual / dartboard_real

    dart_virtual = one_cm * dart_real
    yb_virtual = one_cm * yb_real
    bb_virtual = one_cm * bb_real


def crop_image_to_circle(image, center, radius):
    mask = np.zeros_like(image)

    cv2.circle(mask, center, radius, (255, 255, 255), -1)

    masked_image = cv2.bitwise_and(image, mask)

    background = np.zeros_like(image)

    result = cv2.add(masked_image, background)

    return result
