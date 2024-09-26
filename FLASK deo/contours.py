import cv2
import numpy as np
import math

# Function to find the farthest point from a given point
def find_farthest_point(point, points):
    max_distance = 0
    farthest_point = point
    for p in points:
        distance = np.linalg.norm(np.array(point) - np.array(p))
        if distance > max_distance:
            max_distance = distance
            farthest_point = p
    return farthest_point, max_distance

# Find the nearest point from the average center
def find_nearest_point(point, points):
    min_distance = float('inf')
    nearest_point = point
    for p in points:
        distance = np.linalg.norm(np.array(point) - np.array(p))
        if distance < min_distance:
            min_distance = distance
            nearest_point = p
    return nearest_point, min_distance


def find_center(img, green_or_red):

    if green_or_red == 'red':
        # Ako je CRVENA BOJA OSNOVNA
        # Convert the image to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        a_channel = lab[:, :, 1]

        # Apply Gaussian blur to the A channel
        blurred = cv2.GaussianBlur(a_channel, (5, 5), 0)

        # Threshold the A channel to create a mask for red colors
        _, red_mask = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    else:
        # Ako je ZELENA BOJA OSNOVNA
        # Convert the image to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        a_channel = lab[:, :, 1]

        # Apply Gaussian blur to the A channel
        blurred = cv2.GaussianBlur(a_channel, (5, 5), 0)

        # Threshold the A channel to create a mask for red colors
        _, red_mask = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY_INV)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if green_or_red == 'red':
        # Sort contours based on area in descending order and take the top 9
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:9]
    else:
        # Sort contours based on area in descending order and take the top 10 
        # here is different because we have center as biggest contour
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    cv2.drawContours(img, sorted_contours, -1, (0, 255, 0), 1)

    # Function to calculate the center of a contour
    def get_contour_center(contour):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        return (cx, cy)

    # Get the centers of the 9 biggest contours
    centers = [get_contour_center(contour) for contour in sorted_contours]

    # Function to find the farthest point from a given point
    def find_farthest_point(point, points):
        max_distance = 0
        farthest_point = point
        for p in points:
            distance = np.linalg.norm(np.array(point) - np.array(p))
            if distance > max_distance:
                max_distance = distance
                farthest_point = p
        return farthest_point, max_distance

    # Calculate the lengths of the lines between each center and the farthest center
    lines = []
    midpoints = []

    for center in centers:
        farthest_center = find_farthest_point(center, centers)[0]
        distance = np.linalg.norm(np.array(center) - np.array(farthest_center))
        lines.append((center, farthest_center, distance))
        # cv2.line(img, center, farthest_center, (255, 0, 0), 1)  # Draw the line in green

        # Calculate the midpoint of the line
        midpoint = ((center[0] + farthest_center[0]) // 2, (center[1] + farthest_center[1]) // 2)
        midpoints.append(midpoint)

    # Find the shortest line
    shortest_line = min(lines, key=lambda x: x[2])

    # Remove the shortest line from the list
    lines.remove(shortest_line)

    # Recalculate the midpoints of the remaining lines
    remaining_centers = [((line[0][0] + line[1][0]) // 2, (line[0][1] + line[1][1]) // 2) for line in lines]

    # Calculate the median point of the remaining midpoints
    average_center = (int(np.median([p[0] for p in remaining_centers])), int(np.median([p[1] for p in remaining_centers])))
    # Find the farthest point from the average center among the convex hull points

    convex_hulls = [cv2.convexHull(contour) for contour in sorted_contours]
    all_hull_points = [tuple(point[0]) for hull in convex_hulls for point in hull]
    farthest_point, radius = find_farthest_point(average_center, all_hull_points)

    # Crop the image to a circle with the radius
    mask = np.zeros_like(img)
    cv2.circle(mask, average_center, int(radius), (255, 255, 255), -1)
    cropped_image = cv2.bitwise_and(img, mask)

    for center in remaining_centers:
        cv2.circle(cropped_image, center, 1, (255, 255, 255), -1)

    # Draw the average center point on the cropped image
    cv2.circle(cropped_image, average_center, 1, (0, 0, 255), -1)  # Draw the average center in red

    return average_center, cropped_image, radius


def rotate_img(image, deg):

    if deg == 90:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif deg == 180:
        rotated_image = cv2.rotate(image, cv2.ROTATE_180)
    elif deg == 270:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    return rotated_image



def crop_img_to_quarter(cropped_img, center_x, center_y, tip_x, tip_y):
    
    height, width = cropped_img.shape[:2]
    mid_x, mid_y = center_x, center_y
    new_tip_x = tip_x
    new_tip_y = tip_y

    quarter_corner = 'full image'

    # rotate image to the bottom right corner
    # and find new tip coordinates
    if tip_x < mid_x and tip_y < mid_y:
        # Top-left quarter
        quarter_img = cropped_img[0:mid_y, 0:mid_x]
        quarter_corner = 'top-left'
        quarter_img = rotate_img(quarter_img, 180)
        new_tip_x = abs(center_x - tip_x)
        new_tip_y = abs(center_y - tip_y)
    elif tip_x >= mid_x and tip_y < mid_y:
        # Top-right quarter
        quarter_img = cropped_img[0:mid_y, mid_x:width]
        quarter_corner = 'top-right'
        quarter_img = rotate_img(quarter_img, 90)
        new_tip_x = abs(center_y - tip_y)
        new_tip_y = abs(tip_x - center_x)
    elif tip_x < mid_x and tip_y >= mid_y:
        # Bottom-left quarter
        quarter_img = cropped_img[mid_y:height, 0:mid_x]
        quarter_corner = 'bottom-left'
        quarter_img = rotate_img(quarter_img, 270)
        new_tip_x = abs(tip_y - center_y)
        new_tip_y = abs(center_x - tip_x)
    else:
        # Bottom-right quarter
        quarter_img = cropped_img[mid_y:height, mid_x:width]
        quarter_corner = 'bottom-right'
        new_tip_x = abs(tip_x - center_x)
        new_tip_y = abs(tip_y - center_y)

    return quarter_img, quarter_corner, new_tip_x, new_tip_y


# Pronadji krugove crvene boje
def find_circles_red(quarter_img):
    # Convert the image to LAB color space
    lab = cv2.cvtColor(quarter_img, cv2.COLOR_BGR2LAB)
    a_channel = lab[:, :, 1]

    # Apply Gaussian blur to the A channel
    blurred = cv2.GaussianBlur(a_channel, (5, 5), 0)

    # Threshold the A channel to create a mask for red colors
    _, red_mask = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the farthest point from the average center
    farthest_point, farthest_radius = find_farthest_point((0, 0), [tuple(point[0]) for point in largest_contour])

    # Draw a circle with the radius equal to the distance between the average center and the farthest point
    cv2.circle(quarter_img, (0, 0), int(farthest_radius), (255, 0, 0), 2)  # Draw the circle in green

    nearest_point, nearest_radius = find_nearest_point((0, 0), [tuple(point[0]) for point in largest_contour])

    # Draw a circle with the radius equal to the distance between the average center and the nearest point
    cv2.circle(quarter_img, (0, 0), int(nearest_radius), (255, 0, 0), 2)  # Draw the circle in blue
    # cv2.imshow('ajmoo', quarter_img)
    # Crop the image to a circle with the radius
    mask = np.zeros_like(quarter_img)
    cv2.circle(mask, (0, 0), int(nearest_radius), (255, 255, 255), -1)
    cropped_image = cv2.bitwise_and(quarter_img, mask)

    # Draw the average center point on the cropped image
    cv2.circle(cropped_image, (0, 0), 1, (0, 0, 255), -1)

    return cropped_image, farthest_radius, nearest_radius, largest_contour


def find_circles_green(quarter_img):
    # Convert the image to LAB color space
    lab = cv2.cvtColor(quarter_img, cv2.COLOR_BGR2LAB)
    b_channel = lab[:, :, 1]  # Use the B channel for green detection

    # Apply Gaussian blur to the B channel
    blurred = cv2.GaussianBlur(b_channel, (5, 5), 0)

    # Threshold the B channel to create a mask for green colors
    _, green_mask = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the farthest point from the center
    farthest_point, farthest_radius = find_farthest_point((0, 0), [tuple(point[0]) for point in largest_contour])

    # Draw a circle with the radius equal to the distance between the center and the farthest point
    cv2.circle(quarter_img, (0, 0), int(farthest_radius), (0, 255, 0), 2)  # Draw the circle in green

    # Find the nearest point from the center
    nearest_point, nearest_radius = find_nearest_point((0, 0), [tuple(point[0]) for point in largest_contour])

    # Draw a circle with the radius equal to the distance between the center and the nearest point
    cv2.circle(quarter_img, (0, 0), int(nearest_radius), (255, 0, 0), 2)  # Draw the circle in blue

    # Crop the image to a circle with the radius
    mask = np.zeros_like(quarter_img)
    cv2.circle(mask, (0, 0), int(nearest_radius), (255, 255, 255), -1)
    cropped_image = cv2.bitwise_and(quarter_img, mask)

    # Draw the center point on the cropped image
    cv2.circle(cropped_image, (0, 0), 1, (0, 0, 255), -1)

    return cropped_image, farthest_radius, nearest_radius


# Pronadji linije i uglove
def find_the_lines_angles_points(img, length, largest_contour, quarter_corner, new_tip_x, new_tip_y):

    hull = cv2.convexHull(largest_contour)
    lowest_x_hull_point = min(hull, key=lambda point: point[0][0])[0]

    # Calculate the angle of the line from (0,0) to the lowest x-coordinate point
    angle = np.arctan2(lowest_x_hull_point[1], lowest_x_hull_point[0])

    # Calculate the end point of the line with the given length
    end_point = (int(length * np.cos(angle)), int(length * np.sin(angle)))

    cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 1)
    # Draw the line on the image
    cv2.line(img, (0, 0), end_point, (0, 255, 0), 2)  # Draw the line in green

    # Nalazim ugao tipa
    base_line = (0, length)
    tip_line = (new_tip_x, new_tip_y)
    base = math.atan2(base_line[1], base_line[0]) 
    tip = math.atan2(tip_line[1], tip_line[0])
    tip_angle = abs(math.degrees(tip - base)) # OVO JE UGAO TIPA U ODNOSU NA LEVU IVICU !!!
    # Nalazim ugao linije
    line = math.atan2(lowest_x_hull_point[1], lowest_x_hull_point[0])
    line_angle = abs(math.degrees(line - base))

    print(f'Ugao tipa je: {tip_angle}')
    print(f'Ugao linije je: {line_angle}')

    # Sada kada imam oba ugla, racunam poene
    points_letter = ''
    # # TODO: Proveri da li je potrebno da odradis proveru ako je LINIJA = pola 3-ojke
    if (length/4) > lowest_x_hull_point[0]:
        # LINIJA = leva ivica B
        if tip_angle < line_angle:
            points_letter = 'A'
        elif tip_angle < line_angle + 18:
            points_letter = 'B'
        elif tip_angle < line_angle + 36:
            points_letter = 'C'
        elif tip_angle < line_angle + 54:
            points_letter = 'D'
        elif tip_angle < line_angle + 72:
            points_letter = 'E'
        elif tip_angle < line_angle + 81:
            points_letter = 'F'
        else:
            points_letter = 'ERROR: Cannot find angle'
    elif (length/2) > lowest_x_hull_point[0]:
        # LINIJA = leva ivica C
        if tip_angle < line_angle - 18:
            points_letter = 'A'
        elif tip_angle < line_angle:
            points_letter = 'B'
        elif tip_angle < line_angle + 18:
            points_letter = 'C'
        elif tip_angle < line_angle + 36:
            points_letter = 'D'
        elif tip_angle < line_angle + 54:
            points_letter = 'E'
        elif tip_angle < line_angle + 63:
            points_letter = 'F'
        else:
            points_letter = 'ERROR: Cannot find angle'        
    elif (3*length/4) > lowest_x_hull_point[0]:
        # LINIJA = leva ivica D
        if tip_angle < line_angle - 36:
            points_letter = 'A'
        elif tip_angle < line_angle - 18:
            points_letter = 'B'
        elif tip_angle < line_angle:
            points_letter = 'C'
        elif tip_angle < line_angle + 18:
            points_letter = 'D'
        elif tip_angle < line_angle + 36:
            points_letter = 'E'
        elif tip_angle < line_angle + 45:
            points_letter = 'F'
        else:
            points_letter = 'ERROR: Cannot find angle'
    else:
        # LINIJA = leva ivica E
        if tip_angle < line_angle - 54:
            points_letter = 'A'
        elif tip_angle < line_angle - 36:
            points_letter = 'B'
        elif tip_angle < line_angle - 18:
            points_letter = 'C'
        elif tip_angle < line_angle:
            points_letter = 'D'
        elif tip_angle < line_angle + 18:
            points_letter = 'E'
        elif tip_angle < line_angle + 27:
            points_letter = 'F'
        else:
            points_letter = 'ERROR: Cannot find angle'

    # PROVERA GDE SE NALAZE LINIJE NA 18 STEPENI LEVO I DESNO
    
    # angle_left = angle - np.deg2rad(18)
    # angle_right = angle + np.deg2rad(18)

    # # Calculate the end points for the new lines
    # end_point_left = (int(length * np.cos(angle_left)), int(length * np.sin(angle_left)))
    # end_point_right = (int(length * np.cos(angle_right)), int(length * np.sin(angle_right)))

    # # Draw the new lines on the image
    # cv2.line(img, (0, 0), end_point_left, (255, 0, 0), 2)  # Draw the left line in blue
    # cv2.line(img, (0, 0), end_point_right, (255, 0, 0), 2)  # Draw the right line in blue
    # # PROVERA GDE SE NALAZE LINIJE NA CETVRTINAMA
    # height, width = img.shape[:2]

    # cv2.line(img, (int(length/4), 0), (int(length/4), height), (0, 255, 0), 2)  # Draw the line in green
    # cv2.line(img, (int(length/2), 0), (int(length/2), height), (0, 255, 0), 2)  # Draw the line in green
    # cv2.line(img, (int(3*length/4), 0), (int(3*length/4), height), (0, 255, 0), 2)  # Draw the line in green

    return img, points_letter


def find_points_multiplicator(new_tip_x, new_tip_y, double_out_radius, double_in_radius, tripple_out_radius, tripple_in_radius, bull_out_radius, bull_in_radius):
    distance = math.sqrt((new_tip_x)**2 + (new_tip_y)**2)
    print(f'Distance of tip from center = {distance}')

    if distance < bull_in_radius:
        return 50
    elif distance < bull_out_radius:
        return 25
    elif distance < tripple_in_radius:
        return 1
    elif distance < tripple_out_radius:
        return 3
    elif distance < double_in_radius:
        return 1
    elif distance < double_out_radius:
        return 2


def calculate_points(quarter_corner, points_letter, points_multiplicator):
    # Ar, Bg, Cr, Dg, Er, Fg pretoci u poene
    if quarter_corner == 'top-left':
        # 20r, 5g, 12r, 9g, 14r, 11g,
        print(quarter_corner)
        if points_letter == 'A':
            return 20 * points_multiplicator
        elif points_letter == 'B':
            return 5 * points_multiplicator
        elif points_letter == 'C':
            return 12 * points_multiplicator
        elif points_letter == 'D':
            return 9 * points_multiplicator
        elif points_letter == 'E':
            return 14 * points_multiplicator
        elif points_letter == 'F':
            return 11 * points_multiplicator
        else:
            return 0
    elif quarter_corner == 'top-right':
        # 6g, 13r, 4g, 18r, 1g, 20r
        print(quarter_corner)
        if points_letter == 'A':
            return 6 * points_multiplicator
        elif points_letter == 'B':
            return 13 * points_multiplicator
        elif points_letter == 'C':
            return 4 * points_multiplicator
        elif points_letter == 'D':
            return 18 * points_multiplicator
        elif points_letter == 'E':
            return 1 * points_multiplicator
        elif points_letter == 'F':
            return 20 * points_multiplicator
        else:
            return 0
    elif quarter_corner == 'bottom-left':
        # 11g, 8r, 16g, 7r, 19g, 3r
        print(quarter_corner)
        if points_letter == 'A':
            return 11 * points_multiplicator
        elif points_letter == 'B':
            return 8 * points_multiplicator
        elif points_letter == 'C':
            return 16 * points_multiplicator
        elif points_letter == 'D':
            return 7 * points_multiplicator
        elif points_letter == 'E':
            return 19 * points_multiplicator
        elif points_letter == 'F':
            return 3 * points_multiplicator
        else:
            return 0
    elif quarter_corner == 'bottom-right':
        # 3r, 17g, 2r, 15g, 10r, 6g
        print(quarter_corner)
        if points_letter == 'A':
            return 3 * points_multiplicator
        elif points_letter == 'B':
            return 17 * points_multiplicator
        elif points_letter == 'C':
            return 2 * points_multiplicator
        elif points_letter == 'D':
            return 15 * points_multiplicator
        elif points_letter == 'E':
            return 10 * points_multiplicator
        elif points_letter == 'F':
            return 6 * points_multiplicator
        else:
            return 0
    else:
        return 0
