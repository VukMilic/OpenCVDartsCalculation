import cv2
import numpy as np
from contours import find_center
from colors import getCentersOfColors
from dartcalc import find_nearest_point
from dartcalc import find_farthest_point
from dartcalc import findTipOfDartWithoutYellow
from dartcalc import findTipOfDart
from contours import crop_img_to_quarter
from contours import find_circles_red
from contours import find_circles_green
from contours import find_the_lines_angles_points
from contours import calculate_points
from contours import find_points_multiplicator

def dart_points(image_path, tip_color_down, tip_color_up, flight_color_down, flight_color_up):
    img = cv2.imread(image_path)

    debug_mode = 0

    green_or_red = 'green'

    # img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    if img.shape[1] > img.shape[0]:
        width = 1000
        height = int(width * img.shape[0] / img.shape[1])
        img = cv2.resize(img, (width, height))
    else:
        height = 800
        width = int(height * img.shape[1] / img.shape[0])
        img = cv2.resize(img, (width, height))

    # first: find center
    center, cropped_img, radius = find_center(img, green_or_red)

    # Display the results
    if debug_mode == 1:
        print(f"Center: {center}")
        print(f"Radius: {radius}")
        cv2.imshow('Cropped Image', cropped_img)

    # light blue HSV
    blueCenters, blueContours = getCentersOfColors(cropped_img, [tip_color_down, 80, 80], [tip_color_up, 255, 255])
    # yellow HSV
    yellowCenter, yellowContours = getCentersOfColors(cropped_img, [flight_color_down, 80, 80], [flight_color_up, 255, 255])

    if len(yellowCenter) > 1:
        # if there are more than one yellow mask, take the biggest one and find the center
        largest_contour = max(yellowContours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        yellowCenter.clear()
        yellowCenter.append([int(x + w / 2), int(y + h / 2)])

    if len(blueCenters) > 3:
        # if there are more than three blue masks, take the three biggest and find their centers
        sorted_contours = sorted(blueContours, key=cv2.contourArea, reverse=True)
        largest_contours = sorted_contours[:3]
        blueCenters.clear()
        for contour in largest_contours:
            hull = cv2.convexHull(contour)

            if len(yellowCenter) == 0:
                # find the nearest point of every contour (nearest to the center)
                center = ([center[0], center[1]])
                point = find_nearest_point(hull, center)
            else:
                # find the farthest point of every contour (farthest of the yellow center)
                point = find_farthest_point(hull, yellowCenter)

            blueCenters.append([int(point[0][0]), int(point[0][1])])
    else:
        blueCenters.clear()
        for contour in blueContours:
            hull = cv2.convexHull(contour)

            if len(yellowCenter) == 0:
                # find the nearest point of every contour (nearest to the center)
                center = ([center[0], center[1]])
                point = find_nearest_point(hull, center)
            else:
                # find the farthest point of every contour (farthest of the yellow center)
                point = find_farthest_point(hull, yellowCenter)

            blueCenters.append([int(point[0][0]), int(point[0][1])])

    # check if the yellow mask is outside the dartboard
    if len(yellowCenter) == 0:
        tip_x, tip_y = findTipOfDartWithoutYellow(blueCenters, radius, radius)
    else:
        tip_x, tip_y = findTipOfDart(blueCenters, yellowCenter)

    # print the tip coordinates and draw them on the board
    if debug_mode == 1:
        print(f'{tip_x}, {tip_y}  is tip')
        # cv2.circle(cropped_img, (tip_x, tip_y), 5, (255, 0, 255), 2)
        cv2.imshow('Tabla sa tipom', cropped_img)

    # now I got the center and the tip
    # find in which quarter the tip is
    quarter_img, quarter_corner, new_tip_x, new_tip_y = crop_img_to_quarter(cropped_img, center[0], center[1], tip_x, tip_y)
    if debug_mode == 1:
        print(f"Nove koordinate su: ({new_tip_x}, {new_tip_y})")
        cv2.circle(quarter_img, (new_tip_x, new_tip_y), 1, (255, 0, 0), 2)  
        cv2.imshow('Image Quarter', quarter_img)

    # Sada kada imamo deo gde je pogodak
    # zelim da uzmem najvecu konturu crvene boje.
    # Zatim, uzmi najudaljeniju tacku i najblizu tacku centru na toj konturi
    # i vrati radiuse od obe kruznice sa tih tacaka
    quarter_img_cropped_on_double_in, double_out_radius, double_in_radius, max_double_contour = find_circles_red(quarter_img)
    if debug_mode == 1:
        cv2.imshow('Cropped quarter on double', quarter_img_cropped_on_double_in)
    # Kropovao sam sliku gde sada vise nemam double polja.
    # Sada nadji najvecu crvenu konturu koja ce predstavljati tripple polje
    # Izvuci iz nje najblizu i najdalju tacku i vrati ih kao radiuse
    quarter_img_cropped_on_tripple_in, tripple_out_radius, tripple_in_radius, max_tripple_contour = find_circles_red(quarter_img_cropped_on_double_in)
    if debug_mode == 1:
        cv2.imshow('Cropped quarter on tripple', quarter_img_cropped_on_tripple_in)
    # Sada sam kropovao sliku i nemam vise ni tripple polje
    # Sada nalazimo najvecu konturu ZELENE boje koja predstavlja polu centar
    # Zasto zelena boja sad?
    # Zato sto je veca od crvene, jedina je na toj slici zelena, i maltene ne postoji sansa da bude zaklonjena kao crveni centar na primer
    quarter_img_cropped_on_bull, bull_out_radius, bull_in_radius = find_circles_green(quarter_img_cropped_on_tripple_in)
    if debug_mode == 1:
        cv2.imshow('Cropped quarter on bull', quarter_img_cropped_on_bull)

    # SADA PRIKAZI SLIKU SA KRUGOVIMA
    if debug_mode == 1:
        cv2.circle(quarter_img, (0, 0), int(double_out_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(double_in_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(tripple_out_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(tripple_in_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(bull_out_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(bull_in_radius), (255, 0, 0), 2)  
        cv2.imshow('Quarter Image with All Circles', quarter_img)

    points = 0

    # Nakon sto si nasao kruznice, potrebno je da nadjes i uglove
    # Prvo nadji od najvece konture tacku koja je najbliza 0 po x osi
    # Zatim izracunaj poen - A, B, C, D, E, F (posle prebaci u poene)
    img_with_line, points_letter = find_the_lines_angles_points(quarter_img, double_out_radius, max_double_contour, quarter_corner, new_tip_x, new_tip_y)
    if debug_mode == 1:
        cv2.imshow('Quarter image with line', img_with_line)
        print(f'Poeni u slovima: {points_letter}')

    points_multiplicator = find_points_multiplicator(new_tip_x, new_tip_y, double_out_radius, double_in_radius, tripple_out_radius, tripple_in_radius, bull_out_radius, bull_in_radius)
    if debug_mode == 1:
        print(f'Multiplicator: {points_multiplicator}')

    # CALCULATE POINTS !!!!!!!!!!!!!!!!!!!!!!!
    if points_multiplicator == 50:
        points = 50
    elif points_multiplicator == 25:
        points = 25
    else:
        points = calculate_points(quarter_corner, points_letter, points_multiplicator)

    print(f'******** POINTS: {points} *************')

    return points
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def dart_points_clock(image_path, tip_color_down, tip_color_up, flight_color_down, flight_color_up):
    img = cv2.imread(image_path)

    debug_mode = 0

    green_or_red = 'green'

    # img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    if img.shape[1] > img.shape[0]:
        width = 1000
        height = int(width * img.shape[0] / img.shape[1])
        img = cv2.resize(img, (width, height))
    else:
        height = 800
        width = int(height * img.shape[1] / img.shape[0])
        img = cv2.resize(img, (width, height))

    # first: find center
    center, cropped_img, radius = find_center(img, green_or_red)

    # Display the results
    if debug_mode == 1:
        print(f"Center: {center}")
        print(f"Radius: {radius}")
        cv2.imshow('Cropped Image', cropped_img)

    # light blue HSV
    blueCenters, blueContours = getCentersOfColors(cropped_img, [tip_color_down, 80, 80], [tip_color_up, 255, 255])
    # yellow HSV
    yellowCenter, yellowContours = getCentersOfColors(cropped_img, [flight_color_down, 80, 80], [flight_color_up, 255, 255])

    if len(yellowCenter) > 1:
        # if there are more than one yellow mask, take the biggest one and find the center
        largest_contour = max(yellowContours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        yellowCenter.clear()
        yellowCenter.append([int(x + w / 2), int(y + h / 2)])

    if len(blueCenters) > 3:
        # if there are more than three blue masks, take the three biggest and find their centers
        sorted_contours = sorted(blueContours, key=cv2.contourArea, reverse=True)
        largest_contours = sorted_contours[:3]
        blueCenters.clear()
        for contour in largest_contours:
            hull = cv2.convexHull(contour)

            if len(yellowCenter) == 0:
                # find the nearest point of every contour (nearest to the center)
                center = ([center[0], center[1]])
                point = find_nearest_point(hull, center)
            else:
                # find the farthest point of every contour (farthest of the yellow center)
                point = find_farthest_point(hull, yellowCenter)

            blueCenters.append([int(point[0][0]), int(point[0][1])])
    else:
        blueCenters.clear()
        for contour in blueContours:
            hull = cv2.convexHull(contour)

            if len(yellowCenter) == 0:
                # find the nearest point of every contour (nearest to the center)
                center = ([center[0], center[1]])
                point = find_nearest_point(hull, center)
            else:
                # find the farthest point of every contour (farthest of the yellow center)
                point = find_farthest_point(hull, yellowCenter)

            blueCenters.append([int(point[0][0]), int(point[0][1])])

    # check if the yellow mask is outside the dartboard
    if len(yellowCenter) == 0:
        tip_x, tip_y = findTipOfDartWithoutYellow(blueCenters, radius, radius)
    else:
        tip_x, tip_y = findTipOfDart(blueCenters, yellowCenter)

    # print the tip coordinates and draw them on the board
    if debug_mode == 1:
        print(f'{tip_x}, {tip_y}  is tip')
        cv2.circle(img, (tip_x, tip_y), 5, (255, 0, 255), 2)
        cv2.imshow('Tabla sa tipom', img)

    # now I got the center and the tip
    # find in which quarter the tip is
    quarter_img, quarter_corner, new_tip_x, new_tip_y = crop_img_to_quarter(cropped_img, center[0], center[1], tip_x, tip_y)
    if debug_mode == 1:
        print(f"Nove koordinate su: ({new_tip_x}, {new_tip_y})")
        cv2.circle(quarter_img, (new_tip_x, new_tip_y), 1, (255, 0, 0), 2)  
        cv2.imshow('Image Quarter', quarter_img)

    # Sada kada imamo deo gde je pogodak
    # zelim da uzmem najvecu konturu crvene boje.
    # Zatim, uzmi najudaljeniju tacku i najblizu tacku centru na toj konturi
    # i vrati radiuse od obe kruznice sa tih tacaka
    quarter_img_cropped_on_double_in, double_out_radius, double_in_radius, max_double_contour = find_circles_red(quarter_img)
    if debug_mode == 1:
        cv2.imshow('Cropped quarter on double', quarter_img_cropped_on_double_in)
    # Kropovao sam sliku gde sada vise nemam double polja.
    # Sada nadji najvecu crvenu konturu koja ce predstavljati tripple polje
    # Izvuci iz nje najblizu i najdalju tacku i vrati ih kao radiuse
    quarter_img_cropped_on_tripple_in, tripple_out_radius, tripple_in_radius, max_tripple_contour = find_circles_red(quarter_img_cropped_on_double_in)
    if debug_mode == 1:
        cv2.imshow('Cropped quarter on tripple', quarter_img_cropped_on_tripple_in)
    # Sada sam kropovao sliku i nemam vise ni tripple polje
    # Sada nalazimo najvecu konturu ZELENE boje koja predstavlja polu centar
    # Zasto zelena boja sad?
    # Zato sto je veca od crvene, jedina je na toj slici zelena, i maltene ne postoji sansa da bude zaklonjena kao crveni centar na primer
    quarter_img_cropped_on_bull, bull_out_radius, bull_in_radius = find_circles_green(quarter_img_cropped_on_tripple_in)
    if debug_mode == 1:
        cv2.imshow('Cropped quarter on bull', quarter_img_cropped_on_bull)

    # SADA PRIKAZI SLIKU SA KRUGOVIMA
    if debug_mode == 1:
        cv2.circle(quarter_img, (0, 0), int(double_out_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(double_in_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(tripple_out_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(tripple_in_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(bull_out_radius), (255, 0, 0), 2)  
        cv2.circle(quarter_img, (0, 0), int(bull_in_radius), (255, 0, 0), 2)  
        cv2.imshow('Quarter Image with All Circles', quarter_img)

    points = 0

    # Nakon sto si nasao kruznice, potrebno je da nadjes i uglove
    # Prvo nadji od najvece konture tacku koja je najbliza 0 po x osi
    # Zatim izracunaj poen - A, B, C, D, E, F (posle prebaci u poene)
    img_with_line, points_letter = find_the_lines_angles_points(quarter_img, double_out_radius, max_double_contour, quarter_corner, new_tip_x, new_tip_y)
    if debug_mode == 1:
        cv2.imshow('Quarter image with line', img_with_line)
        print(f'Poeni u slovima: {points_letter}')
    points_multiplicator = find_points_multiplicator(new_tip_x, new_tip_y, double_out_radius, double_in_radius, tripple_out_radius, tripple_in_radius, bull_out_radius, bull_in_radius)
    if debug_mode == 1:
        print(f'Multiplicator: {points_multiplicator}')

    # CALCULATE POINTS !!!!!!!!!!!!!!!!!!!!!!!
    if points_multiplicator == 50 or points_multiplicator == 25:
        points = 0
    else:
        points_multiplicator = 1
        points = calculate_points(quarter_corner, points_letter, points_multiplicator)

    print(f'******** POINTS CLOCK: {points} *************')

    return points

