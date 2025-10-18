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

# Exibir uma explicação sobre a aplicação com expander e duas colunas
with st.expander("Sobre o que é esta aplicação?"):
    # Cria as colunas dentro do expander
    col1, col2 = st.columns([1,2])

    # Adiciona conteúdo à primeira coluna
    with col1:
        st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhWSVR_PA-xWPXwdQ5qyRDWAZZdVA1JhdQuaT6yI926pYTAg0boScUh3J-lsiu1i3KDyHJQmN_OgNx6HX4Zun6XDIRfqNXJe8CdyKcnwDymZp8P52JvRrKav0otT263CjHKyS_RitA5VPJFOg6NJ-uqRwuksj2r_J1mna9CnfEVq4psg-QMaH4bq2Uy2w/w485-h335/fc-removebg-preview.png", width=400)

    # Adiciona conteúdo à segunda coluna
    with col2:
        st.write("Esta aplicação permite a análise interativa dos dados de docentes do Espírito Santo, com base nas Sinopses Estatísticas do Censo Escolar da Educação Básica.")
        st.write(
                    "Os dados utilizados foram os referentes aos anos de 2022 a 2024, que se encontram disponíveis no site do INEP: " \
                    "(https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-basica)"
                )
        st.write("Aqui você pode explorar dados sobre os professores do estado, incluindo informações demográficas, formação acadêmica, e muito mais.")
 
st.markdown("---")

# --- CRIAÇÃO DAS ABAS TEMÁTICAS (TABS) ---
st.subheader(f"Exibindo dados de quantidade de docentes, segundo o município e o ano selecionados.")

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
    df_etapas = dfs["etapas"]

    # --- Definindo containers dentro da aba ---
    # Container para o gráfico de barras
    c1 = st.container(border=True)

    # Selecionando as colunas para o gráfico
    colunas_etapas = ['Creche', 'Pré-Escola', 'EF - Anos Iniciais', 'EF - Anos Finais', 'EM Propedêutico', 'EM Integrado']
    
    # Estabelecendo a lógica para o gráfico, conforme o filtro de município
    if municipio_selecionado == "Todos os Municípios":
        # SE o usuário escolher ver o estado todo:
        # 1. Filtrar o DataFrame apenas pelo ano
        df_filtrado_ano = df_etapas[df_etapas['Ano'] == ano_selecionado]
        # 2. Somar os valores de todos os municípios, resultando em uma série
        dados_base = df_filtrado_ano[colunas_etapas].sum()
        # 3. Transformar a série em um DataFrame longo
        dados_grafico = dados_base.reset_index()
        dados_grafico.columns = ['Etapa de Ensino', 'Quant. de Docentes']

    else:
        # SENÃO (o usuário escolheu um município específico)...
        # 1. Filtrar o DataFrame pelo ano E pelo município
        df_filtrado = df_etapas[
            (df_etapas['Ano'] == ano_selecionado) &
            (df_etapas['Município'] == municipio_selecionado)
        ]
        # 2. TRANSFORMA a tabela larga em longa usando .melt()
        dados_grafico = df_filtrado[colunas_etapas].melt(var_name='Etapa de Ensino', value_name='Quant. de Docentes')

    # Gerando o gráfico    
    if not dados_grafico.empty:
            # Parametrizando o px.bar
            fig = px.bar(
                            dados_grafico, 
                            x='Etapa de Ensino', 
                            y='Quant. de Docentes', 
                            color='Etapa de Ensino',
                            text_auto=True, 
                            title=f"Docentes por Etapa de Ensino em {municipio_selecionado} ({ano_selecionado})"
                        )
            # Adicionando a formatação de números brasileiros
            fig.update_layout(
                                separators=',.',
                                showlegend=False
                            )
            fig.update_yaxes(tickformat=",.0f")
            
            c1.plotly_chart(fig, use_container_width=True)    
    else:
            c1.warning("Nenhum dado encontrado para a seleção atual.")
        
    # Exibindo o dataframe filtrado correspondente
    with c1.expander("Ver tabela de dados"):
        st.dataframe(df_filtrado_ano)    

    # --- Container 2: Gráfico de Linhas (a evolução temporal) ---
    st.markdown("---") # Linha divisória
    c1t = st.container(border=True)
    c1t.markdown("##### Análise da Evolução Temporal (2022-2024)")

    # 1. Preparando os dados para a análise temporal
    if municipio_selecionado == "Todos os Municípios":
        # Se for o estado todo, agrupamos por ano e somamos
        dados_temporais = df_etapas.groupby('Ano')[colunas_etapas].sum()
    else:
        # Se for um município, filtramos e definimos o ano como índice
        dados_temporais = df_etapas[df_etapas['Município'] == municipio_selecionado].set_index('Ano')[colunas_etapas]
    
    # 2. Criamos o FILTRO para a etapa de ensino que você sugeriu
    col_filtro, col_vazia = c1t.columns([2, 3])
    with col_filtro:
        etapa_selecionada = st.selectbox(
            "Selecione a Etapa para ver a tendência:",
            options=colunas_etapas
        )
    
    # 3. Selecionamos apenas a coluna (etapa) que o usuário escolheu
    dados_linha = dados_temporais[[etapa_selecionada]] # Usar colchetes duplos mantém como DataFrame

    # 4. Usamos px.line com formatação ---
