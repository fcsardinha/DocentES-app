import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="DocentES | Censo Escolar",
    page_icon="👩🏻‍🏫",
    layout="wide"
)

# --- FUNÇÃO PARA CARREGAR TODOS OS DADOS ---
@st.cache_data
def carregar_todos_os_dados():
    """
    Esta função carrega todos os 5 arquivos CSV em DataFrames separados
    e os retorna em um dicionário para fácil acesso.
    """
    # Nomes dos arquivos
    nomes_arquivos = {
        "dependencia": "docentes_dependencia.csv",
        "etapas": "docentes_etapas.csv",
        "formacao": "docentes_formacao.csv",
        "idade": "docentes_idade.csv",
        "vinculo": "docentes_vinculo.csv"
    }
    
    dataframes = {}
    for nome, caminho in nomes_arquivos.items():
        # Carrega cada dataframe usando ';' como separador
        df = pd.read_csv(caminho, delimiter=';')
        dataframes[nome] = df
        
    # Limpeza específica: remove a coluna vazia do arquivo de vínculo
    #if 'Unnamed: 7' in dataframes['vinculo'].columns:
    #    dataframes['vinculo'] = dataframes['vinculo'].drop(columns=['Unnamed: 7'])
        
    return dataframes

# Carrega todos os dataframes
try:
    dfs = carregar_todos_os_dados()
except FileNotFoundError as e:
    st.error(f"Erro ao carregar os dados: O arquivo {e.filename} não foi encontrado.")
    st.info("Por favor, certifique-se de que todos os 5 arquivos CSV estão na mesma pasta que o app.py.")
    st.stop()


# --- TÍTULO E INTRODUÇÃO ---
st.title("👩🏽‍🏫 DocentES 👨🏻‍🏫")
st.markdown(
    "Bem-vindo à DocentES, a plataforma sobre os Docentes do Espírito Santo!"
)
st.markdown("Análise interativa dos dados de docentes do Espírito Santo, com base nas Sinopses Estatísticas do Censo Escolar da Educação Básica.")
st.markdown("---")

# --- BARRA LATERAL COM FILTROS (SIDEBAR) ---
# Foi usado o dataframe de 'etapas' como base para criar os filtros.
st.sidebar.header("⚙️ Filtros")
st.sidebar.markdown("Use os filtros abaixo para selecionar o ano e o município desejados.")

# Filtro de Ano
ano_selecionado = st.sidebar.selectbox(
    "Selecione o Ano",
    options=sorted(dfs['etapas']['Ano'].unique(), reverse=True)
)

# Filtro de Município
lista_municipios = sorted(dfs['etapas']['Município'].unique())
municipio_selecionado = st.sidebar.selectbox(
    "Selecione o Município",
    options=lista_municipios
)

# --- CRIAÇÃO DAS ABAS (TABS) ---
st.header(f"Exibindo dados para: {municipio_selecionado} ({ano_selecionado})")

# Nomeando as abas temáticas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Etapas de Ensino",
    "📊 Faixa Etária e Sexo",
    "📊 Nível de Formação",
    "📊 Vínculo Funcional",
    "📊 Dependência e Localização"
])


# --- ABA 1: ETAPAS DE ENSINO ---
with tab1:
    st.subheader("Docentes por Etapa de Ensino")
    
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['etapas'][
        (dfs['etapas']['Ano'] == ano_selecionado) &
        (dfs['etapas']['Município'] == municipio_selecionado)
    ]
    
    # Prepara os dados para o gráfico (transforma colunas em linhas)
    colunas_etapas = ['Creche', 'Pré-Escola', 'EF - Anos Iniciais', 'EF - Anos Finais', 'EM Propedêutico', 'EM Integrado']
    dados_grafico = df_filtrado[colunas_etapas].melt(var_name='Etapa', value_name='Nº de Docentes')
    
    # Cria e exibe o gráfico
    fig = px.bar(dados_grafico, x='Etapa', y='Nº de Docentes', text_auto=True, title="Total de Docentes por Etapa")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_filtrado)


# --- ABA 2: FAIXA ETÁRIA E SEXO ---
with tab2:
    st.subheader("Docentes por Faixa Etária e Sexo")
    
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['idade'][
        (dfs['idade']['Ano'] == ano_selecionado) &
        (dfs['idade']['Município'] == municipio_selecionado)
    ]
    
    # Prepara os dados para o gráfico
    colunas_idade = ['Até 24 anos', 'De 25 a 29 anos', 'De 30 a 39 anos', 'De 40 a 49 anos', 'De 50 a 54 anos', 'De 55 a 59 anos', '60 anos ou mais']
    dados_grafico = df_filtrado.melt(id_vars=['Sexo'], value_vars=colunas_idade, var_name='Faixa Etária', value_name='Nº de Docentes')
    
    # Cria o gráfico de barras agrupado por sexo
    fig = px.bar(dados_grafico, x='Faixa Etária', y='Nº de Docentes', color='Sexo', barmode='group', text_auto=True, title="Distribuição de Docentes por Idade e Sexo")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_filtrado)


# --- ABA 3: NÍVEL DE FORMAÇÃO ---
with tab3:
    st.subheader("Docentes por Nível de Formação")
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['formacao'][
        (dfs['formacao']['Ano'] == ano_selecionado) &
        (dfs['formacao']['Município'] == municipio_selecionado)
    ]
    # IMPLEMENTAÇÃO: Crie o gráfico para esta aba, similar ao da Aba 1
    st.info("Gráfico de Formação a ser implementado.")
    st.dataframe(df_filtrado)


# --- ABA 4: VÍNCULO FUNCIONAL ---
with tab4:
    st.subheader("Docentes por Vínculo Funcional")
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['vinculo'][
        (dfs['vinculo']['Ano'] == ano_selecionado) &
        (dfs['vinculo']['Município'] == municipio_selecionado)
    ]
    # IMPLEMENTAÇÃO: Este gráfico pode ser um de pizza (pie chart)
    st.info("Gráfico de Vínculo a ser implementado.")
    st.dataframe(df_filtrado)


# --- ABA 5: DEPENDÊNCIA E LOCALIZAÇÃO ---
with tab5:
    st.subheader("Docentes por Dependência Administrativa e Localização")
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['dependencia'][
        (dfs['dependencia']['Ano'] == ano_selecionado) &
        (dfs['dependencia']['Município'] == municipio_selecionado)
    ]
    # IMPLEMENTAÇÃO: Gráfico de barras agrupado por Localização (Urbana/Rural)
    st.info("Gráfico de Dependência e Localização a ser implementado.")
    st.dataframe(df_filtrado)
