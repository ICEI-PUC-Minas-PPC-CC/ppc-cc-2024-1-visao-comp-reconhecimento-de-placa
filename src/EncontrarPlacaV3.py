import cv2
import pytesseract
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Diretório para salvar o arquivo placas.txt
arquivos_dir = os.path.join(base_dir, "Arquivos")
placas_file = os.path.join(arquivos_dir, "placas.txt")

# Cria o diretório Arquivos se não existir
if not os.path.exists(arquivos_dir):
    os.makedirs(arquivos_dir)

# Cria o diretório output se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Cria o arquivo placas.txt se não existir
if not os.path.isfile(placas_file):
    with open(placas_file, 'w'):
        pass  # Arquivo criado vazio

def desenhaContornos(contornos, imagem):
    for i, c in enumerate(contornos):
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(approx) == 4:
                (x, y, lar, alt) = cv2.boundingRect(c)
                aspect_ratio = lar / float(alt)
                if 2 < aspect_ratio < 5 and alt > 20 and alt < 100 and lar > 80:
                    cv2.rectangle(imagem, (x, y), (x + lar, y + alt), (0, 255, 0), 2)
                    roi = imagem[y:y + alt, x:x + lar]
                    return roi
    return None

def buscaRetanguloPlaca(source):
    if not os.path.isfile(source):
        print(f"Arquivo de vídeo não encontrado: {source}")
        return

    video = cv2.VideoCapture(source)
    if not video.isOpened():
        print(f"Não foi possível abrir o vídeo: {source}")
        return

    frame_count = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1
        print(f"Processando frame {frame_count}")

        img_result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)
        #img_result = cv2.GaussianBlur(img_result, (5, 5), 0)
        #contornos, hier = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #roi_preprocessada = preProcessamentoRoi(img_result)
        saida = reconhecimentoOCR(img_result)
        gravar_saida(saida)

        #roi = desenhaContornos(contornos, frame)
        #if roi is not None:
        #    roi_preprocessada = preProcessamentoRoi(roi)
        #    saida = reconhecimentoOCR(roi_preprocessada)
        #    if saida and len(saida) == 8 and saida.isalnum():
        #        cv2.imwrite(os.path.join(output_dir, f"roi_{frame_count}.png"), roi_preprocessada)  # Salva a ROI processada para OCR
        #        gravar_saida(saida)
        #        exibir_placa(frame_count, roi)  # Exibe a ROI em uma janela separada

        cv2.imshow('FRAME', img_result)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

def preProcessamentoRoi(roi):
    #img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #img = cv2.equalizeHist(img)
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return img

def reconhecimentoOCR(img):
    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 --psm 6'
    saida = pytesseract.image_to_string(img, lang='eng', config=config)
    saida = saida.strip()
    print(f"OCR result: {saida}")
    return saida

def gravar_saida(saida):
    with open(placas_file, 'a', encoding='utf-8') as f:
        if os.path.getsize(placas_file) > 0:
            f.write('\n')
        f.write(saida)
    print(f"Gravando saída: {saida}")

def exibir_placa(frame_count, roi):
    cv2.imshow(f'Placa Identificada no Frame {frame_count}', roi)
    cv2.waitKey(0)
    cv2.destroyWindow(f'Placa Identificada no Frame {frame_count}')

if __name__ == "__main__":
    source = os.path.join(base_dir, "resource", "placa5.mp4")
    print(f"Tentando abrir o vídeo: {source}")
    buscaRetanguloPlaca(source)
