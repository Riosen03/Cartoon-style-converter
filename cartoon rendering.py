import cv2
import numpy as np

img_name = "test5"


img = cv2.imread(img_name + ".jpg")
if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit()



# edge 탐지
# 흑백(gray)으로 전환, noise 제거
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 7)
# Sobel(edge 찾기)
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
mag = np.sqrt(sobelx**2 + sobely**2)
mag = cv2.convertScaleAbs(mag)
# Threshold(noise 제거)
_, edges = cv2.threshold(mag, 40, 255, cv2.THRESH_BINARY)


# 색 필터
color = img.copy()
for _ in range(2):
    color = cv2.bilateralFilter(color, 9, 300, 300)
Z = color.reshape((-1, 3))
Z = np.float32(Z)
# k-mean(색상 단순화)
K = 10
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
_, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)


# 이미지 복원
center = np.uint8(center)
color_quantized = center[label.flatten()]
color_quantized = color_quantized.reshape(color.shape)
# edge 색 반전 & 합성
edges_inv = cv2.bitwise_not(edges)
cartoon = cv2.bitwise_and(color_quantized, color_quantized, mask=edges_inv)



cv2.imshow("Original", img)
cv2.imshow("Cartoon", cartoon)
cv2.imwrite(img_name + "_cartoon_result.jpg", cartoon)
cv2.waitKey(0)
cv2.destroyAllWindows()