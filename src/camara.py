import cv2
import numpy as np

# Cargar vídeo
url = "http://192.168.0.2:8080/video.jpg"
cap = cv2.VideoCapture(0)
print("Esperando tecla: ")
filtro = np.ones((5,5),np.float32)/25
# Trabajamos frame a frame
while(cap.isOpened()):
	ret, frame = cap.read()
	if ret==True:    
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == 27:
			break
		elif cv2.waitKey(1) & 0xFF == ord('s'):
			print('Guardando la foto')
			cv2.imwrite('img.png',frame)
			img_to_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
			img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])
			hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)
			dst = cv2.filter2D(hist_equalization_result,-1,filtro)
			cv2.imwrite('ecualizada.png',hist_equalization_result)
			cv2.imwrite('suavizada.png',dst)
			gray_image = cv2.cvtColor(hist_equalization_result, cv2.COLOR_BGR2GRAY) 
			cv2.imwrite('foto_old.png',gray_image)
	else:
		break
cap.release()
cv2.destroyAllWindows()
