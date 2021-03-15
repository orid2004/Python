import cv2 as cv

# capture = cv.VideoCapture("./opencv-course/Resources/Videos/dog.mp4")
capture = cv.VideoCapture(0)  # start webcam
last = 0  # last number of white dots


def abs(x):
    return x * (-1) if x < 0 else x


cv.namedWindow("Video")  # set window
cv.moveWindow("Video", 500, 200)  # place window
while True:
    # ------ LOAD NEXT FRAME FROM VIDEO -------
    frame_status, frame = capture.read()  # video current frame

    # ------- DETECT MOTION -------
    canny = cv.Canny(frame, 125, 175)  # black & white dots
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # contours --> count white dots
    contours, _ = cv.findContours(
        canny,
        cv.RETR_LIST,
        cv.CHAIN_APPROX_SIMPLE
    )
    current = len(contours)  # current white dots
    if last and abs(last - current) > 30:
        # if change of 30 dots (+30 or -30)
        print("Motion Detected! {}".format(abs(last - current)))  # print
        print('\a')  # beep
    last = current  # set last to current

    # -------- PLAY VIDEO -------
    if frame_status:
        cv.imshow("Video", frame)  # show frame
    else:
        # if video stops
        break
    if cv.waitKey(20) & 0xFF == ord('d'):
        # if 'd' was pressed - stop
        break

    # ----- REPEAT - LOAD NEXT FRAME ------

capture.release()
cv.destroyAllWindows()
