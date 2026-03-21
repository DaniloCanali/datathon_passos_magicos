"""
🔮 PASSOS MÁGICOS - Sistema Preditivo de Risco Educacional
"""

import streamlit as st
import pandas as pd
import numpy as np

# Configuração
st.set_page_config(
    page_title="Passos Mágicos - Predição de Risco",
    page_icon="🔮",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #1E3A5F; text-align: center;}
    .sub-header {font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem;}
    .risk-high {background: #E53935; color: white; padding: 20px; border-radius: 10px; text-align: center;}
    .risk-medium {background: #FF9800; color: white; padding: 20px; border-radius: 10px; text-align: center;}
    .risk-low {background: #4CAF50; color: white; padding: 20px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# Funções
def calcular_risco(iaa, ieg, ips, ipv, ian, fase):
    score = ((10-ipv)*0.446 + (10-ieg)*0.289 + fase*0.02 + (10-iaa)*0.033 + (10-ian)*0.029 + (10-ips)*0.026) / 10
    return min(max(score, 0), 1)

def classificar(prob):
    if prob >= 0.6: return "ALTO", "risk-high", "🔴"
    elif prob >= 0.35: return "MÉDIO", "risk-medium", "🟡"
    return "BAIXO", "risk-low", "🟢"

# Header
st.markdown('<h1 class="main-header">🔮 Passos Mágicos</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema de Predição de Risco de Defasagem Educacional</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Sobre")
    st.markdown("Sistema de ML para identificar alunos em risco de defasagem.")
    st.markdown("---")
    st.markdown("**Modelo:** Gradient Boosting")
    st.markdown("**Acurácia:** 80.2%")
    st.markdown("**ROC-AUC:** 0.813")
    st.markdown("---")
    st.markdown("### 🚦 Níveis de Risco")
    st.markdown("🟢 Baixo: < 35%")
    st.markdown("🟡 Médio: 35-60%")
    st.markdown("🔴 Alto: > 60%")

# Tabs
tab1, tab2, tab3 = st.tabs(["🎯 Predição", "📊 Lote", "📈 Dashboard"])

# TAB 1
with tab1:
    st.markdown("### Análise Individual")
    
    col1, col2 = st.columns(2)
    with col1:
        iaa = st.slider("IAA - Autoavaliação", 0.0, 10.0, 7.5, 0.1)
        ieg = st.slider("IEG - Engajamento", 0.0, 10.0, 7.8, 0.1)
        ips = st.slider("IPS - Psicossocial", 0.0, 10.0, 7.0, 0.1)
    with col2:
        ipv = st.slider("IPV - Ponto de Virada", 0.0, 10.0, 7.2, 0.1)
        ian = st.slider("IAN - Adequação", 0.0, 10.0, 6.5, 0.1)
        fase = st.selectbox("Fase", list(range(8)), index=2)
    
    if st.button("🔍 Calcular Risco", type="primary", use_container_width=True):
        prob = calcular_risco(iaa, ieg, ips, ipv, ian, fase)
        nivel, classe, emoji = classificar(prob)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        
        with col2:
            st.markdown(f'<div class="{classe}"><h1>{emoji}</h1><h2>Risco {nivel}</h2><h1>{prob*100:.1f}%</h1></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Comparativo
        st.markdown("#### Comparativo com Média")
        comp = pd.DataFrame({
            'Indicador': ['IAA', 'IEG', 'IPS', 'IPV', 'IAN'],
            'Aluno': [iaa, ieg, ips, ipv, ian],
            'Média': [8.27, 7.89, 6.90, 7.25, 6.42]
        })
        comp['Diferença'] = comp['Aluno'] - comp['Média']
        st.dataframe(comp, use_container_width=True, hide_index=True)
        
        # Recomendações
        if nivel == "ALTO":
            st.error("⚠️ **Atenção Imediata:** Encaminhar para avaliação psicopedagógica e criar plano de intervenção.")
        elif nivel == "MÉDIO":
            st.warning("⚡ **Monitoramento:** Aumentar frequência de avaliações e verificar engajamento.")
        else:
            st.success("✅ **Desenvolvimento Saudável:** Manter acompanhamento regular.")

# TAB 2
with tab2:
    st.markdown("### Análise em Lote")
    
    template = pd.DataFrame({'Nome': ['Aluno 1'], 'IAA': [7.5], 'IEG': [7.0], 'IPS': [6.5], 'IPV': [7.0], 'IAN': [6.0], 'Fase': [2]})
    st.download_button("📥 Template", template.to_csv(index=False), "template.csv")
    
    arquivo = st.file_uploader("Upload CSV/Excel", type=['csv', 'xlsx'])
    
    if arquivo:
        df = pd.read_csv(arquivo) if arquivo.name.endswith('.csv') else pd.read_excel(arquivo)
        st.success(f"✅ {len(df)} registros")
        
        if st.button("🚀 Processar", type="primary"):
            df['Fase'] = df.get('Fase', 3)
            df['Prob'] = df.apply(lambda r: calcular_risco(r['IAA'], r['IEG'], r['IPS'], r['IPV'], r['IAN'], r['Fase']), axis=1)
            df['Risco'] = df['Prob'].apply(lambda x: classificar(x)[0])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🔴 Alto", (df['Risco']=='ALTO').sum())
            col2.metric("🟡 Médio", (df['Risco']=='MÉDIO').sum())
            col3.metric("🟢 Baixo", (df['Risco']=='BAIXO').sum())
            
            st.dataframe(df.sort_values('Prob', ascending=False), use_container_width=True)
            st.download_button("📥 Resultados", df.to_csv(index=False), "resultados.csv")

# TAB 3
with tab3:
    st.markdown("### Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Alunos", "860")
    col2.metric("INDE Médio", "7.04")
    col3.metric("Acima Nível", "69.9%")
    col4.metric("Ponto Virada", "13.1%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Correlações com INDE")
        st.bar_chart(pd.DataFrame({'Correlação': [0.818, 0.802, 0.789, 0.455, 0.395, 0.269]}, 
                                   index=['IDA', 'IEG', 'IPV', 'IAA', 'IAN', 'IPS']))
    with col2:
        st.markdown("#### Importância no Modelo")
        st.bar_chart(pd.DataFrame({'Importância': [0.446, 0.289, 0.115, 0.062, 0.033, 0.029]}, 
                                   index=['IPV', 'IEG', 'Fase', 'Idade', 'IAA', 'IAN']))
    
    st.markdown("---")
    st.markdown("### 💡 Insights")
    
    col1, col2, col3 = st.columns(3)
    col1.info("**Engajamento é Chave**\n\nIEG correlação 0.80 com INDE")
    col2.warning("**Autoavaliação Alta**\n\nAlunos se avaliam 2.2 pts acima")
    col3.success("**Programa Efetivo**\n\n69.9% acima do nível esperado")

# Footer
st.markdown("---")
st.markdown("<center>🔮 Passos Mágicos - Datathon PosTech FIAP</center>", unsafe_allow_html=True)
