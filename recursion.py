import cv2


def getImage(image_path):
    image = cv2.imread(image_path)
    return image


def processImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, image) = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # I accidentally exported the image sequence of Bad Apple, the original animation I designed this for
    # off by a pixel, so one was cut off, and a single pixel wide black edge was added on the other. This attempts to compensate for that
    # but is not necessary for most images.
    # cv2.rectangle(
    #     image, (0, 0), (image.shape[1]-1, image.shape[0]-1), (255, 255, 255), 1)
    # Bitwise not as it searches for whitespace. I want to fill in blackpsace.
    image = cv2.bitwise_not(image)
    return image


def getDistanceField(processing_image):
    dist = cv2.distanceTransform(
        processing_image, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    return dist


# loop through the find largest circle until size limit is reached
# draw a circle on the searching image to not search in that area. otherwise would only return the largest circle.
def gasketFill(dist, viewing_image, processing_image):
    _, radius, _, center = cv2.minMaxLoc(dist)
    cv2.circle(processing_image, tuple(center), int(radius), (0, 0, 0), -1)
    # drawing the circles on the viewing image requires a radius of 1 or more, as it subtracts one from the calculated radius.
    if radius <= 1:
        return int(radius)
    # its a bit inefficient to do it like this with two seperate images, but it's like this to draw a nicer final result
    # while still having discernable circles. otherwise they overlap too much and it looks much worse.
    cv2.circle(viewing_image, tuple(center), int(radius-1), (0, 0, 0), -1)
    return int(radius)


def drawFrame(index):
    image_path = "Frames/"+str(index).zfill(4)+".jpg"
    image = getImage(image_path)
    processing_image = processImage(image)
    image = processImage(image)
    minRadius = 1
    for x in range(0, 10000):
        dist = getDistanceField(processing_image)
        radius = gasketFill(dist, image, processing_image)
        if radius <= minRadius:
            break
    print(index)
    # Bitwise not undos the previous one to return to the original scheme
    #cv2.imshow("viewer", cv2.bitwise_not(image))
    #cv2.imshow("processing", cv2.bitwise_not(processing_image))
    #cv2.imshow("processing", cv2.bitwise_not(processing_image)+ cv2.bitwise_not(image))
    cv2.imwrite("output/" + str(index).zfill(4) +
                # ".jpg", (image))
                ".jpg", cv2.bitwise_not(image))


# TODO: I could use optional argument variables to improve commandline use. Not necessary at the moment.
frames = 1
offset = 4


for x in range(offset, offset+frames):
    drawFrame(x)

cv2.waitKey(0)
cv2.destroyAllWindows()
