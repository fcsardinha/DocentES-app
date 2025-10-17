# Importando as bibliotecas necessárias
import streamlit as st
import unicodedata
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
def carregar_dados():
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
        df.columns = df.columns.str.strip()
        dataframes[nome] = df
            
    return dataframes

# Carrega todos os dataframes
try:
    dfs = carregar_dados()
except FileNotFoundError as e:
    st.error(f"Erro ao carregar os dados: O arquivo {e.filename} não foi encontrado.")
    st.info("Por favor, certifique-se de que todos os 5 arquivos CSV estão na mesma pasta que o app.py.")
    st.stop()

# --- DEFININDO BARRA LATERAL COM FILTROS (Ano e Município) ---

# Definindo função auxiliar para normalizar texto para ordenação
def normalizar_para_ordenacao(texto):
    """
    Remove acentos de uma string para usá-la como chave de ordenação.
    Ex: 'Águia Branca' -> 'Aguia Branca'
    """
    # Normaliza a string para decompor os caracteres acentuados
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Remove os caracteres de combinação (acentos)
    return "".join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

# Foi usado o dataframe de 'etapas' como base para criar os filtros.
st.sidebar.header("⚙️ Filtros")
st.sidebar.markdown("Use os filtros abaixo para selecionar o ano e o município desejados.")

# --- Filtro de Ano ---
ano_selecionado = st.sidebar.selectbox(
    "Selecione o Ano",
    options=sorted(
                    dfs['etapas']['Ano'].unique(), 
                    reverse=True
                  )
)

# --- Filtro de Município ---
# Criando a opção geral
opcao_geral = ["Todos os Municípios"]
# Criando uma lista ordenada dos municípios
lista_municipios = sorted(
    dfs['etapas']['Município'].unique(),
    key=normalizar_para_ordenacao # Usando a função de normalização
    )
# Juntando as duas listas!
opcoes_municipios = opcao_geral + lista_municipios

# Usamos a nova lista completa como opções do selectbox
municipio_selecionado = st.sidebar.selectbox(
    "Selecione o Município",
    options=opcoes_municipios
)

# --- CORPO PRINCIPAL DO APP ---

# Título da aplicação
st.title("👩🏽‍🏫 DocentES 👨🏻‍🏫")
# Descrição da aplicação
st.markdown(
    "Bem-vindo à DocentES, a plataforma sobre os Docentes do Espírito Santo!"
)

# Exibir uma explicação sobre a aplicação com uma imagem ilustrativa
with st.expander("Sobre o que é esta aplicação?"):
    # Cria as colunas dentro do expander
    col1, col2 = st.columns([1,2])

    # Adiciona conteúdo à primeira coluna
    with col1:
        st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhWSVR_PA-xWPXwdQ5qyRDWAZZdVA1JhdQuaT6yI926pYTAg0boScUh3J-lsiu1i3KDyHJQmN_OgNx6HX4Zun6XDIRfqNXJe8CdyKcnwDymZp8P52JvRrKav0otT263CjHKyS_RitA5VPJFOg6NJ-uqRwuksj2r_J1mna9CnfEVq4psg-QMaH4bq2Uy2w/w485-h335/fc-removebg-preview.png", width=400)

    # Adiciona conteúdo à segunda coluna
    with col2:
        st.header("Coluna 2")
        st.write("Este é o conteúdo da segunda coluna.")

st.markdown("Análise interativa dos dados de docentes do Espírito Santo, com base nas Sinopses Estatísticas do Censo Escolar da Educação Básica.")
st.write("Aqui você pode explorar dados sobre os professores do estado, incluindo informações demográficas, formação acadêmica, e muito mais.")

st.markdown("---")

# --- CRIAÇÃO DAS ABAS (TABS) ---
st.subheader(f"Exibindo dados para: {municipio_selecionado} ({ano_selecionado})")

# Nomeando as abas temáticas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Etapas de Ensino",
    "📊 Faixa Etária e Sexo",
    "📊 Formação Acadêmica",
    "📊 Vínculo Funcional",
    "📊 Dependência e Localização"
])

# --- ABA 1: ETAPAS DE ENSINO ---
with tab1:
    st.markdown("#### Docentes por Etapa de Ensino")
    
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['etapas'][
        (dfs['etapas']['Ano'] == ano_selecionado) &
        (dfs['etapas']['Município'] == municipio_selecionado)
    ]
    
    # Prepara os dados para o gráfico (transforma colunas em linhas)
    colunas_etapas = ['Creche', 'Pré-Escola', 'EF - Anos Iniciais', 'EF - Anos Finais', 'EM Propedêutico', 'EM Integrado']
    dados_grafico = df_filtrado[colunas_etapas].melt(var_name='Etapa de Ensino', value_name='Quant. de Docentes')
    
    # Cria e exibe o gráfico
    fig = px.bar(dados_grafico, x='Etapa de Ensino', y='Quant. de Docentes', text_auto=True, title="Quantidade de docentes por etapa de ensino, segundo o município")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_filtrado)
    
    # Mensagem explicativa sobre os dados
    st.info("O mesmo docente pode ser contabilizado mais de uma vez, por atuar em diferentes etapas de ensino.")

