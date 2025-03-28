-- Importação de operadoras (ajuste o caminho do arquivo)
LOAD DATA INFILE '/caminho/completo/operadoras_ativas.csv'
INTO TABLE operadoras_ativas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
 logradouro, numero, complemento, bairro, cidade, uf, cep,
 ddd, telefone, fax, endereco_eletronico, representante,
 cargo_representante, @data_registro_ans)
SET data_registro_ans = STR_TO_DATE(@data_registro_ans, '%d/%m/%Y');

-- Importação de demonstrações (executar para cada arquivo mensal)
LOAD DATA INFILE '/caminho/completo/demonstracao_202301.csv'
INTO TABLE demonstracoes_contabeis
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, @competencia, conta_contabil, descricao, @valor)
SET
    competencia = STR_TO_DATE(CONCAT(@competencia, '01'), '%Y%m%d'),
    valor = CAST(REPLACE(REPLACE(@valor, '.', ''), ',', '.') AS DECIMAL(15,2));