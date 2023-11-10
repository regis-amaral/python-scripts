import cv2
import numpy as np

# Carregar a imagem
img = cv2.imread("tacografo_processado.png", cv2.IMREAD_GRAYSCALE)

# Aplicar thresholding
_, binary_img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

# Criar kernel para dilatação
kernel = np.ones((1, 5), np.uint8)  # Ajuste o tamanho conforme necessário

# Criar uma máscara para proteger os caracteres/dígitos
masked_img = cv2.bitwise_and(binary_img, binary_img, mask=~binary_img)

# Aplicar dilatação apenas nas áreas não protegidas pela máscara
dilated_img = cv2.dilate(masked_img, kernel, iterations=1)

# Combinar a imagem dilatada com a imagem original
final_img = cv2.bitwise_or(dilated_img, binary_img)

# Salvar a imagem resultante
cv2.imwrite("tacografo_sem_linhas_tracejadas.png", final_img)
