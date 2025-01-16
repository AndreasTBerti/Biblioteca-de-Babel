import requests
from bs4 import BeautifulSoup
import os

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QListWidget, QLineEdit, QScrollArea
from random import randint, choice

class InterfaceGrafica(QWidget):

    def __init__(self):
        self.aplication = QApplication()

        super().__init__()

        # Configuração da Janela do App
        self.setWindowTitle("Biblioteca de Babel")
        self.resize(900, 700)

        # Criação dos Objetos do App

        # Input do url
        self.text_box = QLineEdit()
        self.text_box.setStyleSheet("QLineEdit { padding: 10px; font-size: 14px; background-color: #F8F8FF; }")

        # Lista de Arquivos Upados
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("border: 1px solid black;")

        # Botão para extrair os textos do site com o presente url
        self.botao_extrair = QPushButton("Extrair")

        # Local onde se exibirá as palavras coletadas
        self.exibir_palavras = QLabel()

        # Scroll dos textos
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.exibir_palavras)
        self.scroll_area.setWidgetResizable(True)

        # Criação do Layout

        self.master_layout = QHBoxLayout()

        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.text_box)
        col1.addWidget(self.botao_extrair)
        col1.addWidget(self.file_list)
        
        col2.addWidget(self.scroll_area)

        self.master_layout.addLayout(col1, 20)
        self.master_layout.addLayout(col2, 80)
        self.master_layout.setContentsMargins(16, 16, 16, 16)

        

    def exibirArquivos(self):
        
        # Coletando os textos já armazenados
        arquivos_acervo = os.listdir("Acervo")

        self.file_list.clear()
        for item in arquivos_acervo:
            self.file_list.addItem(item)


class BibliotecaDeBabel(InterfaceGrafica):

    def __init__(self):
        super().__init__()

        # Criação do diretório no qual os arquivos serão armazenados.
        try:
            os.mkdir("Acervo")
        except FileExistsError:
            pass


        self.exibirArquivos()
        self.file_list.currentRowChanged.connect(self.abrirArquivo)
        self.botao_extrair.clicked.connect(self.gerarArquivo)

        self.setLayout(self.master_layout)

        super().show()
        self.aplication.exec()

    
    # Função que extrai os textos para um arquivo.txt e os armazena do diretório criado
    def gerarArquivo(self) -> None:

        # Extraindo o url da caixa de texto da interface 
        self.url = self.text_box.text()

        # Lista de palavras palavras tratadas para serem utilizadas na biblioteca
        palavras_tratadas = []

        # Requisição de acesso ao site
        try:
            fonte = requests.get(self.url)
        except requests.exceptions.ConnectionError as e:
            raise Exception("falha ao estabelecer conexão com o site")

        # Coleta do html do site e conversão para texto
        soup: BeautifulSoup = BeautifulSoup(fonte.text, "html.parser")
        
        # Coleta dos textos presentes no corpo do html
        lista_textos = []
        for dado in soup:
            dado = dado.get_text()
            lista_textos = dado.split(" ") #Coleta de cada palavra individualmente

            # Tratamento das Palavras
            for texto in lista_textos:

                texto_tratado = texto.replace("\n", "") #Primeiro Tratamento
                texto_tratado = texto_tratado.strip('.""!()?@©|[]$&,<>:;=+-/» ') #Segundo Tratamento

                # Último tratamento
                if texto_tratado != '': #Excluino espaços vazios ou sem importância
                    if '.' in texto_tratado: #Seprando palavras por ponto
                        divisao_provisoria: list = texto_tratado.split('.')
                        palavras_tratadas.extend(divisao_provisoria)
                    else:
                        palavras_tratadas.append(texto_tratado) 


        # Processo de criação do arquivo.
        verificador: bool = False
        while not verificador:

            nome_arquivo_gerado = self.criarNome() #Nome a ser utilizado no arquivo

            # Verifica se já existe um arquivo com esse nome. Se existir, outro nome será gerado.
            if not os.path.exists(f"Acervo/{nome_arquivo_gerado}.txt"): #Verificando se o arquivo existe
                with open(f"Acervo/{nome_arquivo_gerado}.txt", 'w', encoding="utf-8") as file: #Criando o arquivo
                    for index, palavra in enumerate(palavras_tratadas): #Coletando as palavras
                        file.write(f"{index + 1}. {palavra.capitalize()}\n") #Armazenando-as no arquivo

                verificador = True

        print(f"Novo arquivo gerado: {nome_arquivo_gerado}")
        self.exibirArquivos()


    def abrirArquivo(self) -> None:
        self.texto_exibido = ''

        textfilename = self.file_list.currentItem().text()

        with open(f"Acervo/{textfilename}", encoding="utf-8") as file:
            texto = file.readlines()
            for palavra in texto:
                self.texto_exibido += palavra + "\n"

        self.exibir_palavras.setText(self.texto_exibido)


    # Função que gera um nome aleatório para o arquivo criado.
    def criarNome(self) -> str:

        # Palavras e números coletados para integrar a senha
        palavras_chave: list = []
        numeros_chave: str = ''

        # Gerando as palavras e os números
        palavras_chave = self.url.split("/")
        for n in range(5): numeros_chave += str(randint(0, 10))


        # Palavra que será utilizada para a senha
        palavra_chave_senha: str = ''

        # Tratando e escolhendo a palavra chave da senha
        verificador = False
        while not verificador:
            palavra_chave_senha = choice(palavras_chave) #Escolha da Palavra
            palavra_chave_senha = palavra_chave_senha.strip(":") #Primeiro tratamento 

            #Segundo Tratamento
            if palavra_chave_senha == '': #Primeiro Filtro
                palavras_chave.remove(palavra_chave_senha)
            
            else:

                if "." in palavra_chave_senha: #Segundo Filtro
                    lista_provisoria: list = palavra_chave_senha.split(".")
                    palavra_chave_senha = choice(lista_provisoria)

                if "-" in palavra_chave_senha: #Terceiro Filtro
                    lista_provisoria: list = palavra_chave_senha.split("-")
                    palavra_chave_senha = choice(lista_provisoria)

                verificador = True


        #print(palavra_chave_senha + numeros_chave)
        return palavra_chave_senha + numeros_chave
        

# Execução teste para o programa.
def main():   

    biblioteca: BibliotecaDeBabel = BibliotecaDeBabel()


if __name__ == "__main__":
    main()