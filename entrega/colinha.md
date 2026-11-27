# Colinha — Projeto Final

**Fluxo em uma linha:**
`Video_Games.csv` → **NB01** → `jogos_preparados.csv` → **NB02** → `resumo_analise.json` → **NB03 + llm_client.py** → `interacao_llm.json` + conclusão

---

## Pergunta inicial

> **Quais jogos apresentam perfis semelhantes de vendas e avaliação, e quais se afastam do padrão do mercado?**

---

## 1. Notebook 01 — Carrega, limpa e prepara

Carrega o dataset bruto (`Video_Games.csv`, 16.719 × 16), aplica as técnicas de preparação e gera a base `jogos_preparados.csv`.

**Técnicas utilizadas:**
- **Verificação de tipos** — identificação de colunas numéricas que vieram como texto.
- **Conversão de tipos** — números em texto e o valor `"tbd"` são convertidos para número ou ausente.
- **Análise de valores ausentes** — contagem e percentual de ausência por coluna.
- **Detecção de duplicidades** — linhas idênticas e jogos repetidos na mesma plataforma.
- **Detecção de outliers por IQR** — identificação dos valores fora do padrão, sem remoção.
- **Engenharia de atributos** — participação de cada região nas vendas e transformação logarítmica das vendas.
- **Seleção de atributos** — escolha dos 7 atributos usados na mineração.

**O que foi removido (e por quê):**
- **Duplicados exatos** — removidos; no dataset eram zero.
- **Jogos repetidos de mesmo nome + plataforma** — **mantidos**, pois são edições/relançamentos diferentes.
- **Registros sem vendas globais ou com venda zero** — removidos, pois não é possível calcular a participação regional dividindo por zero.
- **Registros sem os 7 atributos completos** — removidos, pois distância e agrupamento exigem dados completos.
- **Colunas removidas da modelagem:**
  - `Global_Sales` bruta — substituída pelo log das vendas;
  - `Critic_Count` e `User_Count` — medem a quantidade de avaliações, não a qualidade;
  - `Name`, `Platform`, `Genre`, `Publisher`, `Developer` e `Rating` — identificação/categorias, usadas apenas para descrever os grupos.

**O que NÃO foi removido (e por quê):**
- **Outliers** — são justamente o objeto da pergunta ("quais se afastam do padrão"); apenas medidos.
- **Valores ausentes** — a ausência é informação da fonte (cobertura do Metacritic) e não foi preenchida artificialmente.

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
