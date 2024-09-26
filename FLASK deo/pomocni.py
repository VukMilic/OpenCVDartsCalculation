from main_function import dart_points_clock
import cv2


points = dart_points_clock('uploads/bull.jpg', 92, 105, 24, 35)

print(f'Result is: {points}')

cv2.waitKey(0)
cv2.destroyAllWindows()
