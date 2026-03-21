"""
================================================================================
🔧 PASSOS MÁGICOS - TRATAMENTO DOS DADOS
================================================================================
Datathon PosTech FIAP - Fase 5
Limpeza, transformação e preparação dos dados para modelagem
================================================================================
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🔧 PASSOS MÁGICOS - TRATAMENTO DOS DADOS")
print("="*70)

# =============================================================================
# 1. CARREGAMENTO DOS DADOS BRUTOS
# =============================================================================
print("\n📂 ETAPA 1: Carregamento dos Dados Brutos")
print("-"*50)

df_raw = pd.read_excel('/mnt/user-data/uploads/BASE_DE_DADOS_PEDE_2024_-_DATATHON.xlsx')

print(f"✅ Base carregada: {df_raw.shape[0]} registros, {df_raw.shape[1]} colunas")
print(f"\n📋 Colunas originais:")
print(df_raw.columns.tolist())

# =============================================================================
# 2. ANÁLISE DE VALORES AUSENTES
# =============================================================================
print("\n\n📊 ETAPA 2: Análise de Valores Ausentes")
print("-"*50)

missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(1)
missing_df = pd.DataFrame({
    'Coluna': missing.index,
    'Ausentes': missing.values,
    'Percentual': missing_pct.values
})
missing_df = missing_df[missing_df['Ausentes'] > 0].sort_values('Ausentes', ascending=False)

print("\n📋 Colunas com valores ausentes:")
print(missing_df.to_string(index=False))

# =============================================================================
# 3. SELEÇÃO DE COLUNAS RELEVANTES
# =============================================================================
print("\n\n🎯 ETAPA 3: Seleção de Colunas Relevantes")
print("-"*50)

# Colunas que vamos usar na análise
colunas_identificacao = ['RA', 'Nome', 'Fase', 'Turma']
colunas_demograficas = ['Ano nasc', 'Idade 22', 'Gênero', 'Ano ingresso']
colunas_indicadores = ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN']
colunas_resultado = ['INDE 22', 'Pedra 22', 'Defas', 'Atingiu PV']
colunas_academicas = ['Matem', 'Portug', 'Inglês']

todas_colunas = colunas_identificacao + colunas_demograficas + colunas_indicadores + colunas_resultado + colunas_academicas

# Filtrar apenas colunas que existem
colunas_existentes = [col for col in todas_colunas if col in df_raw.columns]

print(f"✅ Colunas selecionadas: {len(colunas_existentes)}")
print(f"   Identificação: {[c for c in colunas_identificacao if c in df_raw.columns]}")
print(f"   Demográficas: {[c for c in colunas_demograficas if c in df_raw.columns]}")
print(f"   Indicadores: {[c for c in colunas_indicadores if c in df_raw.columns]}")
print(f"   Resultado: {[c for c in colunas_resultado if c in df_raw.columns]}")

df = df_raw[colunas_existentes].copy()

# =============================================================================
# 4. RENOMEAÇÃO DE COLUNAS
# =============================================================================
print("\n\n📝 ETAPA 4: Renomeação de Colunas")
print("-"*50)

rename_map = {
    'INDE 22': 'INDE',
    'Pedra 22': 'Pedra',
    'Idade 22': 'Idade',
    'Ano nasc': 'Ano_Nascimento',
    'Ano ingresso': 'Ano_Ingresso',
    'Atingiu PV': 'Ponto_de_Virada'
}

# Aplicar renomeação apenas para colunas que existem
rename_existente = {k: v for k, v in rename_map.items() if k in df.columns}
df = df.rename(columns=rename_existente)

print(f"✅ Colunas renomeadas: {list(rename_existente.keys())}")
print(f"   → {list(rename_existente.values())}")

# =============================================================================
# 5. TRATAMENTO DE TIPOS DE DADOS
# =============================================================================
print("\n\n🔄 ETAPA 5: Tratamento de Tipos de Dados")
print("-"*50)

# Converter indicadores para numérico
indicadores = ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE']
for col in indicadores:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"   ✅ {col} → float64")

# Converter Fase para inteiro
if 'Fase' in df.columns:
    df['Fase'] = pd.to_numeric(df['Fase'], errors='coerce').astype('Int64')
    print(f"   ✅ Fase → Int64")

# Converter Idade para inteiro
if 'Idade' in df.columns:
    df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce').astype('Int64')
    print(f"   ✅ Idade → Int64")

# Converter Ponto de Virada para binário
if 'Ponto_de_Virada' in df.columns:
    df['Ponto_de_Virada'] = df['Ponto_de_Virada'].map({'Sim': 1, 'Não': 0, 1: 1, 0: 0})
    print(f"   ✅ Ponto_de_Virada → binário (0/1)")

# =============================================================================
# 6. TRATAMENTO DE VALORES AUSENTES
# =============================================================================
print("\n\n🩹 ETAPA 6: Tratamento de Valores Ausentes")
print("-"*50)

# Estratégia: Imputação com mediana para indicadores numéricos
for col in indicadores:
    if col in df.columns:
        ausentes_antes = df[col].isnull().sum()
        if ausentes_antes > 0:
            mediana = df[col].median()
            df[col] = df[col].fillna(mediana)
            print(f"   ✅ {col}: {ausentes_antes} valores ausentes → preenchidos com mediana ({mediana:.2f})")

# Preencher Fase ausente com moda
if 'Fase' in df.columns and df['Fase'].isnull().sum() > 0:
    moda = df['Fase'].mode()[0]
    df['Fase'] = df['Fase'].fillna(moda)
    print(f"   ✅ Fase: valores ausentes → preenchidos com moda ({moda})")

# =============================================================================
# 7. CRIAÇÃO DE NOVAS FEATURES
# =============================================================================
print("\n\n✨ ETAPA 7: Criação de Novas Features (Feature Engineering)")
print("-"*50)

# 7.1 Classificação por Pedra baseada no INDE
if 'INDE' in df.columns:
    def classificar_pedra(inde):
        if pd.isna(inde):
            return 'Não classificado'
        elif inde < 5.506:
            return 'Quartzo'
        elif inde < 6.868:
            return 'Ágata'
        elif inde < 8.230:
            return 'Ametista'
        else:
            return 'Topázio'
    
    df['Pedra_Calculada'] = df['INDE'].apply(classificar_pedra)
    print("   ✅ Pedra_Calculada: classificação baseada no INDE")

# 7.2 Gap entre Autoavaliação e Desempenho
if 'IAA' in df.columns and 'IDA' in df.columns:
    df['Gap_IAA_IDA'] = df['IAA'] - df['IDA']
    print("   ✅ Gap_IAA_IDA: diferença entre autoavaliação e desempenho real")

# 7.3 Média dos indicadores acadêmicos
if 'IDA' in df.columns and 'IEG' in df.columns:
    df['Media_Academica'] = (df['IDA'] + df['IEG']) / 2
    print("   ✅ Media_Academica: média de IDA e IEG")

# 7.4 Indicador de Risco (variável target para ML)
if 'Defas' in df.columns and 'IDA' in df.columns:
    df['RISCO'] = ((df['Defas'] > 0) | (df['IDA'] < 5)).astype(int)
    risco_count = df['RISCO'].sum()
    print(f"   ✅ RISCO: variável target para ML ({risco_count} alunos em risco = {100*risco_count/len(df):.1f}%)")
elif 'IDA' in df.columns:
    df['RISCO'] = (df['IDA'] < 5).astype(int)
    risco_count = df['RISCO'].sum()
    print(f"   ✅ RISCO: variável target baseada em IDA < 5 ({risco_count} alunos)")

# 7.5 Faixa etária
if 'Idade' in df.columns:
    def faixa_etaria(idade):
        if pd.isna(idade):
            return 'Desconhecido'
        elif idade <= 10:
            return 'Criança (até 10)'
        elif idade <= 14:
            return 'Adolescente (11-14)'
        else:
            return 'Jovem (15+)'
    
    df['Faixa_Etaria'] = df['Idade'].apply(faixa_etaria)
    print("   ✅ Faixa_Etaria: categorização por idade")

# 7.6 Tempo no programa
if 'Ano_Ingresso' in df.columns:
    df['Tempo_Programa'] = 2022 - df['Ano_Ingresso']
    print("   ✅ Tempo_Programa: anos desde o ingresso")

# =============================================================================
# 8. TRATAMENTO DE OUTLIERS
# =============================================================================
print("\n\n📉 ETAPA 8: Análise de Outliers")
print("-"*50)

for col in ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN']:
    if col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        
        if outliers > 0:
            print(f"   ⚠️ {col}: {outliers} outliers detectados (mantidos para análise)")
        else:
            print(f"   ✅ {col}: sem outliers")

# Nota: Não removemos outliers pois podem ser casos reais importantes

# =============================================================================
# 9. VALIDAÇÃO DOS DADOS
# =============================================================================
print("\n\n✔️ ETAPA 9: Validação dos Dados Tratados")
print("-"*50)

print(f"\n📊 Shape final: {df.shape[0]} registros, {df.shape[1]} colunas")

print(f"\n📋 Colunas finais:")
print(df.columns.tolist())

print(f"\n📊 Tipos de dados:")
print(df.dtypes)

print(f"\n📊 Valores ausentes restantes:")
remaining_missing = df.isnull().sum()
remaining_missing = remaining_missing[remaining_missing > 0]
if len(remaining_missing) > 0:
    print(remaining_missing)
else:
    print("   ✅ Nenhum valor ausente!")

print(f"\n📊 Estatísticas dos indicadores tratados:")
indicadores_final = [col for col in ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE'] if col in df.columns]
print(df[indicadores_final].describe().round(2))

# =============================================================================
# 10. SALVAMENTO DOS DADOS TRATADOS
# =============================================================================
print("\n\n💾 ETAPA 10: Salvamento dos Dados Tratados")
print("-"*50)

# Salvar CSV tratado
output_path = '/mnt/user-data/outputs/dados_tratados.csv'
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"✅ Dados tratados salvos: {output_path}")

# Salvar Excel tratado
output_excel = '/mnt/user-data/outputs/dados_tratados.xlsx'
df.to_excel(output_excel, index=False)
print(f"✅ Dados tratados salvos: {output_excel}")

# =============================================================================
# RESUMO DO TRATAMENTO
# =============================================================================
print("\n\n" + "="*70)
print("📋 RESUMO DO TRATAMENTO DE DADOS")
print("="*70)

print(f"""
📂 DADOS ORIGINAIS:
   - Registros: {df_raw.shape[0]}
   - Colunas: {df_raw.shape[1]}

🔧 TRATAMENTOS REALIZADOS:
   1. ✅ Seleção de colunas relevantes
   2. ✅ Renomeação de colunas para padronização
   3. ✅ Conversão de tipos de dados
   4. ✅ Imputação de valores ausentes (mediana/moda)
   5. ✅ Criação de features derivadas
   6. ✅ Análise de outliers

✨ FEATURES CRIADAS:
   - Pedra_Calculada: classificação por INDE
   - Gap_IAA_IDA: autoavaliação - desempenho
   - Media_Academica: média de IDA e IEG
   - RISCO: variável target para ML
   - Faixa_Etaria: categorização por idade
   - Tempo_Programa: anos desde ingresso

📊 DADOS FINAIS:
   - Registros: {df.shape[0]}
   - Colunas: {df.shape[1]}
   - Valores ausentes: {df.isnull().sum().sum()}

💾 ARQUIVOS GERADOS:
   - dados_tratados.csv
   - dados_tratados.xlsx
""")

print("="*70)
print("✅ TRATAMENTO DE DADOS CONCLUÍDO!")
print("="*70)
