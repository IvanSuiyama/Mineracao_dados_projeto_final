# Projeto Final — Mineração de Dados com apoio de LLM via API

**Aluno:** Ivan Suiyama Silva · 6°DSM
**Tema:** Perfis e similaridades no mercado de videogames

> *Quais jogos apresentam perfis semelhantes de vendas e avaliação, e quais se afastam do padrão do mercado?*

---

## Como abrir o projeto

O ambiente já está pronto. O kernel se chama **`Python (Mineracao LLM)`**.

```bash
# na pasta do projeto
jupyter lab
# ou
jupyter notebook
```

Ao abrir um notebook, selecione o kernel **Python (Mineracao LLM)**.

Para recriar o ambiente do zero:

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name mineracao-llm --display-name "Python (Mineracao LLM)"
```

---

## Ordem de execução

| # | Notebook | O que faz | Status |
|---|---|---|---|
| 01 | `01_entendimento_e_qualidade.ipynb` | Entende o dataset, trata tipos/nulos, cria atributos | ✅ executado |
| 02 | `02_similaridade_e_clusters.ipynb` | Z-score, distância Euclidiana, K-Means, perfis | ✅ executado |
| 03 | `03_llm_interpretacao.ipynb` | Envia o resumo agregado à API e registra a resposta | ✅ executado |

---

## Configurar a chave da API (DeepSeek)

1. Copie o modelo de configuração:

   ```bash
   cp .env.example .env
   ```

2. Edite o `.env` e cole **sua** chave:

   ```
   DEEPSEEK_API_KEY=sk-...
   ```

3. Pronto. O notebook 03 lê a chave automaticamente.

**A chave nunca vai para o notebook nem para o Git** — o `.env` está no `.gitignore`.
Na entrega, não inclua o `.env`.

---

## Estrutura

```
├── data/
│   ├── raw/Video_Games.csv          # dataset original (16.719 linhas)
│   └── processed/jogos_preparados.csv
├── notebooks/
│   ├── 01_entendimento_e_qualidade.ipynb
│   ├── 02_similaridade_e_clusters.ipynb
│   └── 03_llm_interpretacao.ipynb
├── src/llm_client.py                # cliente da API (compatível OpenAI)
├── saidas/
│   ├── resumo_analise.json           # resumo agregado enviado à LLM
│   └── interacao_llm.json            # prompt + resposta registrados
├── requirements.txt
└── .env.example
```

---

## Dataset

**Video Game Sales with Ratings** — VGChartz (vendas) + Metacritic (notas).
Fonte original: <https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings>
Cópia pública usada: repositório `dimaggiofrancesco/DATA_ANALYSIS-Videogames_sales_and_ratings`.

16.719 registros · 16 atributos · vendas em milhões · **sem dados pessoais**.

---

## Resultados já obtidos

- Base preparada: **7.017 registros** com todos os atributos (recorte natural por notas completas).
- Atributos de modelagem: shares regionais, `log1p(Global_Sales)`, `Critic_Score`, `User_Score`.
- **k = 6 grupos**, escolhido automaticamente pelo silhouette (≈ 0,2526 — estrutura fraca/moderada).
- Resumo agregado em `saidas/resumo_analise.json`.
- LLM chamada via API e resposta registrada em `saidas/interacao_llm.json`.
- Verificação automática: nenhuma estatística inventada pela LLM.

### Perfis encontrados

| Grupo | % | Vendas médias | Crítica | User | Perfil |
|---|---|---|---|---|---|
| 0 | 15,7% | 0,28M | 49,5 | 5,0 | Baixa avaliação, forte na América do Norte |
| 1 | 7,9% | 0,49M | 71,4 | 7,8 | Forte no Japão (62%), RPG |
| 2 | 12,3% | 3,59M | 83,4 | 7,8 | Sucessos globais |
| 3 | 28,8% | 0,32M | 72,9 | 7,7 | Dominado pela América do Norte (79%) |
| 4 | 8,7% | 0,15M | 74,5 | 7,1 | Forte na Europa (88%) |
| 5 | 26,6% | 0,51M | 71,8 | 7,4 | Equilibrado NA/Europa |

### Pendências

- Revisar o checklist final do PDF antes de entregar.
- (Opcional) incluir vendas digitais e período mais recente como trabalho futuro.

### Entregável

- **`entrega/Projeto_Final_Mineracao_Dados_Ivan_Suiyama.pdf`** — relatório enxuto (sem código):
  capa com dados, pergunta e técnicas; Notebook 01, Notebook 02, `llm_client.py` e Notebook 03.
