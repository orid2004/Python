# import the opencv2 module
import cv2 as cv

# crate a cv-image object and load cat.jpg
cat_img = cv.imread("./opencv-course/Resources/Photos/cat.jpg")

# show the image under "Cat" window
# cv.imshow("Cat", cat_img)

# create a capture object
# 0 stands for webcam
# we can use path to open a video

capture = cv.VideoCapture("./opencv-course/Resources/Videos/dog.mp4")
while True:
    # read() reads frame by frame
    # read() returns the frame, and frame_status (bool)
    frame_status, frame = capture.read()
    # display the frame
    if frame_status:
        cv.imshow("Video", frame)
    else:
        # stop show if video ends
        break
    # wait for a 'D' press to stop to shoe
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()

# waitKet(0)
cv.waitKey(0)
