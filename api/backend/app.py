import os
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Caminho correto do CSV
CSV_PATH = "/home/anderson-lima/Documentos/TESTES DE NIVELAMENTO v.250321/database/data/Relatorio_cadop.csv"

# Verificar se o arquivo existe
try:
    df = pd.read_csv(CSV_PATH, encoding='latin1', delimiter=';')  # Ajuste a codificação e o delimitador se necessário
except FileNotFoundError:
    print(f"Erro: arquivo CSV não encontrado em {CSV_PATH}")
    df = None

@app.route('/empresas', methods=['GET'])
def get_empresas():
    if df is None:
        return jsonify({'erro': 'Arquivo CSV não encontrado'}), 404

    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'erro': 'Parâmetro "q" é obrigatório'}), 400

    # Supondo que a coluna com o nome da empresa seja "Nome Fantasia"
    empresas = df[df['Nome_Fantasia'].str.lower().str.contains(query, na=False)]['Nome_Fantasia'].tolist()

    return jsonify({'empresas': empresas})

if __name__ == '__main__':
    app.run(debug=True)
