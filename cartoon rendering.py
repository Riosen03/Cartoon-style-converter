import cv2
import numpy as np

def cartoonize(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    edges = cv2.Canny(gray, 50, 150)

    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel)

    color = img.copy()
    for _ in range(3):
        color = cv2.bilateralFilter(color, d=9, sigmaColor=200, sigmaSpace=200)

    Z = color.reshape((-1, 3))
    Z = np.float32(Z)

    K = 8
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    color_quantized = center[label.flatten()]
    color_quantized = color_quantized.reshape(color.shape)

    edges_inv = cv2.bitwise_not(edges)
    cartoon = cv2.bitwise_and(color_quantized, color_quantized, mask=edges_inv)

    return cartoon


if __name__ == "__main__":
    img_name = "test1"

    img = cv2.imread(img_name + ".jpg")

    if img is None:
        print("이미지를 불러올 수 없습니다.")
        exit()

    cartoon = cartoonize(img)

    cv2.imshow("Original", img)
    cv2.imshow("Cartoon", cartoon)

    cv2.imwrite(img_name + "_cartoon_result.jpg", cartoon)

    cv2.waitKey(0)
    cv2.destroyAllWindows()