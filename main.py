import os,base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# DESKTOP_PATH = os.path.expanduser("~/Desktop")

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'rb') as arquivo:
        return arquivo.read()
    
def gravar_arquivo(nome_arquivo, mensagem):
    with open(nome_arquivo, 'wb') as arquivo:
        arquivo.write(mensagem)

def derivar_chave(senha, salt=b'saltomaluco@maisde8000'):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Tamanho da chave em bytes
        salt=salt,
        iterations=100000,  # Número de iterações do algoritmo (quanto maior, mais seguro)
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(senha.encode()))

def criptografar_arquivo(nome_arquivo, chave):
    fernet = Fernet(chave)
    nome_base_arquivo = os.path.basename(nome_arquivo)
    try:
        dados_original = ler_arquivo(nome_arquivo)
        dados_criptografados = fernet.encrypt(dados_original)
        gravar_arquivo(nome_arquivo + '.cripto', dados_criptografados)
        os.remove(nome_arquivo)
        
        return {nome_base_arquivo:'Dados criptografados com sucesso!'}
    
    except Exception as e:
        return e

def descriptografar_arquivo(nome_arquivo, chave):
    fernet = Fernet(chave)
    nome_base_arquivo = os.path.basename(nome_arquivo)
    try:
        dados_criptografados = ler_arquivo(nome_arquivo)
        dados_descriptografados = fernet.decrypt(dados_criptografados)
        gravar_arquivo(nome_arquivo.replace('.cripto', ''), dados_descriptografados)
        os.remove(nome_arquivo)

        return {nome_base_arquivo:'Arquivo descriptografrado com sucesso!'}
    
    except InvalidToken:
        return {nome_base_arquivo:'Senha Errada!'}
    
    except Exception as e:
        return e
        

def criptografar_descriptografar_arquivo(arquivo, senha):
    chave = derivar_chave(senha)
    print(chave)
    if not arquivo.endswith('.cripto'):
        # chave = salvar_chave('chave')
        saida = criptografar_arquivo(arquivo, chave)
    else:
        # chave = ler_arquivo('chave')
        saida = descriptografar_arquivo(arquivo, chave)
    return saida

def criptografar_descriptografar_pasta(pasta, senha):
    saida = []
    for root, dirs, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(root, arquivo)

            saida_arquivo = criptografar_descriptografar_arquivo(caminho_arquivo, senha)
            saida.append(saida_arquivo)
    return saida

def main():
    opcao = input(""" \
Digite uma opção:
    [1] Arquivo         
    [2] Pasta
    [3] Sair
Opção: """)
    if opcao == '1':
        arquivo = input("Digite o caminho completo do arquivo: ")
        senha = input("Digite uma Senha: ")
        saida = criptografar_descriptografar_arquivo(arquivo, senha)
        print(saida)

    elif opcao == '2':
        pasta = input("Digite o caminho completo da pasta: ")
        senha = input("Digite uma Senha: ")
        saida = criptografar_descriptografar_pasta(pasta, senha)
        print(saida)
    
    elif opcao == '3':
        print("Saindo...")

    else:
        print("Opçao Inválida!")
    


if __name__ == '__main__':
    main()

# def gerar_chave():
#     return Fernet.generate_key()

# def salvar_chave(nome_arquivo):
#     chave = gerar_chave()
#     gravar_arquivo(nome_arquivo, chave)
#     return chave