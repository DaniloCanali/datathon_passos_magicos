# 🔮 Passos Mágicos - Datathon FIAP Fase 5

Projeto desenvolvido para o **POSTECH – Data Analytics – Datathon – Fase 5**, em parceria com a **Associação Passos Mágicos**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://SEU-APP.streamlit.app)

---

## 🎯 Objetivo

Analisar os dados do **PEDE (Pesquisa Extensiva do Desenvolvimento Educacional)** e desenvolver um modelo preditivo para identificar alunos em risco de defasagem educacional.

---

## 📁 Estrutura do Projeto

```
.
├── app/
│   └── app.py                    # Aplicação Streamlit
├── notebooks/
│   └── datathon_notebook_completo.ipynb   # Análise + Modelo ML
├── models/
│   ├── modelo_risco_defasagem.pkl    # Modelo Gradient Boosting
│   ├── scaler.pkl                    # Scaler para normalização
│   └── features.pkl                  # Lista de features
├── docs/
│   └── Apresentacao_Passos_Magicos_Datathon.pptx
├── .streamlit/
│   └── config.toml               # Configuração do tema
├── requirements.txt
├── .python-version
└── README.md
```

---

## 📊 Indicadores Analisados

| Sigla | Nome | Descrição |
|-------|------|-----------|
| **IAA** | Autoavaliação | Percepção do aluno sobre si mesmo |
| **IEG** | Engajamento | Participação nas atividades |
| **IPS** | Psicossocial | Bem-estar psicossocial |
| **IDA** | Aprendizagem | Desempenho acadêmico |
| **IPV** | Ponto de Virada | Transformação comportamental |
| **IAN** | Adequação ao Nível | Adequação série/idade |
| **INDE** | Desenvolvimento Educacional | Índice geral ponderado |

---

## 🔍 Principais Descobertas

| # | Insight | Impacto |
|---|---------|---------|
| 1 | **69.9% dos alunos acima do nível** | Programa muito eficaz |
| 2 | **IEG correlação 0.80 com INDE** | Engajamento é chave |
| 3 | **Autoavaliação 2.2 pts acima do real** | Trabalhar metacognição |
| 4 | **Fase 3 tem 30% de Quartzo** | Ponto crítico |
| 5 | **IPV é maior preditor (44.6%)** | Ponto de Virada transforma |

---

## 🤖 Modelo de Machine Learning

| Métrica | Valor |
|---------|-------|
| **Algoritmo** | Gradient Boosting |
| **Acurácia** | 80.2% |
| **ROC-AUC** | 0.813 |
| **F1-Score** | 0.61 |

### Importância das Features:
```
IPV (Ponto de Virada)  ████████████████████████  44.6%
IEG (Engajamento)      ███████████████          28.9%
Fase                   ██████                   11.5%
Idade                  ███                       6.2%
IAA                    ██                        3.3%
```

---

## 🌐 Aplicação Streamlit

A aplicação permite:
- ✅ Calcular risco individual de alunos
- ✅ Análise em lote via upload de planilha
- ✅ Dashboard com principais indicadores
- ✅ Exportar lista de alunos em risco

**Acesse:** [[SEU-LINK.streamlit.app](https://SEU-LINK.streamlit.app)](https://datathonpaappsmagicos-wijkucagk5k2xosfgnjhpl.streamlit.app/)

---

## ▶️ Como Executar

### 1. Clonar repositório
```bash
git clone https://github.com/SEU-USUARIO/datathon_passos_magicos.git
cd datathon_passos_magicos
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar Streamlit
```bash
streamlit run app/app.py
```

---

## 📋 Recomendações para Passos Mágicos

1. **Sistema de Alerta Precoce** - Implementar modelo preditivo
2. **Foco em Engajamento** - Criar ações para elevar IEG
3. **Atenção à Fase 3** - Reforçar acompanhamento
4. **Trabalho de Metacognição** - Alinhar IAA com IDA
5. **Expandir Psicologia** - 47% não atendidos

---

## 🎓 Sobre

**Projeto:** Datathon PosTech FIAP - Data Analytics - Fase 5

**Parceiro:** Associação Passos Mágicos (32 anos transformando vidas em Embu-Guaçu/SP)

---

## 📹 Vídeo de Apresentação

[Link do vídeo - 5 minutos]

---

<p align="center">
  🔮 <strong>Transformando dados em ações para mudar vidas</strong> 🔮
</p>