if not dados_linha.empty:
    # Criando a figura base com Plotly Express
    fig_linha = px.line(
                        dados_linha,
                        markers=True, # Adiciona pontos sobre a linha para destacar os anos
                        labels={'value': 'Quant. de Docentes', 'Ano': 'Ano'}
                    )

    # Formata os separadores para o padrão brasileiro
    fig_linha.update_layout(separators=',.',showlegend=False)
    
    # Formata o eixo Y (quantidade) para ter separador de milhar e sem decimais
    fig_linha.update_yaxes(tickformat=",.0f")
    
    # Formata o eixo X (ano) para mostrar apenas os números inteiros
    # O 'd' em tickformat significa 'decimal integer'
    fig_linha.update_xaxes(tickformat='d', tickvals=dados_temporais.index)

    # Exibindo a figura do Plotly
    c1t.plotly_chart(fig_linha, use_container_width=True)
else:
    c1t.warning("Nenhum dado encontrado para a seleção.")

    # Mensagem explicativa sobre os dados
    st.info("O mesmo docente pode ser contabilizado mais de uma vez, por atuar em diferentes etapas de ensino.")

# --- ABA 2: FAIXA ETÁRIA E SEXO ---
with tab2:
    st.markdown("#### Docentes por Faixa Etária e Sexo")
    df_idade = dfs["idade"]

    c2 = st.container(border=True)

    colunas_idade = ['Até 24 anos', 'De 25 a 29 anos', 'De 30 a 39 anos', 'De 40 a 49 anos', 'De 50 a 54 anos', 'De 55 a 59 anos', '60 anos ou mais']

    # Lógica de preparação de dados
    if municipio_selecionado == "Todos os Municípios":
        df_filtrado = df_idade[df_idade['Ano'] == ano_selecionado]
        dados_base = df_filtrado.groupby('Sexo')[colunas_idade].sum().reset_index()
    else:
        dados_base = df_idade[
            (df_idade['Ano'] == ano_selecionado) &
            (df_idade['Município'] == municipio_selecionado)
        ]

    # Transformação com .melt()
    dados_para_plotar = dados_base.melt(
        id_vars=['Sexo'], 
        value_vars=colunas_idade, 
        var_name='Faixa Etária', 
        value_name='Quant. de Docentes'
    )

    # Ordenação correta das categorias
    ordem_faixa_etaria = ['Até 24 anos', 'De 25 a 29 anos', 'De 30 a 39 anos', 'De 40 a 49 anos', 'De 50 a 54 anos', 'De 55 a 59 anos', '60 anos ou mais']
    dados_para_plotar['Faixa Etária'] = pd.Categorical(dados_para_plotar['Faixa Etária'], categories=ordem_faixa_etaria, ordered=True)

    # Gerando o gráfico
    if not dados_para_plotar.empty:
        fig = px.bar(
            dados_para_plotar,
            x='Faixa Etária',
            y='Quant. de Docentes',
            color='Sexo',
            barmode='group',
            text_auto=True,
            title=f"Docentes por Faixa Etária e Sexo em {municipio_selecionado} ({ano_selecionado})"
        )
        fig.update_layout(separators=',.')
        fig.update_yaxes(tickformat=",.0f")
        c2.plotly_chart(fig, use_container_width=True)
    else:
        c2.warning("Nenhum dado encontrado para a seleção atual.")

    with c2.expander("Ver tabela de dados"):
        st.dataframe(dados_base)

# --- ABA 3: NÍVEL DE FORMAÇÃO ---
with tab3:
    st.markdown("#### Docentes por Escolaridade ou Nível de Formação Acadêmica")
    df_formacao = dfs["formacao"]

    c3 = st.container(border=True)

    colunas_formacao = ['Ensino Fundamental', 'Ensino Médio', 'Graduação - Licenciatura', 'Graduação - Sem Licenciatura', 'Especialização', 'Mestrado', 'Doutorado']

    if municipio_selecionado == "Todos os Municípios":
        df_filtrado = df_formacao[df_formacao['Ano'] == ano_selecionado]
        dados_base = df_filtrado[colunas_formacao].sum()
        dados_para_plotar = dados_base.reset_index()
        dados_para_plotar.columns = ['Formação Acadêmica', 'Quant. de Docentes']
    else:
        df_filtrado = df_formacao[
            (df_formacao['Ano'] == ano_selecionado) &
            (df_formacao['Município'] == municipio_selecionado)
        ]
        dados_para_plotar = df_filtrado[colunas_formacao].melt(var_name='Formação Acadêmica', value_name='Quant. de Docentes')

    # Ordenação correta das categorias
    ordem_formacao = ['Ensino Fundamental', 'Ensino Médio', 'Graduação - Licenciatura', 'Graduação - Sem Licenciatura', 'Especialização', 'Mestrado', 'Doutorado']
    dados_para_plotar['Formação Acadêmica'] = pd.Categorical(dados_para_plotar['Formação Acadêmica'], categories=ordem_formacao, ordered=True)
    dados_para_plotar = dados_para_plotar.sort_values('Formação Acadêmica')

    if not dados_para_plotar.empty:
        fig = px.bar(
            dados_para_plotar,
            x='Quant. de Docentes',
            y='Formação Acadêmica',
            color='Formação Acadêmica',
            orientation='h',
            text_auto=True,
            title=f"Docentes por Escolaridade ou Formação Acadêmica em {municipio_selecionado} ({ano_selecionado})"
        )
        fig.update_layout(separators=',.', showlegend=False)
        fig.update_xaxes(tickformat=",.0f")
        c3.plotly_chart(fig, use_container_width=True)
    else:
        c3.warning("Nenhum dado encontrado para a seleção atual.")
    
    with c3.expander("Ver tabela de dados"):
        st.dataframe(df_filtrado)

