import pytesseract
import cv2
import os

# Diretório onde o script está sendo executado
base_dir = os.path.dirname(os.path.abspath(_file_))
output_dir = os.path.join(base_dir, "output")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def desenhaContornos(contornos, imagem):
    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            # aproxima os contornos da forma correspondente
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
            if len(approx) == 4:
                # Contorna a placa atraves dos contornos encontrados
                (x, y, lar, alt) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y), (x + lar, y + alt), (0, 255, 0), 2)
                # segmenta a placa da imagem
                roi = imagem[y:y + alt, x:x + lar]
                cv2.imwrite(os.path.join(output_dir, "roi.png"), roi)


def buscaRetanguloPlaca(source):
    # Captura ou Video
    video = cv2.VideoCapture(source)

    while video.isOpened():

        ret, frame = video.read()

        if (ret == False):
            break

        # area de localização 720p video original
        area = frame[500:, 300:800]

        # escala de cinza
        img_result = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

        # limiarização
        ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)

        # desfoque
        img_result = cv2.GaussianBlur(img_result, (5, 5), 0)

        # lista os contornos
        contornos, hier = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        cv2.imshow('FRAME', frame)

        desenhaContornos(contornos, area)

        cv2.imshow('RES', area)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    video.release()
    preProcessamentoRoi()
    cv2.destroyAllWindows()


def preProcessamentoRoi():
    img_roi = cv2.imread(os.path.join(output_dir, "roi.png"))
    if img_roi is None:
        return

    # redimensiona a imagem da placa em 4x
    img = cv2.resize(img_roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Desfoque na Imagem
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Salva a imagem processada para OCR
    cv2.imwrite(os.path.join(output_dir, "roi-ocr.png"), img)

    return img


def reconhecimentoOCR():
    img_roi_ocr = cv2.imread(os.path.join(output_dir, "roi-ocr.png"))
    if img_roi_ocr is None:
        return

    config = r'-c tessedit_char_whitelist=ABCDEFGHJKLMNOPQRSTUVWXYZ1234567890 --psm 6'
    saida = pytesseract.image_to_string(img_roi_ocr, lang='eng', config=config)

    gravar_saida(saida)


def gravar_saida(saida):
    if not os.path.isdir(os.path.join(base_dir, 'Arquivos')):
        os.mkdir(os.path.join(base_dir, 'Arquivos'))

    # Verificar se o arquivo já existe
    arquivo_existe = os.path.isfile(os.path.join(base_dir, 'Arquivos', 'placas.txt'))

    with open(os.path.join(base_dir, 'Arquivos', 'placas.txt'), 'a', encoding='utf-8') as arq:
        if arquivo_existe:
            # Adicionar uma quebra de linha antes de escrever a nova saída
            arq.write('\n')
        arq.write(saida)
        print(saida)


if _name_ == "_main_":
    source = os.path.join(base_dir, "resource", "fiorino.mp4")

    buscaRetanguloPlaca(source)
    preProcessamentoRoi()
    reconhecimentoOCR()
