import os,base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DESKTOP_PATH = os.path.expanduser("~/Desktop")

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

    try:
        dados_original = ler_arquivo(nome_arquivo)
        dados_criptografados = fernet.encrypt(dados_original)
        gravar_arquivo(nome_arquivo + '.cripto', dados_criptografados)
        os.remove(nome_arquivo)
        
        return 'Dados criptografados com sucesso!'
    
    except Exception as e:
        return e

def descriptografar_arquivo(nome_arquivo, chave):
    fernet = Fernet(chave)

    try:
        dados_criptografados = ler_arquivo(nome_arquivo)
        dados_descriptografados = fernet.decrypt(dados_criptografados)
        gravar_arquivo(nome_arquivo.replace('.cripto', ''), dados_descriptografados)
        os.remove(nome_arquivo)

        return 'Arquivo descriptografrado com sucesso!'
    
    except InvalidToken:
        return 'Senha Errada!'
    
    except Exception as e:
        return e
        

def main(arquivo):
    senha = input("Digite uma senha: " )
    chave = derivar_chave(senha)
    print(chave)
    if not os.path.isfile(arquivo + '.cripto'):
        # chave = salvar_chave('chave')
        output = criptografar_arquivo(arquivo, chave)
    else:
        # chave = ler_arquivo('chave')
        output = descriptografar_arquivo(arquivo + '.cripto', chave)
    print(output)

if __name__ == '__main__':
    main(DESKTOP_PATH + '\\image.jpeg')

# def gerar_chave():
#     return Fernet.generate_key()

# def salvar_chave(nome_arquivo):
#     chave = gerar_chave()
#     gravar_arquivo(nome_arquivo, chave)
#     return chave