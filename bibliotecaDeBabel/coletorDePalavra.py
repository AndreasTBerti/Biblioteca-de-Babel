from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import os

from random import randint, choice

@dataclass
class ColetorDePalavra():
    url: str

    def __post_init__(self):

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
                texto_tratado = texto_tratado.strip('.""!()?@©|[]$&,<>:;=+-/') #Segundo Tratamento

                # Último tratamento
                if texto_tratado != '': #Excluino espaços vazios ou sem importância
                    if '.' in texto_tratado: #Seprando palavras por ponto
                        divisao_provisoria: list = texto_tratado.split('.')
                        palavras_tratadas.extend(divisao_provisoria)
                    else:
                        palavras_tratadas.append(texto_tratado) 

        print(palavras_tratadas)

        # Criação do diretório no qual os arquivos serão armazenados
        try:
            os.mkdir("BibliotecaDeBabel")
        except FileExistsError:
            pass

        # Processo de criação do arquivo
        verificador: bool = False
        while not verificador:

            nome_arquivo_gerado = self.geradorDeNomes() #Nome a ser utilizado no arquivo

            # Se o arquivo já existir, outro nome será gerado
            if not os.path.exists(f"BibliotecaDeBabel/{nome_arquivo_gerado}.txt"): #Verificando se o arquivo existe
                with open(f"BibliotecaDeBabel/{nome_arquivo_gerado}.txt", 'w', encoding="utf-8") as file:
                    for index, palavra in enumerate(palavras_tratadas):
                        file.write(f"{index + 1}. {palavra.capitalize()}\n")

                verificador = True

        print(f"Novo arquivo gerado: {nome_arquivo_gerado}")


    # Função que gera um nome aleatório para o arquivo criado
    def geradorDeNomes(self) -> str:

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
        

# Execução teste para o programa
def main():   
    teste = ColetorDePalavra('https://docs.python.org/3/library/functions.html#sorted')

if __name__ == "__main__":
    main()