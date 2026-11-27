# Colinha — Projeto Final

**Fluxo em uma linha:**
`Video_Games.csv` → **NB01** → `jogos_preparados.csv` → **NB02** → `resumo_analise.json` → **NB03 + llm_client.py** → `interacao_llm.json` + conclusão

---

## Pergunta inicial

> **Quais jogos apresentam perfis semelhantes de vendas e avaliação, e quais se afastam do padrão do mercado?**

---

## 1. Notebook 01 — Carrega, limpa e prepara

Carrega o dataset bruto (`data/raw/Video_Games.csv`, 16.719 × 16), limpa e gera a base preparada
(`data/processed/jogos_preparados.csv`).

**Limpeza feita com:**
- `pd.to_numeric(..., errors="coerce")` — converte texto e `"tbd"` em número ou ausente (`NaN`);
- `isna().sum()` / `isna().mean()` — mede os valores ausentes;
- `duplicated()` / `drop_duplicates()` — identifica e remove duplicados exatos;
- **IQR** (`quantile` 25/75) — detecta possíveis outliers (**não remove**: eles são o objeto da pergunta);
- engenharia de atributos — **shares regionais** (venda da região ÷ total regional) e **`log1p(Global_Sales)`**;
- `dropna(subset=...)` — mantém apenas os registros com os 7 atributos completos.

**Resultado:** 7.017 linhas × 22 colunas.

---

## 2. Notebook 02 — A mineração em si

Entrada: `jogos_preparados.csv`.

Objetivo: **responder à pergunta inicial** aplicando as técnicas da disciplina.

**Estratégias aplicadas:**
- **Z-score** (`StandardScaler`) — padroniza os 7 atributos;
- **Distância Euclidiana** (`NearestNeighbors`) — encontra os jogos mais semelhantes e os mais atípicos;
- **K-Means** — agrupa os jogos em perfis;
- **Método do cotovelo** (WCSS) — apoia a escolha de k;
- **Silhouette** — valida a qualidade dos grupos (k = 6 escolhido).

**Saída:** `saidas/resumo_analise.json` — metadados, 6 grupos, 10 pares mais semelhantes e 10 jogos mais atípicos.

---

## 3. `llm_client.py` — Conexão com a API

- Lê a **chave de API** (`DEEPSEEK_API_KEY`) do arquivo `.env`.
- Cria a **conexão com a API do DeepSeek**, que é compatível com o SDK da OpenAI (`base_url` + modelo `deepseek-chat`).
- O modelo é **pago** e a chave já está adquirida.
- `interpretar_resultados()` — envia o resumo + a pergunta e devolve o texto da LLM.
- `registrar_interacao()` — salva o prompt e a resposta.

---

## 4. Notebook 03 — Análise pela LLM e verificação

- Carrega `resumo_analise.json`.
- Importa as funções de `llm_client.py`.
- Executa a interpretação na LLM.
- Salva o resultado em `saidas/interacao_llm.json`.
- **Verificação obrigatória:** a resposta **não é aceita automaticamente**; os números citados pela IA são conferidos contra o resumo.
- Com a resposta da IA **junto a uma análise humana**, é possível responder à pergunta inicial.

---

## Resposta resumida

Os **7.017 jogos** se organizam em **6 perfis**, definidos principalmente pela **região de vendas**
(América do Norte, Japão, Europa ou equilibrado). Existem jogos **semelhantes** (mesmo perfil regional
e faixas próximas de nota/porte) e **atípicos** (vendas extremas ou combinações incomuns de crítica e
nota de usuário). **Vendas e avaliação não caminham sempre juntas**, e a separação é **moderada**
(silhouette ≈ 0,25) — os grupos descrevem o mercado, mas não são fronteiras rígidas.
