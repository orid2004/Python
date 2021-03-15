import cv2 as cv

cat_img = cv.imread("./opencv-course/Resources/Photos/cat.jpg")
cv.imshow("img", cat_img)


# Rotate
def rotate(frame, angle):
    height, width = frame.shape[:2]
    # set rotation point to mid
    rotPoint = (width // 2, height // 2)
    # create the base matrix rotated
    rotMatrix = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    # create the matrix dimensions
    dimensions = (width, height)
    # place the frame on the rotated matrix
    rotFrame = cv.warpAffine(frame, rotMatrix, dimensions)

    return rotFrame


# Resize
def resize(frame, shape):
    return cv.resize(frame, shape, interpolation=cv.INTER_CUBIC)


# Flipping
def flip_y_axis_mirror(frame):
    # Negative value --> flip on Y axis
    # Mirror
    return cv.flip(frame, -1)


def flip_y_axis_spin(frame):
    # 0 value --> flip on Y axis
    # Spin 180
    return cv.flip(frame, 0)


def flip_x_axis(frame):
    # Positive value --> flip on X axis
    return cv.flip(frame, 1)


cv.imshow("img", flip_x_axis(cat_img))

cv.waitKey(0)
