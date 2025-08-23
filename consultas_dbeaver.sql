-- =====================================================
-- CONSULTAS ÚTEIS PARA DBEAVER - ADAPTIVE CODE JUDGE
-- =====================================================

-- 1. VISÃO GERAL DOS DADOS
-- =====================================================

-- Contar registros em cada tabela
SELECT 'problems' as tabela, COUNT(*) as total FROM problems
UNION ALL
SELECT 'test_cases' as tabela, COUNT(*) as total FROM test_cases
UNION ALL
SELECT 'benchmarks' as tabela, COUNT(*) as total FROM benchmarks
UNION ALL
SELECT 'submissions' as tabela, COUNT(*) as total FROM submissions
UNION ALL
SELECT 'submission_results' as tabela, COUNT(*) as total FROM submission_results
UNION ALL
SELECT 'problem_benchmark_active' as tabela, COUNT(*) as total FROM problem_benchmark_active;

-- 2. EXPLORAR PROBLEMAS
-- =====================================================

-- Ver todos os problemas
SELECT 
    id,
    title,
    difficulty,
    tags,
    time_limit_base,
    memory_limit,
    is_active,
    created_at
FROM problems
ORDER BY created_at DESC;

-- Problemas por dificuldade
SELECT 
    difficulty,
    COUNT(*) as quantidade
FROM problems
GROUP BY difficulty
ORDER BY quantidade DESC;

-- 3. EXPLORAR TEST CASES
-- =====================================================

-- Test cases por problema
SELECT 
    p.title as problema,
    COUNT(tc.id) as total_test_cases,
    SUM(CASE WHEN tc.is_sample = 1 THEN 1 ELSE 0 END) as samples,
    SUM(CASE WHEN tc.is_hidden = 1 THEN 1 ELSE 0 END) as hidden
FROM problems p
LEFT JOIN test_cases tc ON p.id = tc.problem_id
GROUP BY p.id, p.title
ORDER BY total_test_cases DESC;

-- Ver detalhes dos test cases
SELECT 
    p.title as problema,
    tc.name as test_case,
    tc.complexity_hint,
    tc.input_size,
    tc.is_sample,
    tc.is_hidden,
    tc.weight,
    LENGTH(tc.input_data) as tamanho_input,
    LENGTH(tc.expected_output) as tamanho_output
FROM test_cases tc
JOIN problems p ON tc.problem_id = p.id
ORDER BY p.title, tc.name;

-- 4. EXPLORAR BENCHMARKS
-- =====================================================

-- Ver benchmarks disponíveis
SELECT 
    p.title as problema,
    b.base_time_cpp,
    b.adjustment_factor_python,
    b.status,
    b.repetitions,
    b.median_cpp,
    b.median_python,
    b.is_reliable,
    b.created_at
FROM benchmarks b
JOIN problems p ON b.problem_id = p.id
ORDER BY b.created_at DESC;

-- Estatísticas de benchmarks
SELECT 
    status,
    COUNT(*) as quantidade,
    AVG(adjustment_factor_python) as fator_medio_python,
    AVG(base_time_cpp) as tempo_medio_cpp
FROM benchmarks
GROUP BY status;

-- 5. EXPLORAR SUBMISSIONS
-- =====================================================

-- Submissions por linguagem e status
SELECT 
    language,
    status,
    COUNT(*) as quantidade
FROM submissions
GROUP BY language, status
ORDER BY language, quantidade DESC;

-- Submissions recentes
SELECT 
    p.title as problema,
    s.language,
    s.status,
    s.result,
    s.execution_time_total,
    s.memory_usage_max,
    s.created_at
FROM submissions s
JOIN problems p ON s.problem_id = p.id
ORDER BY s.created_at DESC
LIMIT 20;

-- 6. ANÁLISES AVANÇADAS
-- =====================================================

-- Performance por linguagem
SELECT 
    s.language,
    COUNT(*) as total_submissions,
    AVG(s.execution_time_total) as tempo_medio,
    AVG(s.memory_usage_max) as memoria_media,
    SUM(CASE WHEN s.status = 'COMPLETED' THEN 1 ELSE 0 END) as concluidas,
    ROUND(
        (SUM(CASE WHEN s.status = 'COMPLETED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 
        2
    ) as taxa_sucesso_pct
FROM submissions s
GROUP BY s.language;

-- Problemas mais difíceis (mais submissions com erro)
SELECT 
    p.title,
    p.difficulty,
    COUNT(s.id) as total_submissions,
    SUM(CASE WHEN s.status != 'COMPLETED' THEN 1 ELSE 0 END) as com_erro,
    ROUND(
        (SUM(CASE WHEN s.status != 'COMPLETED' THEN 1 ELSE 0 END) * 100.0 / COUNT(s.id)), 
        2
    ) as taxa_erro_pct
FROM problems p
LEFT JOIN submissions s ON p.id = s.problem_id
GROUP BY p.id, p.title, p.difficulty
HAVING COUNT(s.id) > 0
ORDER BY taxa_erro_pct DESC;

-- 7. ANÁLISE DE RESULTADOS DE TESTE
-- =====================================================

-- Resultados de teste por tipo de erro
SELECT 
    sr.error_type,
    COUNT(*) as quantidade
FROM submission_results sr
WHERE sr.error_type IS NOT NULL
GROUP BY sr.error_type
ORDER BY quantidade DESC;

-- Test cases que mais causam erro
SELECT 
    p.title as problema,
    tc.name as test_case,
    COUNT(sr.id) as execucoes,
    SUM(CASE WHEN sr.passed = 0 THEN 1 ELSE 0 END) as falhas,
    ROUND(
        (SUM(CASE WHEN sr.passed = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(sr.id)), 
        2
    ) as taxa_falha_pct
FROM submission_results sr
JOIN test_cases tc ON sr.test_case_id = tc.id
JOIN problems p ON tc.problem_id = p.id
GROUP BY tc.id, p.title, tc.name
HAVING COUNT(sr.id) > 0
ORDER BY taxa_falha_pct DESC;

-- 8. QUERIES PARA DEBUGGING
-- =====================================================

-- Ver estrutura das tabelas
SELECT sql FROM sqlite_master WHERE type='table';

-- Ver últimos logs de erro
SELECT 
    s.id,
    p.title,
    s.language,
    s.status,
    s.error_message,
    s.created_at
FROM submissions s
JOIN problems p ON s.problem_id = p.id
WHERE s.error_message IS NOT NULL
ORDER BY s.created_at DESC
LIMIT 10;

-- =====================================================
-- COMO USAR ESSAS CONSULTAS:
-- =====================================================
-- 1. Copie e cole qualquer consulta no DBeaver
-- 2. Execute com Ctrl+Enter (ou Cmd+Enter no Mac)
-- 3. Use os resultados para analisar o comportamento do sistema
-- 4. Modifique as consultas conforme necessário
-- =====================================================
