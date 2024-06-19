# Documentação de Instalação

## Pré-requisitos

Antes de instalar o código, verifique se você possui os seguintes pré-requisitos instalados em seu sistema:

- [Python](https://www.python.org/downloads/release/python-390/) (versão 3.9 ou superior)
- [Open CV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) (versão 4.7 ou superior)
- [PyTesseract](https://pypi.org/project/pytesseract/) (versão 0.3.10 ou superior)
- [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (versão 5.0.0 ou superior): Adicionar o caminho do diretório da instalação nas variáveis de ambiente

Certifique-se de ter as versões corretas das dependências instaladas para evitar conflitos ou erros durante a execução do código.

## Instalação

Siga as etapas abaixo para instalar e configurar o código:

1. Clone o repositório do código para o seu sistema:
Se você não tiver o Git instalado, pode fazer o download do repositório como um arquivo ZIP e descompactá-lo em uma pasta de sua escolha.

`git clone https://github.com/ICEI-PUC-Minas-PPC-CC/ppc-cc-2023-1-visao-comp-detectar-placa-de-veiculo.git`

2. Acesse o diretório do código:

`cd src`

3. Instale as dependências do código usando um gerenciador de pacotes, como o `pip`:

`pip install opencv-python`
`pip install pytesseract`

Certifique-se de estar usando o ambiente correto (virtual ou global) para evitar conflitos de pacotes.

4. Realize outras configurações necessárias, como o vídeo a ser analisado para a extração da placa, conforme especificado na documentação do código.

## Executando o Código

Após concluir a instalação, você pode executar o código da seguinte maneira:

1. Navegue até o diretório raiz do código:

`cd src`

2. Execute o código:

`python EncontrarPlaca.py`

Certifique-se de seguir as instruções adicionais fornecidas na documentação do código para realizar tarefas específicas ou configurações adicionais.