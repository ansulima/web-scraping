-- Query 1: Top 10 operadoras com maiores despesas no último trimestre
SELECT
    o.razao_social,
    o.nome_fantasia,
    SUM(d.valor) AS total_despesas,
    MAX(d.competencia) AS ultima_competencia
FROM
    demonstracoes_contabeis d
JOIN
    operadoras_ativas o ON d.registro_ans = o.registro_ans
WHERE
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS%'
    AND d.competencia >= DATE_SUB(
        (SELECT MAX(competencia) FROM demonstracoes_contabeis),
        INTERVAL 3 MONTH)
GROUP BY
    o.razao_social, o.nome_fantasia
ORDER BY
    total_despesas DESC
LIMIT 10;

-- Query 2: Top 10 operadoras com maiores despesas no último ano
SELECT
    o.razao_social,
    o.nome_fantasia,
    SUM(d.valor) AS total_despesas,
    COUNT(DISTINCT MONTH(d.competencia)) AS meses_com_dados
FROM
    demonstracoes_contabeis d
JOIN
    operadoras_ativas o ON d.registro_ans = o.registro_ans
WHERE
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS%'
    AND d.competencia >= DATE_SUB(
        (SELECT MAX(competencia) FROM demonstracoes_contabeis),
        INTERVAL 1 YEAR)
GROUP BY
    o.razao_social, o.nome_fantasia
ORDER BY
    total_despesas DESC
LIMIT 10;