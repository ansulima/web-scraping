# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar os dados do CSV
df = pd.read_csv('/home/anderson-lima/Documentos/TESTES DE NIVELAMENTO v.250321/api/backend/data/Relatorio_cadop.csv', sep=';', encoding='utf-8')

# Pré-processamento dos dados
df = df.fillna('')
df = df.astype(str)

@app.get("/operadoras/")
async def buscar_operadoras(termo: str, limite: int = 10):
    """
    Busca operadoras por termo textual, retornando os registros mais relevantes.
    A relevância é determinada pela presença do termo em campos importantes.
    """
    if not termo:
        return []
    
    termo = termo.lower()
    
    # Criar uma coluna de pontuação baseada na relevância
    def calcular_relevancia(row):
        score = 0
        campos_relevantes = ['Razao_Social', 'Nome_Fantasia', 'Modalidade', 'Cidade', 'UF']
        
        for campo in campos_relevantes:
            if termo in str(row[campo]).lower():
                score += 2 if campo in ['Razao_Social', 'Nome_Fantasia'] else 1
        
        return score
    
    df['relevancia'] = df.apply(calcular_relevancia, axis=1)
    
    # Filtrar e ordenar por relevância
    resultados = df[df['relevancia'] > 0].sort_values('relevancia', ascending=False).head(limite)
    
    # Converter para formato JSON
    return resultados.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)