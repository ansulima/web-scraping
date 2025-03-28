import os
import pandas as pd
from tabula import read_pdf
from zipfile import ZipFile

# Caminho para o PDF do Anexo I
pdf_path = "../downloads/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
output_csv = "rol_procedimentos.csv"
output_zip = "Teste_Anderson_Lima.zip"


def extract_tables_from_pdf(pdf_path):
    """Extrai tabelas do PDF e retorna um DataFrame."""
    # Extrai tabelas do PDF usando tabula-py
    tables = read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=True)

    # Concatena todas as tabelas em um único DataFrame
    combined_df = pd.concat(tables, ignore_index=True)
    return combined_df


def replace_abbreviations(df):
    """Substitui as abreviações OD e AMB pelas descrições completas."""
    abbreviation_map = {
        "OD": "Odontológico",
        "AMB": "Ambulatorial"
    }
    df["OD"] = df["OD"].replace(abbreviation_map)
    df["AMB"] = df["AMB"].replace(abbreviation_map)
    return df


def main():
    # Extrai tabelas do PDF
    df = extract_tables_from_pdf(pdf_path)

    # Substitui abreviações
    df = replace_abbreviations(df)

    # Salva o DataFrame como CSV
    df.to_csv(output_csv, index=False)
    print(f"Dados salvos em {output_csv}")

    # Compacta o CSV em um arquivo ZIP
    with ZipFile(output_zip, "w") as zip_file:
        zip_file.write(output_csv, os.path.basename(output_csv))
    print(f"Arquivo compactado em {output_zip}")


if __name__ == "__main__":
    main()