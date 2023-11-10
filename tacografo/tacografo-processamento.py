import cv2
import numpy as np

# Carregar a imagem
img = cv2.imread("tacografo_processado.png", cv2.IMREAD_GRAYSCALE)

# Definir as coordenadas das linhas de velocidade
velocidades = [120, 100, 80, 60, 40, 20, 0]

# Inicializar lista para armazenar os pontos de máxima e mínima
pontos_max_min = []

# Percorrer a imagem a partir da segunda linha
for y in range(1, img.shape[0]):
    linha_anterior = img[y-1]
    linha_atual = img[y]
    
    # Verificar se houve uma transição de velocidade
    transicoes = np.where(linha_anterior != linha_atual)[0]
    
    if len(transicoes) > 0:
        for transicao in transicoes:
            velocidade_anterior = linha_anterior[transicao]
            velocidade_atual = linha_atual[transicao]
            
            if velocidade_anterior in velocidades and velocidade_atual in velocidades:
                tempo_min = y // 5  # Cada linha representa 5 minutos
                pontos_max_min.append((tempo_min, velocidade_anterior, velocidade_atual))

# Imprimir os pontos de máxima e mínima
for ponto in pontos_max_min:
    print(f"Tempo: {ponto[0]*5} minutos - Velocidade Máxima: {max(ponto[1], ponto[2])} km/h, Velocidade Mínima: {min(ponto[1], ponto[2])} km/h")
