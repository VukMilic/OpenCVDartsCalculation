import cv2
import numpy as np

def maskTheColorLAB(img, color):
    if color == 'green':
        # ZELENA MASKA !!!!!!!!!!!!!!!!!!!!!!!! (LAB)

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        a_channel = lab[:, :, 1]
        # cv2.imshow('LAB image 1', a_channel)

        blurred = cv2.GaussianBlur(a_channel, (5, 5), 0)

        # Threshold the A channel to create a mask for green colors
        # Use a lower threshold value to capture green (negative values in A channel)
        _, green_mask = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY_INV)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

        # Apply the mask to the original BGR image
        masked = cv2.bitwise_and(img, img, mask=green_mask)

        # Display the result
        # cv2.imshow('Green Masked Image', masked)
        # cv2.imshow('Green Mask', green_mask)
    elif color == 'red':
        # CRVENA MASKA !!!!!!!!!!!!!!!!!!!!!!!!! (LAB)

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        a_channel = lab[:, :, 1]
        blurred = cv2.GaussianBlur(a_channel, (5, 5), 0)
        # Threshold the A channel to create a mask for red colors
        _, red_mask = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

        # Apply the mask to the original BGR image
        masked = cv2.bitwise_and(img, img, mask=red_mask)

        # Display the result
        # cv2.imshow('Red Masked Image', masked)
        # cv2.imshow('Red Mask', red_mask)
        
    elif color == 'blue':
        # PLAVA MASKA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (LAB)

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        b_channel = lab[:, :, 2]

        # Display the B channel
        # cv2.imshow('LAB image B channel', b_channel)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(b_channel, (5, 5), 0)

        # Threshold the B channel to create a mask for blue colors
        # Use a lower threshold value to capture blue (negative values in B channel)
        _, blue_mask = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY_INV)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

        # Apply the mask to the original BGR image
        masked = cv2.bitwise_and(img, img, mask=blue_mask)

        # Display the result
        # cv2.imshow('Blue Masked Image', masked)
        # cv2.imshow('Blue Mask', blue_mask)
    elif color == 'yellow':
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        # Extract the B channel
        b_channel = lab[:, :, 2]

        # Display the B channel
        # cv2.imshow('LAB image B channel', b_channel)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(b_channel, (5, 5), 0)

        # Threshold the B channel to create a mask for yellow colors
        # Use a higher threshold value to capture yellow (positive values in B channel)
        _, yellow_mask = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)

        # Apply the mask to the original BGR image
        masked = cv2.bitwise_and(img, img, mask=yellow_mask)

        # Display the result
        # cv2.imshow('Yellow Masked Image', masked)
        # cv2.imshow('Yellow Mask', yellow_mask)


def getCentersOfColors(img, HSV1, HSV2):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_color = np.array(HSV1)
    upper_color = np.array(HSV2)

    # Create a mask
    light_blue_mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((3, 3), np.uint8)
    light_blue_mask = cv2.morphologyEx(light_blue_mask, cv2.MORPH_CLOSE, kernel)
    light_blue_mask = cv2.morphologyEx(light_blue_mask, cv2.MORPH_OPEN, kernel)

    # find contours around those colors
    contours, hierarchy = cv2.findContours(light_blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    blank_image = np.zeros_like(light_blue_mask)
    cv2.drawContours(blank_image, contours, -1, (255, 0, 0), 1)

    # Return centers of those contours
    centers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        centers.append([int(x + w/2), int(y + h/2)])
        print(f'{x + w/2}, {y + h/2}  yellow')
        # draw a circle to see where center is
        # cv2.circle(blank_image, (int(x+w/2), int(y+h/2)), 3, (255, 0, 0), 2)

    # U slucaju DEBUG-a ukljuci ovu liniju da bi video gde je kontura
    # cv2.imshow('Colors', blank_image)

    return centers, contours
