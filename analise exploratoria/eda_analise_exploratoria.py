"""
================================================================================
🔮 PASSOS MÁGICOS - ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
================================================================================
Datathon PosTech FIAP - Fase 5
Análise completa dos dados PEDE com visualizações
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 100

# Cores do tema Passos Mágicos
CORES = {
    'azul_escuro': '#1E3A5F',
    'azul_medio': '#2E5077',
    'laranja': '#FF6B35',
    'verde': '#4CAF50',
    'vermelho': '#E53935',
    'amarelo': '#FFC107',
    'roxo': '#9C27B0',
    'cinza': '#666666'
}

# Cores para as pedras
CORES_PEDRAS = {
    'Quartzo': '#A0A0A0',
    'Ágata': '#8B4513',
    'Ametista': '#9966CC',
    'Topázio': '#FFD700'
}

print("="*70)
print("🔮 PASSOS MÁGICOS - ANÁLISE EXPLORATÓRIA DE DADOS")
print("="*70)

# =============================================================================
# 1. CARREGAMENTO DOS DADOS
# =============================================================================
print("\n📂 Carregando dados...")

# Carregar base principal
df = pd.read_excel('/mnt/user-data/uploads/BASE_DE_DADOS_PEDE_2024_-_DATATHON.xlsx')

print(f"✅ Base carregada: {df.shape[0]} registros, {df.shape[1]} colunas")

# =============================================================================
# 2. VISÃO GERAL DOS DADOS
# =============================================================================
print("\n" + "="*70)
print("📊 VISÃO GERAL DOS DADOS")
print("="*70)

print(f"\n📋 Colunas disponíveis ({len(df.columns)}):")
print(df.columns.tolist())

print(f"\n📈 Tipos de dados:")
print(df.dtypes.value_counts())

print(f"\n📊 Valores ausentes:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_df = pd.DataFrame({'Ausentes': missing, '%': missing_pct})
print(missing_df[missing_df['Ausentes'] > 0].sort_values('Ausentes', ascending=False))

# =============================================================================
# 3. ESTATÍSTICAS DESCRITIVAS
# =============================================================================
print("\n" + "="*70)
print("📊 ESTATÍSTICAS DESCRITIVAS DOS INDICADORES")
print("="*70)

# Identificar indicadores
indicadores = ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP', 'INDE']
indicadores_disponiveis = [col for col in indicadores if col in df.columns]

print(f"\n📈 Indicadores encontrados: {indicadores_disponiveis}")
print("\n" + df[indicadores_disponiveis].describe().round(2).to_string())

# =============================================================================
# 4. VISUALIZAÇÕES
# =============================================================================
print("\n" + "="*70)
print("📊 GERANDO VISUALIZAÇÕES...")
print("="*70)

# -----------------------------------------------------------------------------
# GRÁFICO 1: Distribuição dos Indicadores
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(2, 4, figsize=(18, 10))
fig.suptitle('📊 Distribuição dos Indicadores PEDE', fontsize=18, fontweight='bold', color=CORES['azul_escuro'])

for i, col in enumerate(indicadores_disponiveis):
    row = i // 4
    col_idx = i % 4
    ax = axes[row, col_idx]
    
    # Histograma com KDE
    ax.hist(df[col].dropna(), bins=25, color=CORES['azul_medio'], alpha=0.7, edgecolor='white')
    ax.axvline(df[col].mean(), color=CORES['laranja'], linestyle='--', linewidth=2, label=f'Média: {df[col].mean():.2f}')
    ax.axvline(df[col].median(), color=CORES['verde'], linestyle=':', linewidth=2, label=f'Mediana: {df[col].median():.2f}')
    ax.set_title(f'{col}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Frequência')
    ax.legend(fontsize=9)

# Esconder eixos vazios se houver
for j in range(len(indicadores_disponiveis), 8):
    row = j // 4
    col_idx = j % 4
    axes[row, col_idx].set_visible(False)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/01_distribuicao_indicadores.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Gráfico 1 salvo: 01_distribuicao_indicadores.png")

# -----------------------------------------------------------------------------
# GRÁFICO 2: Boxplot dos Indicadores
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6))
fig.suptitle('📦 Boxplot dos Indicadores PEDE', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])

df_melted = df[indicadores_disponiveis].melt(var_name='Indicador', value_name='Valor')
sns.boxplot(data=df_melted, x='Indicador', y='Valor', palette='Set2', ax=ax)
ax.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='Limiar crítico (5.0)')
ax.set_ylabel('Valor')
ax.legend()

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/02_boxplot_indicadores.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Gráfico 2 salvo: 02_boxplot_indicadores.png")

# -----------------------------------------------------------------------------
# GRÁFICO 3: Matriz de Correlação
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 10))
fig.suptitle('🔗 Matriz de Correlação dos Indicadores', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])

corr_matrix = df[indicadores_disponiveis].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', 
            center=0, square=True, linewidths=1, ax=ax,
            cbar_kws={'label': 'Correlação'},
            annot_kws={'size': 11})
ax.set_title('')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/03_matriz_correlacao.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Gráfico 3 salvo: 03_matriz_correlacao.png")

# -----------------------------------------------------------------------------
# GRÁFICO 4: Distribuição por Fase
# -----------------------------------------------------------------------------
if 'Fase' in df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('📈 Análise por Fase', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])
    
    # Contagem por fase
    fase_counts = df['Fase'].value_counts().sort_index()
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(fase_counts)))
    
    axes[0].bar(fase_counts.index.astype(str), fase_counts.values, color=colors, edgecolor='white')
    axes[0].set_xlabel('Fase')
    axes[0].set_ylabel('Número de Alunos')
    axes[0].set_title('Distribuição de Alunos por Fase', fontweight='bold')
    
    for i, (idx, v) in enumerate(zip(fase_counts.index, fase_counts.values)):
        axes[0].text(i, v + 3, str(v), ha='center', fontsize=11, fontweight='bold')
    
    # INDE médio por fase
    if 'INDE' in df.columns:
        inde_por_fase = df.groupby('Fase')['INDE'].mean().sort_index()
        cores_inde = [CORES['verde'] if x >= 7 else CORES['amarelo'] if x >= 6 else CORES['vermelho'] for x in inde_por_fase.values]
        
        axes[1].bar(inde_por_fase.index.astype(str), inde_por_fase.values, color=cores_inde, edgecolor='white')
        axes[1].axhline(y=inde_por_fase.mean(), color=CORES['laranja'], linestyle='--', linewidth=2, label=f'Média Geral: {inde_por_fase.mean():.2f}')
        axes[1].set_xlabel('Fase')
        axes[1].set_ylabel('INDE Médio')
        axes[1].set_title('INDE Médio por Fase', fontweight='bold')
        axes[1].legend()
        axes[1].set_ylim(6, 8)
        
        for i, (idx, v) in enumerate(zip(inde_por_fase.index, inde_por_fase.values)):
            axes[1].text(i, v + 0.05, f'{v:.2f}', ha='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/04_analise_por_fase.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Gráfico 4 salvo: 04_analise_por_fase.png")

# -----------------------------------------------------------------------------
# GRÁFICO 5: Distribuição por Pedra (Classificação)
# -----------------------------------------------------------------------------
if 'INDE' in df.columns:
    # Criar classificação por pedra
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
    
    df['Pedra'] = df['INDE'].apply(classificar_pedra)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('💎 Análise por Classificação (Pedra)', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])
    
    # Contagem por pedra
    pedra_order = ['Quartzo', 'Ágata', 'Ametista', 'Topázio']
    pedra_counts = df['Pedra'].value_counts().reindex(pedra_order).dropna()
    cores_pedra = [CORES_PEDRAS.get(p, 'gray') for p in pedra_counts.index]
    
    # Pizza
    axes[0].pie(pedra_counts.values, labels=pedra_counts.index, colors=cores_pedra,
                autopct='%1.1f%%', startangle=90, explode=[0.02]*len(pedra_counts),
                textprops={'fontsize': 12})
    axes[0].set_title('Distribuição por Pedra', fontweight='bold')
    
    # Barras com indicadores médios
    indicadores_media = df.groupby('Pedra')[['IEG', 'IDA', 'IPV', 'IAA']].mean().reindex(pedra_order)
    
    x = np.arange(len(pedra_order))
    width = 0.2
    
    for i, col in enumerate(['IEG', 'IDA', 'IPV', 'IAA']):
        if col in indicadores_media.columns:
            axes[1].bar(x + i*width, indicadores_media[col], width, label=col, alpha=0.8)
    
    axes[1].set_xlabel('Pedra')
    axes[1].set_ylabel('Média do Indicador')
    axes[1].set_title('Indicadores Médios por Pedra', fontweight='bold')
    axes[1].set_xticks(x + width * 1.5)
    axes[1].set_xticklabels(pedra_order)
    axes[1].legend()
    axes[1].set_ylim(0, 10)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/05_analise_por_pedra.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Gráfico 5 salvo: 05_analise_por_pedra.png")

# -----------------------------------------------------------------------------
# GRÁFICO 6: Análise de Defasagem (IAN)
# -----------------------------------------------------------------------------
if 'Defas' in df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('📊 Análise de Defasagem (IAN)', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])
    
    # Distribuição da defasagem
    defas_counts = df['Defas'].value_counts().sort_index()
    colors = [CORES['verde'] if x < 0 else CORES['amarelo'] if x == 0 else CORES['vermelho'] for x in defas_counts.index]
    
    axes[0].bar(defas_counts.index.astype(str), defas_counts.values, color=colors, edgecolor='white')
    axes[0].set_xlabel('Nível de Defasagem')
    axes[0].set_ylabel('Número de Alunos')
    axes[0].set_title('Distribuição da Defasagem', fontweight='bold')
    
    for i, (idx, v) in enumerate(zip(defas_counts.index, defas_counts.values)):
        axes[0].text(i, v + 3, str(v), ha='center', fontsize=10)
    
    # Resumo
    total = len(df)
    acima = (df['Defas'] < 0).sum()
    adequado = (df['Defas'] == 0).sum()
    abaixo = (df['Defas'] > 0).sum()
    
    labels = [f'Acima do Nível\n({100*acima/total:.1f}%)', 
              f'Adequado\n({100*adequado/total:.1f}%)', 
              f'Defasado\n({100*abaixo/total:.1f}%)']
    sizes = [acima, adequado, abaixo]
    colors_pie = [CORES['verde'], CORES['amarelo'], CORES['vermelho']]
    
    axes[1].pie(sizes, labels=labels, colors=colors_pie, autopct='', startangle=90,
                explode=[0.02, 0.02, 0.1], textprops={'fontsize': 11})
    axes[1].set_title('Resumo da Adequação ao Nível', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/06_analise_defasagem.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Gráfico 6 salvo: 06_analise_defasagem.png")

# -----------------------------------------------------------------------------
# GRÁFICO 7: Scatter Plots - Relações entre Indicadores
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('🔗 Relações entre Indicadores', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])

relacoes = [
    ('IEG', 'IDA', 'Engajamento vs Aprendizagem'),
    ('IEG', 'INDE', 'Engajamento vs INDE'),
    ('IAA', 'IDA', 'Autoavaliação vs Aprendizagem'),
    ('IPV', 'IDA', 'Ponto de Virada vs Aprendizagem'),
    ('IPS', 'IDA', 'Psicossocial vs Aprendizagem'),
    ('IEG', 'IPV', 'Engajamento vs Ponto de Virada')
]

for i, (x_col, y_col, titulo) in enumerate(relacoes):
    row = i // 3
    col = i % 3
    ax = axes[row, col]
    
    if x_col in df.columns and y_col in df.columns:
        # Scatter
        ax.scatter(df[x_col], df[y_col], alpha=0.4, c=CORES['azul_medio'], s=30)
        
        # Linha de tendência
        mask = df[[x_col, y_col]].notna().all(axis=1)
        if mask.sum() > 10:
            z = np.polyfit(df.loc[mask, x_col], df.loc[mask, y_col], 1)
            p = np.poly1d(z)
            x_line = np.linspace(df[x_col].min(), df[x_col].max(), 100)
            ax.plot(x_line, p(x_line), color=CORES['laranja'], linewidth=2, label='Tendência')
        
        # Correlação
        corr = df[x_col].corr(df[y_col])
        ax.set_title(f'{titulo}\nr = {corr:.3f}', fontweight='bold')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/07_scatter_relacoes.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Gráfico 7 salvo: 07_scatter_relacoes.png")

# -----------------------------------------------------------------------------
# GRÁFICO 8: IAA vs IDA (Autoavaliação vs Realidade)
# -----------------------------------------------------------------------------
if 'IAA' in df.columns and 'IDA' in df.columns:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('📝 Autoavaliação (IAA) vs Desempenho Real (IDA)', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])
    
    # Comparação de médias
    medias = [df['IAA'].mean(), df['IDA'].mean()]
    labels = ['IAA\n(Autoavaliação)', 'IDA\n(Desempenho Real)']
    colors = [CORES['azul_medio'], CORES['laranja']]
    
    bars = axes[0].bar(labels, medias, color=colors, edgecolor='white', width=0.5)
    axes[0].set_ylabel('Média')
    axes[0].set_title('Comparação de Médias', fontweight='bold')
    axes[0].set_ylim(0, 10)
    
    for bar, m in zip(bars, medias):
        axes[0].text(bar.get_x() + bar.get_width()/2, m + 0.2, f'{m:.2f}', ha='center', fontsize=14, fontweight='bold')
    
    # Gap
    gap = df['IAA'].mean() - df['IDA'].mean()
    axes[0].annotate(f'Gap: {gap:+.2f}', xy=(0.5, 7.5), fontsize=14, fontweight='bold', 
                     color=CORES['vermelho'], ha='center')
    
    # Scatter com linha de igualdade
    axes[1].scatter(df['IAA'], df['IDA'], alpha=0.4, c=CORES['azul_medio'], s=30)
    axes[1].plot([0, 10], [0, 10], 'r--', linewidth=2, label='Linha de Igualdade')
    axes[1].set_xlabel('IAA (Autoavaliação)')
    axes[1].set_ylabel('IDA (Desempenho Real)')
    axes[1].set_title(f'IAA vs IDA (r = {df["IAA"].corr(df["IDA"]):.3f})', fontweight='bold')
    axes[1].legend()
    axes[1].set_xlim(0, 10)
    axes[1].set_ylim(0, 10)
    
    # Distribuição do Gap
    df['Gap_IAA_IDA'] = df['IAA'] - df['IDA']
    axes[2].hist(df['Gap_IAA_IDA'].dropna(), bins=30, color=CORES['azul_medio'], edgecolor='white', alpha=0.7)
    axes[2].axvline(x=0, color=CORES['verde'], linestyle='-', linewidth=2, label='Gap = 0 (ideal)')
    axes[2].axvline(x=df['Gap_IAA_IDA'].mean(), color=CORES['vermelho'], linestyle='--', linewidth=2, 
                    label=f'Média = {df["Gap_IAA_IDA"].mean():.2f}')
    axes[2].set_xlabel('Gap (IAA - IDA)')
    axes[2].set_ylabel('Frequência')
    axes[2].set_title('Distribuição do Gap', fontweight='bold')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/08_iaa_vs_ida.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Gráfico 8 salvo: 08_iaa_vs_ida.png")

# -----------------------------------------------------------------------------
# GRÁFICO 9: Ponto de Virada
# -----------------------------------------------------------------------------
if 'Ponto_de_Virada' in df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('🎯 Análise do Ponto de Virada', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])
    
    # Contagem
    pv_counts = df['Ponto_de_Virada'].value_counts()
    colors = [CORES['vermelho'], CORES['verde']]
    
    axes[0].pie(pv_counts.values, labels=['Não atingiu', 'Atingiu'], colors=colors,
                autopct='%1.1f%%', startangle=90, explode=[0, 0.05], textprops={'fontsize': 12})
    axes[0].set_title('Distribuição do Ponto de Virada', fontweight='bold')
    
    # Indicadores por PV
    indicadores_pv = ['IEG', 'IDA', 'IAA', 'IPS']
    indicadores_pv_disp = [i for i in indicadores_pv if i in df.columns]
    
    if len(indicadores_pv_disp) > 0:
        pv_group = df.groupby('Ponto_de_Virada')[indicadores_pv_disp].mean()
        
        x = np.arange(len(indicadores_pv_disp))
        width = 0.35
        
        bars1 = axes[1].bar(x - width/2, pv_group.loc[0] if 0 in pv_group.index else [0]*len(indicadores_pv_disp), 
                            width, label='Sem PV', color=CORES['vermelho'], alpha=0.8)
        bars2 = axes[1].bar(x + width/2, pv_group.loc[1] if 1 in pv_group.index else [0]*len(indicadores_pv_disp), 
                            width, label='Com PV', color=CORES['verde'], alpha=0.8)
        
        axes[1].set_ylabel('Média')
        axes[1].set_title('Indicadores por Status de Ponto de Virada', fontweight='bold')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(indicadores_pv_disp)
        axes[1].legend()
        axes[1].set_ylim(0, 10)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/09_ponto_de_virada.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Gráfico 9 salvo: 09_ponto_de_virada.png")

# -----------------------------------------------------------------------------
# GRÁFICO 10: Heatmap de Indicadores por Fase e Pedra
# -----------------------------------------------------------------------------
if 'Fase' in df.columns and 'Pedra' in df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('🗺️ Mapas de Calor dos Indicadores', fontsize=16, fontweight='bold', color=CORES['azul_escuro'])
    
    # Por Fase
    heatmap_fase = df.groupby('Fase')[indicadores_disponiveis].mean()
    sns.heatmap(heatmap_fase, annot=True, fmt='.2f', cmap='RdYlGn', ax=axes[0],
                cbar_kws={'label': 'Média'}, linewidths=0.5)
    axes[0].set_title('Indicadores por Fase', fontweight='bold')
    axes[0].set_ylabel('Fase')
    
    # Por Pedra
    pedra_order = ['Quartzo', 'Ágata', 'Ametista', 'Topázio']
    heatmap_pedra = df.groupby('Pedra')[indicadores_disponiveis].mean().reindex(pedra_order)
    sns.heatmap(heatmap_pedra, annot=True, fmt='.2f', cmap='RdYlGn', ax=axes[1],
                cbar_kws={'label': 'Média'}, linewidths=0.5)
    axes[1].set_title('Indicadores por Pedra', fontweight='bold')
    axes[1].set_ylabel('Pedra')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/10_heatmaps.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Gráfico 10 salvo: 10_heatmaps.png")

# =============================================================================
# 5. RESUMO ESTATÍSTICO
# =============================================================================
print("\n" + "="*70)
print("📊 RESUMO DOS PRINCIPAIS INSIGHTS")
print("="*70)

print("\n🎯 INDICADORES:")
for col in indicadores_disponiveis:
    print(f"   {col}: Média = {df[col].mean():.2f}, Mediana = {df[col].median():.2f}, Std = {df[col].std():.2f}")

print("\n🔗 CORRELAÇÕES COM INDE:")
if 'INDE' in df.columns:
    for col in indicadores_disponiveis:
        if col != 'INDE':
            corr = df['INDE'].corr(df[col])
            forca = "FORTE" if abs(corr) > 0.5 else "MODERADA" if abs(corr) > 0.3 else "FRACA"
            print(f"   INDE x {col}: r = {corr:.3f} ({forca})")

print("\n📈 DEFASAGEM:")
if 'Defas' in df.columns:
    total = len(df)
    acima = (df['Defas'] < 0).sum()
    adequado = (df['Defas'] == 0).sum()
    abaixo = (df['Defas'] > 0).sum()
    print(f"   Acima do nível: {acima} ({100*acima/total:.1f}%)")
    print(f"   No nível adequado: {adequado} ({100*adequado/total:.1f}%)")
    print(f"   Defasados: {abaixo} ({100*abaixo/total:.1f}%)")

print("\n💎 DISTRIBUIÇÃO POR PEDRA:")
if 'Pedra' in df.columns:
    for pedra in ['Quartzo', 'Ágata', 'Ametista', 'Topázio']:
        count = (df['Pedra'] == pedra).sum()
        pct = 100 * count / len(df)
        print(f"   {pedra}: {count} ({pct:.1f}%)")

print("\n" + "="*70)
print("✅ ANÁLISE EXPLORATÓRIA CONCLUÍDA!")
print("="*70)
print("\n📁 Gráficos salvos em /mnt/user-data/outputs/:")
print("   01_distribuicao_indicadores.png")
print("   02_boxplot_indicadores.png")
print("   03_matriz_correlacao.png")
print("   04_analise_por_fase.png")
print("   05_analise_por_pedra.png")
print("   06_analise_defasagem.png")
print("   07_scatter_relacoes.png")
print("   08_iaa_vs_ida.png")
print("   09_ponto_de_virada.png")
print("   10_heatmaps.png")
