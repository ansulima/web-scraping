import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from tabula import read_pdf
from extract_tables import extract_tables_from_pdf, replace_abbreviations

# Caminho para o PDF de teste
TEST_PDF_PATH = "test_data/test_pdf.pdf"
TEST_CSV_PATH = "test_data/test_csv.csv"
TEST_ZIP_PATH = "test_data/test_zip.zip"

class TestExtractTables(unittest.TestCase):

    def setUp(self):
        """Configuração inicial antes de cada teste."""
        # Cria uma pasta temporária para arquivos de teste
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Limpeza após cada teste."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    @patch("tabula.read_pdf")
    def test_extract_tables_from_pdf(self, mock_read_pdf):
        """Testa se o PDF é lido corretamente e retorna um DataFrame."""
        """ O teste test_extract_tables_from_pdf tenta ler um arquivo PDF fictício (test_pdf.pdf) que deveria estar no diretório test_data/.
            Como esse arquivo não existe, ai o teste falha."""
        # Mock dos dados retornados pelo tabula.read_pdf
        mock_table = pd.DataFrame({
            "OD": ["OD", "AMB"],
            "AMB": ["AMB", "OD"]
        })
        mock_read_pdf.return_value = [mock_table]

        # Executa a função
        result = extract_tables_from_pdf(TEST_PDF_PATH)

        # Verifica se o resultado é um DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # Verifica o número de linhas

    def test_replace_abbreviations(self):
        """Test if the abbreviations OD and AMB are correctly replaced with their full descriptions."""

        # Create a test DataFrame with abbreviations
        df = pd.DataFrame({
            "OD": ["OD", "AMB"],
            "AMB": ["AMB", "OD"]
        })

        # Execute the function to replace abbreviations
        result = replace_abbreviations(df)

        # Check if the replacements were done correctly for the "OD" column
        self.assertEqual(result["OD"].tolist(), ["Odontológico", "Ambulatorial"])

        # Check if the replacements were done correctly for the "AMB" column
        self.assertEqual(result["AMB"].tolist(), ["Ambulatorial", "Odontológico"])

    def test_csv_creation(self):
        """Testa se o CSV é gerado corretamente."""
        # Cria um DataFrame de teste
        df = pd.DataFrame({
            "OD": ["Odontológico", "Ambulatorial"],
            "AMB": ["Ambulatorial", "Odontológico"]
        })

        # Salva o DataFrame como CSV
        df.to_csv(TEST_CSV_PATH, index=False)

        # Verifica se o arquivo CSV foi criado
        self.assertTrue(os.path.exists(TEST_CSV_PATH))

        # Lê o CSV e verifica o conteúdo
        loaded_df = pd.read_csv(TEST_CSV_PATH)
        self.assertEqual(loaded_df["OD"].tolist(), ["Odontológico", "Ambulatorial"])

    def test_zip_creation(self):
        """Testa se o arquivo ZIP é criado corretamente."""
        from zipfile import ZipFile

        # Cria um arquivo CSV de teste
        df = pd.DataFrame({
            "OD": ["Odontológico", "Ambulatorial"],
            "AMB": ["Ambulatorial", "Odontológico"]
        })
        df.to_csv(TEST_CSV_PATH, index=False)

        # Compacta o CSV em um arquivo ZIP
        with ZipFile(TEST_ZIP_PATH, "w") as zip_file:
            zip_file.write(TEST_CSV_PATH, os.path.basename(TEST_CSV_PATH))

        # Verifica se o arquivo ZIP foi criado
        self.assertTrue(os.path.exists(TEST_ZIP_PATH))

        # Verifica se o ZIP contém o CSV
        with ZipFile(TEST_ZIP_PATH, "r") as zip_file:
            files_in_zip = zip_file.namelist()
            self.assertIn(os.path.basename(TEST_CSV_PATH), files_in_zip)

if __name__ == "__main__":
    unittest.main()