# --- ABA 4: VÍNCULO FUNCIONAL ---
with tab4:
    st.markdown("#### Docentes por Vínculo Funcional e Dependência Administrativa")
    df_vinculo = dfs["vinculo"]

    c4 = st.container(border=True)
    colunas_vinculo = ['Federal', 'Estadual', 'Municipal']

    if municipio_selecionado == "Todos os Municípios":
        df_filtrado = df_vinculo[df_vinculo['Ano'] == ano_selecionado]
        dados_base = df_filtrado.groupby('Vínculo Funcional')[colunas_vinculo].sum().reset_index()
    else:
        dados_base = df_vinculo[
            (df_vinculo['Ano'] == ano_selecionado) &
            (df_vinculo['Município'] == municipio_selecionado)
        ]

    dados_para_plotar = dados_base.melt(
        id_vars=['Vínculo Funcional'], 
        value_vars=colunas_vinculo, 
        var_name='Dependência Administrativa', 
        value_name='Quant. de Docentes'
    )
    dados_para_plotar = dados_para_plotar[dados_para_plotar['Quant. de Docentes'] > 0]

    if not dados_para_plotar.empty:
        fig = px.bar(
            dados_para_plotar,
            x='Quant. de Docentes',
            y='Vínculo Funcional',
            color='Dependência Administrativa',
            facet_col='Dependência Administrativa',
            facet_col_spacing=0.05, # Usando o parâmetro correto de espaçamento
            orientation='h',
            text_auto=True,
            title=f"Docentes por Vínculo em {municipio_selecionado} ({ano_selecionado})"
        )
        fig.for_each_annotation(lambda a: a.update(text="")) # Remove títulos dos subplots
        fig.update_layout(separators=',.')
        fig.update_xaxes(tickformat=",.0f", title_text="Quantidade de Docentes")
        c4.plotly_chart(fig, use_container_width=True)
    else:
        c4.warning("Nenhum dado encontrado para a seleção atual.")
    
    with c4.expander("Ver tabela de dados"):
        st.dataframe(dados_base)

    # Mensagem explicativa sobre os dados
    st.info("O mesmo docente pode ser contabilizado mais de uma vez, por atuar com mais de um vínculo.")

# --- ABA 5: DEPENDÊNCIA E LOCALIZAÇÃO ---
with tab5:
    st.markdown("#### Docentes por Dependência Administrativa e Localização")
    df_dependencia = dfs["dependencia"]

    c5 = st.container(border=True)
    colunas_dependencia = ['Federal', 'Estadual', 'Municipal', 'Privada']

    if municipio_selecionado == "Todos os Municípios":
        df_filtrado = df_dependencia[df_dependencia['Ano'] == ano_selecionado]
        dados_base = df_filtrado.groupby('Localização')[colunas_dependencia].sum().reset_index()
    else:
        dados_base = df_dependencia[
            (df_dependencia['Ano'] == ano_selecionado) &
            (df_dependencia['Município'] == municipio_selecionado)
        ]

    dados_para_plotar = dados_base.melt(
        id_vars=['Localização'], 
        value_vars=colunas_dependencia, 
        var_name='Dependência', 
        value_name='Quant. de Docentes'
    )

    if not dados_para_plotar.empty:
        fig = px.bar(
            dados_para_plotar,
            x='Localização',
            y='Quant. de Docentes',
            color='Dependência',
            barmode='group',
            text_auto=True,
            title=f"Docentes por Localização e Dependência em {municipio_selecionado} ({ano_selecionado})"
        )
        fig.update_layout(separators=',.')
        fig.update_yaxes(tickformat=",.0f")
        c5.plotly_chart(fig, use_container_width=True)
    else:
        c5.warning("Nenhum dado encontrado para a seleção atual.")

    with c5.expander("Ver tabela de dados"):
        st.dataframe(dados_base)
    
    # Mensagem explicativa sobre os dados
    st.info("O mesmo docente pode ser contabilizado mais de uma vez, por atuar em mais de uma localização e/ou dependência administrativa.")

# --- RODAPÉ DA APLICAÇÃO ---
st.markdown("---")
st.markdown("© 2025 DocentES. Desenvolvido por Farley C. Sardinha. Todos os direitos reservados.")