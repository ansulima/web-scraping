import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Diretório para salvar os arquivos baixados
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# Função para baixar arquivos PDF
def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo baixado: {save_path}")
    else:
        print(f"Falha ao baixar o arquivo: {url}")

# Função principal
def main():
    # Faz a requisição HTTP para acessar o site
    response = requests.get(url)
    if response.status_code != 200:
        print("Falha ao acessar o site.")
        return

    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todos os links para arquivos PDF na página
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            pdf_links.append(href)

    if not pdf_links:
        print("Nenhum arquivo PDF encontrado na página.")
        return

    # Filtra apenas os Anexos I e II (se necessário, ajuste os nomes aqui)
    filtered_links = [link for link in pdf_links if "Anexo_I" in link or "Anexo_II" in link]

    if not filtered_links:
        print("Anexos I e II não encontrados.")
        return

    # Baixa os arquivos PDF
    downloaded_files = []
    for pdf_url in filtered_links:
        file_name = os.path.basename(pdf_url)
        save_path = os.path.join(download_dir, file_name)
        download_pdf(pdf_url, save_path)
        downloaded_files.append(save_path)

    # Compacta os arquivos baixados em um único arquivo ZIP
    zip_file_path = os.path.join(download_dir, "anexos.zip")
    with ZipFile(zip_file_path, 'w') as zip_file:
        for file in downloaded_files:
            zip_file.write(file, os.path.basename(file))
            print(f"Adicionado ao ZIP: {file}")

    print(f"Todos os arquivos foram compactados em: {zip_file_path}")

if __name__ == "__main__":
    main()
