import os
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Caminho para o CSV
CSV_PATH = "/home/anderson-lima/Documentos/TESTES DE NIVELAMENTO v.250321/database/data/Relatorio_cadop.csv"

# Verificar se o arquivo existe
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Arquivo CSV não encontrado: {CSV_PATH}")

# Carregar o CSV dos dados cadastrais das operadoras
try:
    df = pd.read_csv(
        CSV_PATH,
        encoding='utf-8',
        delimiter=';',  # Altere conforme necessário (',' ou ';')
        on_bad_lines='skip'  # Ignorar linhas malformadas
    )
except Exception as e:
    raise ValueError(f"Erro ao carregar o CSV: {e}")


@app.route('/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q', '').lower()  # Obter a consulta textual
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # Filtrar registros que contenham a consulta em qualquer coluna
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]

    # Converter os resultados para JSON
    return jsonify(results.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)