# --- ABA 2: FAIXA ETÁRIA E SEXO ---
with tab2:
    st.markdown("#### Docentes por Faixa Etária e Sexo")
    
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['idade'][
        (dfs['idade']['Ano'] == ano_selecionado) &
        (dfs['idade']['Município'] == municipio_selecionado)
    ]
    
    # Prepara os dados para o gráfico
    colunas_idade = ['Até 24 anos', 'De 25 a 29 anos', 'De 30 a 39 anos', 'De 40 a 49 anos', 'De 50 a 54 anos', 'De 55 a 59 anos', '60 anos ou mais']
    dados_grafico = df_filtrado.melt(id_vars=['Sexo'], value_vars=colunas_idade, var_name='Faixa Etária', value_name='Quant. de Docentes')
    
    # Cria o gráfico de barras agrupado por sexo
    fig = px.bar(dados_grafico, x='Faixa Etária', y='Quant. de Docentes', color='Sexo', barmode='group', text_auto=True, title="Quantidade de docentes por faixa etária e sexo, segundo o município")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_filtrado)

# --- ABA 3: NÍVEL DE FORMAÇÃO ---
with tab3:
    st.markdown("#### Docentes por Escolaridade ou Nível de Formação Acadêmica")
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['formacao'][
        (dfs['formacao']['Ano'] == ano_selecionado) &
        (dfs['formacao']['Município'] == municipio_selecionado)
    ]
    
    # Prepara os dados para o gráfico (transforma colunas em linhas)
    colunas_formacao = ['Ensino Fundamental', 'Ensino Médio', 'Graduação - Licenciatura', 'Graduação - Sem Licenciatura', 'Especialização', 'Mestrado', 'Doutorado']
    dados_grafico = df_filtrado[colunas_formacao].melt(var_name='Escolaridade / Formação Acadêmica', value_name='Quant. de Docentes')
    
    # Cria e exibe o gráfico
    fig = px.bar(dados_grafico, x='Quant. de Docentes', y='Escolaridade / Formação Acadêmica', text_auto=True, title="Quantidade de docentes por escolaridade ou formação acadêmica, segundo o município", orientation='h')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_filtrado)

# --- ABA 4: VÍNCULO FUNCIONAL ---
with tab4:
    st.markdown("#### Docentes por Vínculo Funcional e Dependência Administrativa")
    # Filtra o dataframe específico desta aba
    df_filtrado = dfs['vinculo'][
        (dfs['vinculo']['Ano'] == ano_selecionado) &
        (dfs['vinculo']['Município'] == municipio_selecionado)
    ]
    
    # Preparando os dados para o gráfico (transforma colunas em linhas)
    dados_grafico = df_filtrado.melt(
        id_vars=['Vínculo Funcional'], 
        value_vars=['Federal', 'Estadual', 'Municipal'], 
        var_name='Dependência Administrativa', 
        value_name='Quant. de Docentes'
    )
    
    # Removendo vínculos que não têm docentes para limpar o gráfico
    dados_grafico = dados_grafico[dados_grafico['Quant. de Docentes'] > 0]

    # Criando o gráfico de barras facetado com o argumento 'facet_col'
    fig = px.bar(
        dados_grafico,
        x='Quant. de Docentes',
        y='Vínculo Funcional',
        color='Dependência Administrativa',  # Atribui cores diferentes para cada dependência
        facet_col='Dependência Administrativa', # CRIA OS SUBPLOTS (um para cada dependência)
        labels={'Quant. de Docentes': 'Quant. de Docentes', 'Vínculo Funcional': 'Tipo de Vínculo'},
        title=f"Quantidade de docentes por vínculo funcional para o município de {municipio_selecionado}",
        text_auto=True,
        orientation='h'
    )
    
    # --- Melhora a aparência da aba ---
    # Remove os títulos dos eixos X e Y de cada subplot individualmente
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    
    # Remove os títulos (anotações) de cada subplot (ex: "Dependência Administrativa=Federal")
    fig.for_each_annotation(lambda a: a.update(text=""))
    
    # Adiciona um título centralizado para o eixo X e define o espaçamento
    fig.update_layout(
        xaxis_title="Quantidade de Docentes",  # Título centralizado para o eixo X
        horizontal_spacing=0.05          # Adiciona um espaço de 5% da largura total entre os gráficos
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Exibindo dataframe
    st.dataframe(df_filtrado)

    # Mensagem explicativa sobre os dados
    st.info("O mesmo docente pode ser contabilizado mais de uma vez, por atuar com mais de um vínculo.")

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
    
    # Mensagem explicativa sobre os dados
    st.info("O mesmo docente pode ser contabilizado mais de uma vez, por atuar em mais de uma localização e/ou dependência administrativa.")