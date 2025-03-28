-- Criação da tabela de operadoras ativas
CREATE TABLE IF NOT EXISTS operadoras_ativas (
    registro_ans VARCHAR(20) NOT NULL,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE,
    PRIMARY KEY (registro_ans)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Criação da tabela de demonstrações contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20) NOT NULL,
    competencia DATE NOT NULL,
    conta_contabil VARCHAR(50) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES operadoras_ativas(registro_ans),
    INDEX idx_competencia (competencia),
    INDEX idx_descricao (descricao(50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;