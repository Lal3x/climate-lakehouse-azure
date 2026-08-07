# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # Pipeline Gold - Análises Climáticas
# MAGIC
# MAGIC **Catálogo:** `atmos.gold`
# MAGIC **Fonte:** `atmos.silver.climate_unified`
# MAGIC
# MAGIC Ordem de execução das células abaixo:
# MAGIC 1. `perfil_sazonal_mensal_cidade` — consolida INMET x Visual Crossing por cidade
# MAGIC 2. `perfil_sazonal_mensal` — versão por estação/`id_estacao` (sem consolidar fontes)
# MAGIC 3. `perfil_sazonal_estacao` — agregação por estação do ano (verão/outono/inverno/primavera)
# MAGIC 4. `anomalia_climatologica_mensal` — desvio em relação à normal histórica (depende da #1)
# MAGIC 5. `ranking_meses_extremos` — top 5 meses mais quentes/frios/chuvosos/secos (depende da #1)
# MAGIC 6. `tendencia_interanual_mensal` — regressão linear simples, °C por ano (depende da #1)
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS ATMOS
# MAGIC MANAGED LOCATION 'abfss://atmos-lading-eastus-001@saatmosdeveastus001.dfs.core.windows.net/';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS ATMOS.GOLD;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Perfil sazonal mensal por cidade (consolidado, resolvendo INMET x Visual Crossing)
# MAGIC
# MAGIC Como `id_estacao` diverge entre as fontes para a mesma cidade, esta tabela
# MAGIC prioriza o INMET quando ambas as fontes têm dado no mesmo dia/cidade,
# MAGIC evitando dupla contagem, e registra qual fonte prevaleceu para auditoria.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE atmos.gold.perfil_sazonal_mensal_cidade AS
# MAGIC WITH diario AS (
# MAGIC     SELECT
# MAGIC         data_observacao,
# MAGIC         cidade,
# MAGIC         sistema_origem,
# MAGIC         AVG(temperatura_c)     AS temp_media_dia,
# MAGIC         MAX(temperatura_max_c) AS temp_max_dia,
# MAGIC         MIN(temperatura_min_c) AS temp_min_dia,
# MAGIC         SUM(precipitacao_mm)   AS precipitacao_dia_mm,
# MAGIC         AVG(umidade_pct)       AS umidade_media_dia,
# MAGIC         AVG(pressao_hpa)       AS pressao_media_dia_hpa
# MAGIC     FROM atmos.silver.climate_unified
# MAGIC     GROUP BY data_observacao, cidade, sistema_origem
# MAGIC ),
# MAGIC
# MAGIC diario_priorizado AS (
# MAGIC     -- prioriza INMET quando as duas fontes cobrem o mesmo dia/cidade
# MAGIC     SELECT *,
# MAGIC         ROW_NUMBER() OVER (
# MAGIC             PARTITION BY data_observacao, cidade
# MAGIC             ORDER BY CASE WHEN sistema_origem = 'inmet' THEN 1 ELSE 2 END
# MAGIC         ) AS prioridade_fonte
# MAGIC     FROM diario
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     cidade,
# MAGIC     YEAR(data_observacao)  AS ano,
# MAGIC     MONTH(data_observacao) AS mes,
# MAGIC     ROUND(AVG(temp_media_dia), 2)              AS temperatura_media_c,
# MAGIC     ROUND(AVG(temp_max_dia), 2)                AS temperatura_maxima_media_c,
# MAGIC     ROUND(AVG(temp_min_dia), 2)                AS temperatura_minima_media_c,
# MAGIC     ROUND(MAX(temp_max_dia), 2)                AS temperatura_maxima_abs_c,
# MAGIC     ROUND(MIN(temp_min_dia), 2)                AS temperatura_minima_abs_c,
# MAGIC     ROUND(SUM(precipitacao_dia_mm), 2)         AS precipitacao_total_mm,
# MAGIC     ROUND(AVG(umidade_media_dia), 2)           AS umidade_media_pct,
# MAGIC     ROUND(AVG(pressao_media_dia_hpa), 2)       AS pressao_media_hpa,
# MAGIC     ROUND(AVG(temp_max_dia - temp_min_dia), 2) AS amplitude_termica_media_c,
# MAGIC     COUNT(DISTINCT data_observacao)            AS dias_com_dados,
# MAGIC     MODE(sistema_origem)                       AS fonte_predominante,
# MAGIC     from_utc_timestamp(CURRENT_TIMESTAMP(), 'America/Sao_Paulo') AS timestamp_processamento
# MAGIC FROM diario_priorizado
# MAGIC WHERE prioridade_fonte = 1
# MAGIC GROUP BY cidade, YEAR(data_observacao), MONTH(data_observacao)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Perfil sazonal mensal por estação (mantém `id_estacao`, sem consolidar fontes)
# MAGIC
# MAGIC Use esta versão se precisar granularidade por estação/fonte (ex: comparar
# MAGIC INMET vs Visual Crossing lado a lado). Para visão única por cidade, use a
# MAGIC tabela da célula #1.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE atmos.gold.perfil_sazonal_mensal AS
# MAGIC WITH diario AS (
# MAGIC     SELECT
# MAGIC         data_observacao,
# MAGIC         id_estacao,
# MAGIC         cidade,
# MAGIC         AVG(temperatura_c)     AS temp_media_dia,
# MAGIC         MAX(temperatura_max_c) AS temp_max_dia,
# MAGIC         MIN(temperatura_min_c) AS temp_min_dia,
# MAGIC         SUM(precipitacao_mm)   AS precipitacao_dia_mm,
# MAGIC         AVG(umidade_pct)       AS umidade_media_dia,
# MAGIC         AVG(pressao_hpa)       AS pressao_media_dia_hpa
# MAGIC     FROM atmos.silver.climate_unified
# MAGIC     GROUP BY data_observacao, id_estacao, cidade
# MAGIC ),
# MAGIC
# MAGIC mensal AS (
# MAGIC     SELECT
# MAGIC         id_estacao,
# MAGIC         cidade,
# MAGIC         YEAR(data_observacao)                      AS ano,
# MAGIC         MONTH(data_observacao)                     AS mes,
# MAGIC         ROUND(AVG(temp_media_dia), 2)               AS temperatura_media_c,
# MAGIC         ROUND(AVG(temp_max_dia), 2)                 AS temperatura_maxima_media_c,
# MAGIC         ROUND(AVG(temp_min_dia), 2)                 AS temperatura_minima_media_c,
# MAGIC         ROUND(MAX(temp_max_dia), 2)                 AS temperatura_maxima_abs_c,
# MAGIC         ROUND(MIN(temp_min_dia), 2)                 AS temperatura_minima_abs_c,
# MAGIC         ROUND(SUM(precipitacao_dia_mm), 2)          AS precipitacao_total_mm,
# MAGIC         ROUND(AVG(umidade_media_dia), 2)            AS umidade_media_pct,
# MAGIC         ROUND(AVG(pressao_media_dia_hpa), 2)        AS pressao_media_hpa,
# MAGIC         ROUND(AVG(temp_max_dia - temp_min_dia), 2)  AS amplitude_termica_media_c,
# MAGIC         COUNT(DISTINCT data_observacao)             AS dias_com_dados,
# MAGIC         from_utc_timestamp(CURRENT_TIMESTAMP(), 'America/Sao_Paulo') AS timestamp_processamento
# MAGIC     FROM diario
# MAGIC     GROUP BY id_estacao, cidade, YEAR(data_observacao), MONTH(data_observacao)
# MAGIC )
# MAGIC
# MAGIC SELECT * FROM mensal

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Perfil sazonal por estação do ano (Verão/Outono/Inverno/Primavera)
# MAGIC
# MAGIC Considera o hemisfério sul. Dezembro é contado como início do verão do
# MAGIC "ano-estação" seguinte (ex: dez/2024 + jan/2025 + fev/2025 = verão 2025).

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE atmos.gold.perfil_sazonal_estacao AS
# MAGIC WITH mensal_com_estacao AS (
# MAGIC     SELECT
# MAGIC         *,
# MAGIC         CASE
# MAGIC             WHEN mes IN (12, 1, 2)  THEN 'Verão'
# MAGIC             WHEN mes IN (3, 4, 5)   THEN 'Outono'
# MAGIC             WHEN mes IN (6, 7, 8)   THEN 'Inverno'
# MAGIC             WHEN mes IN (9, 10, 11) THEN 'Primavera'
# MAGIC         END AS estacao_ano,
# MAGIC         CASE WHEN mes = 12 THEN ano + 1 ELSE ano END AS ano_estacao
# MAGIC     FROM atmos.gold.perfil_sazonal_mensal_cidade
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     cidade,
# MAGIC     ano_estacao,
# MAGIC     estacao_ano,
# MAGIC     ROUND(AVG(temperatura_media_c), 2)        AS temp_media_estacao_c,
# MAGIC     ROUND(SUM(precipitacao_total_mm), 2)      AS precipitacao_total_estacao_mm,
# MAGIC     ROUND(AVG(amplitude_termica_media_c), 2)  AS amplitude_media_estacao_c,
# MAGIC     ROUND(MAX(temperatura_maxima_abs_c), 2)   AS temp_maxima_abs_estacao_c,
# MAGIC     ROUND(MIN(temperatura_minima_abs_c), 2)   AS temp_minima_abs_estacao_c,
# MAGIC     SUM(dias_com_dados)                       AS dias_com_dados
# MAGIC FROM mensal_com_estacao
# MAGIC GROUP BY cidade, ano_estacao, estacao_ano

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Anomalia climatológica mensal (desvio em relação à "normal" histórica)
# MAGIC
# MAGIC ⚠️ **Atenção:** só é estatisticamente robusta com vários anos de histórico
# MAGIC por cidade/mês. Com poucos anos, a "normal" fica instável e a anomalia
# MAGIC perde significado.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE atmos.gold.anomalia_climatologica_mensal AS
# MAGIC WITH normal_climatologica AS (
# MAGIC     SELECT
# MAGIC         cidade,
# MAGIC         mes,
# MAGIC         ROUND(AVG(temperatura_media_c), 2)   AS temp_normal_c,
# MAGIC         ROUND(AVG(precipitacao_total_mm), 2) AS precipitacao_normal_mm
# MAGIC     FROM atmos.gold.perfil_sazonal_mensal_cidade
# MAGIC     GROUP BY cidade, mes
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     m.cidade,
# MAGIC     m.ano,
# MAGIC     m.mes,
# MAGIC     m.temperatura_media_c,
# MAGIC     n.temp_normal_c,
# MAGIC     ROUND(m.temperatura_media_c - n.temp_normal_c, 2) AS anomalia_temp_c,
# MAGIC     m.precipitacao_total_mm,
# MAGIC     n.precipitacao_normal_mm,
# MAGIC     ROUND(m.precipitacao_total_mm - n.precipitacao_normal_mm, 2) AS anomalia_precipitacao_mm,
# MAGIC     ROUND(
# MAGIC         (m.precipitacao_total_mm - n.precipitacao_normal_mm)
# MAGIC         / NULLIF(n.precipitacao_normal_mm, 0) * 100, 1
# MAGIC     ) AS anomalia_precipitacao_pct
# MAGIC FROM atmos.gold.perfil_sazonal_mensal_cidade m
# MAGIC JOIN normal_climatologica n
# MAGIC   ON m.cidade = n.cidade AND m.mes = n.mes
# MAGIC ORDER BY m.cidade, m.ano, m.mes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Ranking de meses mais extremos por cidade (top 5 em cada categoria)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE atmos.gold.ranking_meses_extremos AS
# MAGIC SELECT
# MAGIC     cidade,
# MAGIC     ano,
# MAGIC     mes,
# MAGIC     temperatura_maxima_abs_c,
# MAGIC     temperatura_minima_abs_c,
# MAGIC     precipitacao_total_mm,
# MAGIC     RANK() OVER (PARTITION BY cidade ORDER BY temperatura_maxima_abs_c DESC) AS rank_mes_mais_quente,
# MAGIC     RANK() OVER (PARTITION BY cidade ORDER BY temperatura_minima_abs_c ASC)  AS rank_mes_mais_frio,
# MAGIC     RANK() OVER (PARTITION BY cidade ORDER BY precipitacao_total_mm DESC)   AS rank_mes_mais_chuvoso,
# MAGIC     RANK() OVER (PARTITION BY cidade ORDER BY precipitacao_total_mm ASC)    AS rank_mes_mais_seco
# MAGIC FROM atmos.gold.perfil_sazonal_mensal_cidade
# MAGIC QUALIFY rank_mes_mais_quente <= 5
# MAGIC      OR rank_mes_mais_frio <= 5
# MAGIC      OR rank_mes_mais_chuvoso <= 5
# MAGIC      OR rank_mes_mais_seco <= 5

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Tendência interanual por mês (regressão linear simples: °C por ano)
# MAGIC
# MAGIC Exige no mínimo 5 anos de histórico por cidade/mês — ajuste o `HAVING`
# MAGIC conforme a profundidade real da sua base.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE atmos.gold.tendencia_interanual_mensal AS
# MAGIC SELECT
# MAGIC     cidade,
# MAGIC     mes,
# MAGIC     COUNT(DISTINCT ano)                                AS anos_disponiveis,
# MAGIC     ROUND(REGR_SLOPE(temperatura_media_c, ano), 4)     AS tendencia_temp_c_por_ano,
# MAGIC     ROUND(REGR_SLOPE(precipitacao_total_mm, ano), 4)   AS tendencia_precipitacao_mm_por_ano,
# MAGIC     ROUND(REGR_INTERCEPT(temperatura_media_c, ano), 2) AS intercepto_temp,
# MAGIC     ROUND(REGR_R2(temperatura_media_c, ano), 4)        AS r2_temp
# MAGIC FROM atmos.gold.perfil_sazonal_mensal_cidade
# MAGIC GROUP BY cidade, mes
# MAGIC HAVING COUNT(DISTINCT ano) >= 5
# MAGIC ORDER BY cidade, mes