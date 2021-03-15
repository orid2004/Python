import cv2 as cv


def rescale_frame(frame, scale):
    # we can use the property shape
    # frame.shape[1] ---> width
    # frame.shape[0] ---> height
    new_width = int(frame.shape[1] * scale)
    new_height = int(frame.shape[0] * scale)
    # we use a tuple to store the dimensions
    dimensions = (new_width, new_height)

    return cv.resize(frame, dimensions)


cat_img = cv.imread("./opencv-course/Resources/Photos/cat.jpg")
cv.imshow("Cat Frame", rescale_frame(cat_img, .75))
cv.waitKey(0)
