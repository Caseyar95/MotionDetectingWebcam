import cv2, time, pandas
from datetime import datetime

firstFrame = None
statusList = [None, None]
times = []
contourCount = []
frameCount = []
avgContour = []
contCStart = 0 #indicator to start recording contour area

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
df = pandas.DataFrame(columns=["Start","End"])

while True:
    check, frame = video.read()
    status = 0
    # turning gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    #catch first frame for later comparisons
    if firstFrame is None:
        firstFrame = gray
        continue

    delta = cv2.absdiff(firstFrame, gray)

    #finding areas of movement and turning them to black/white
    # then finding contours for the movement
    threshFrame = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    threshFrame = cv2.dilate(threshFrame, None, iterations=2)
    (cnts,_) = cv2.findContours(threshFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #if contour area >5000 put a rectangle around it and excecute rest
    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            if contCStart == 1: #if first movement already detected
                contourCount.append(0)
            continue

        status = 1
        contCStart = 1
        contourCount.append(cv2.contourArea(contour))
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    statusList.append(status)
    statusList = statusList[-2:] #only keep track of part of list we need

    #record time something exits/enters frame, and size on exit
    if statusList[-1] == 1 and statusList[-2] == 0:
        times.append(datetime.now())
    if statusList[-1] == 0 and statusList[-2] == 1:
        times.append(datetime.now())
        times.append(cv2.contourArea(contour))

    #showing gray, delta, black/white, and rectangle on orig
    cv2.imshow("Capturing", gray)
    cv2.imshow("Delta", delta)
    cv2.imshow("Threshold", threshFrame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(100)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
            times.append(cv2.contourArea(contour))
        break
################# end while loop ###############

#add times to data frame
for i in range(0, len(times), 3):
    df = df.append({"Start":times[i], "End":times[i+1], "ExitArea":times[i+2]}, ignore_index=True)

df.to_csv("Times.csv")

z = 0
x = 0
y = 0
count = 1
# averaging contours together to smooth graph
while x < len(contourCount):
    while z < x+10:
        if z < len(contourCount):
            y = contourCount[z] + y
            z = z + 1
            count = count + 1
        else:
            z = x + 50

    avgContour.append(float(int(y/count)^2)) #squared to accentuate changes
    #avgContour.append((y/count))
    y = 0
    x = x + 10
    z = z + 1
    count = 1

i = 0
# count for x-axis on plot
while i < len(avgContour):
    frameCount.append(i)
    i = i + 1

video.release()
cv2.destroyAllWindows()
