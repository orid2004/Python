import cv2 as cv

cat_img = cv.imread("./opencv-course/Resources/Photos/cat.jpg")
cv.imshow("img", cat_img)

gray =cv.cvtColor(cat_img, cv.COLOR_BGR2GRAY)
cv.imshow("gray_img", gray)

canny = cv.Canny(cat_img, 125, 175)
cv.imshow("canny_img", canny)

contours, h = cv.findContours(canny,
                              cv.RETR_LIST,
                              cv.CHAIN_APPROX_NONE
                              )

contours2, _ = cv.findContours(canny,
                              cv.RETR_LIST,
                              cv.CHAIN_APPROX_SIMPLE
                              )
print(len(contours))
print(len(contours2))

cv.waitKey(0)
