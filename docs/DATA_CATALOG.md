# Catálogo de dados

## Bronze

| Tabela | Fonte | Granularidade |
| --- | --- | --- |
| `climate.bronze.inmet_estacao_raw` | INMET / BigQuery | Cadastro bruto de estação |
| `climate.bronze.inmet_microdados_raw` | INMET / BigQuery | Observação meteorológica bruta |
| `climate.bronze.visual_crossing_raw` | Visual Crossing | Payload climático bruto |

## Silver

| Tabela | Finalidade |
| --- | --- |
| `climate.silver.climate_inmet` | Dados do INMET tipados e enriquecidos com estação/cidade |
| `climate.silver.climate_visual_crossing` | Dados da Visual Crossing normalizados |
| `climate.silver.climate_unified` | Contrato comum entre as duas fontes |

### Contrato analítico comum

A Silver unificada contém campos equivalentes a:

| Campo | Significado |
| --- | --- |
| `data_observacao` | Data do registro meteorológico |
| `id_estacao` | Identificador da estação ou origem |
| `cidade` | Cidade normalizada |
| `sistema_origem` | `inmet` ou Visual Crossing |
| `temperatura_c` | Temperatura observada em °C |
| `temperatura_max_c` | Temperatura máxima em °C |
| `temperatura_min_c` | Temperatura mínima em °C |
| `precipitacao_mm` | Precipitação em milímetros |
| `umidade_pct` | Umidade relativa em percentual |
| `pressao_hpa` | Pressão climateférica em hPa |
| `data_ingestao` | Partição lógica da carga |

Confirme o schema efetivo no Unity Catalog, pois as fontes podem evoluir.

## Gold

| Tabela | Grão |
| --- | --- |
| `perfil_sazonal_mensal_cidade` | cidade, ano e mês |
| `perfil_sazonal_mensal` | estação, cidade, ano e mês |
| `perfil_sazonal_estacao` | cidade, ano-estação e estação do ano |
| `anomalia_climatologica_mensal` | cidade, ano e mês |
| `ranking_meses_extremos` | cidade, ano e mês extremo |
| `tendencia_interanual_mensal` | cidade e mês |

## Regras de negócio importantes

- O INMET prevalece na consolidação diária quando as duas fontes cobrem cidade e data iguais.
- As estações do ano seguem o hemisfério sul.
- Dezembro pertence ao verão do ano-estação seguinte.
- Rankings mantêm os cinco melhores resultados de cada categoria.
- Tendências exigem cinco ou mais anos disponíveis.
