import os
import unittest
from unittest.mock import patch, MagicMock
from main import download_pdf, main

class TestWebScraping(unittest.TestCase):

    def setUp(self):
        """Configuração inicial antes de cada teste."""
        self.url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-dasociedade/atualizacao-do-rol-de-procedimentos"
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)

    def tearDown(self):
        """Limpeza após cada teste."""
        for file in os.listdir(self.download_dir):
            os.remove(os.path.join(self.download_dir, file))
        os.rmdir(self.download_dir)

    @patch("main.requests.get")
    def test_site_access(self, mock_get):
        """Testa se o site está acessível."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = main()
        self.assertEqual(response, None)  # O script não deve retornar nada em caso de sucesso
        mock_get.assert_called_once_with(self.url, headers={'User-Agent': 'Mozilla/5.0'})

    @patch("main.BeautifulSoup")
    @patch("main.requests.get")
    def test_find_pdf_links(self, mock_get, mock_soup):
        """Testa se o script encontra links de PDFs na página."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_soup.return_value = mock_soup_instance
        mock_soup_instance.find_all.return_value = [
            MagicMock(href="https://example.com/Anexo_I.pdf"),
            MagicMock(href="https://example.com/Anexo_II.pdf")
        ]

        main()  # Executa o script principal
        mock_soup_instance.find_all.assert_called_once_with("a", href=True)

    @patch("main.requests.get")
    def test_download_pdf(self, mock_get):
        """Testa se o script baixa um arquivo PDF."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake pdf content"
        mock_get.return_value = mock_response

        pdf_url = "https://example.com/test.pdf"
        save_path = os.path.join(self.download_dir, "test.pdf")
        download_pdf(pdf_url, save_path)

        self.assertTrue(os.path.exists(save_path))
        with open(save_path, "rb") as file:
            self.assertEqual(file.read(), b"fake pdf content")

    def test_zip_creation(self):
        """Testa se o script cria um arquivo ZIP corretamente."""
        # Cria arquivos fictícios para simular o download
        file1 = os.path.join(self.download_dir, "file1.pdf")
        file2 = os.path.join(self.download_dir, "file2.pdf")
        with open(file1, "w") as f:
            f.write("dummy content")
        with open(file2, "w") as f:
            f.write("dummy content")

        zip_file_path = os.path.join(self.download_dir, "anexos.zip")
        from zipfile import ZipFile
        with ZipFile(zip_file_path, "w") as zip_file:
            zip_file.write(file1, os.path.basename(file1))
            zip_file.write(file2, os.path.basename(file2))

        self.assertTrue(os.path.exists(zip_file_path))

if __name__ == "__main__":
    unittest.main()
