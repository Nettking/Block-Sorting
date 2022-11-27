import urllib.request
import numpy as np
import cv2

# gray scale values found by trail and error
camera1_threshold = 175
camera2_threshold = 100


def get_image(ip):
    req = urllib.request.urlopen(f'http://{ip}/LiveImage.jpg')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)


    return img


def draw_squares(img, thresholded_image, border=False, name=False, center_dot=False, threshold_dot=False, dbug_print=False):
    contours, hierarchy = cv2.findContours(thresholded_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:    # Square is a polygon with 4 sides
            x, y, w, h = cv2.boundingRect(cnt)

            if w < 25 or h < 25:
                continue
            """
            # For advanced debugging
            if dbug_print:
                print('wh', w, h)
                print(int(x + (w / 2)), int(y + (h / 2)))

            ratio = float(w) / h
            if name:
                if 0.9 <= ratio <= 1.1:
                    cv2.putText(img, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                else:
                    cv2.putText(img, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if border:
                img = cv2.drawContours(img, [cnt], -1, (0, 255, 255), 3)
            if center_dot:
                img = cv2.circle(img, (int(x + (w / 2)), int(y + (h / 2))), radius=2, color=(0, 0, 255), thickness=-1)
            if threshold_dot:
                thresholded_image = cv2.circle(thresholded_image, (int(x + (w / 2)), int(y + (h / 2))), radius=2, color=(0, 0, 255),
                                       thickness=-1)
            """


def draw_cylinders(img, thresholded_image, border=False, threshold_border=False, dbug_print=False):
    blur = cv2.blur(img, (3, 3))
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50,
                               param2=30,
                               minRadius=1,
                               maxRadius=40
                               )

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for pt in circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            """
            # For advanced debugging
            if dbug_print:
                print(a, b, r)

            if border:
                img = cv2.circle(img, (int(a), int(b)), radius=r, color=(0, 255, 0), thickness=2)

            if threshold_border:
                thresholded_image = cv2.circle(thresholded_image, (int(a), int(b)), radius=2, color=(0, 255, 0), thickness=-1)
            """


def show_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Get image from local file
    img = cv2.imread('file.jpeg')

    # Get image form Sick camera
    # img = get_image('10.1.1.8')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 255 is peak grayscale value
    _, thresholded_image = cv2.threshold(img, camera1_threshold, 255, cv2.THRESH_BINARY)

    show_image(thresholded_image)

    draw_squares(img, thresholded_image, center_dot=True)
    draw_cylinders(img, thresholded_image, border=True)

    show_image(img)
