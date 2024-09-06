import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests

# Função para exibir o formulário de perfil do investidor
def perfil_investidor():
    st.title("Análise de Perfil do Investidor")

    # Coletando dados do usuário
    idade = st.slider("Idade", 18, 100)
    risco = st.selectbox("Nível de risco", ["Conservador", "Moderado", "Agressivo"])
    objetivo = st.text_input("Objetivo financeiro")
    prazo = st.selectbox("Prazo do investimento", ["Curto prazo", "Médio prazo", "Longo prazo"])

    if st.button("Analisar perfil"):
        st.write(f"Perfil analisado: Idade {idade}, Risco {risco}, Objetivo: {objetivo}, Prazo: {prazo}")
        # Aqui você pode adicionar a lógica para categorizar o investidor

# Função para recomendar investimentos
def recomendacoes_investimentos():
    st.title("Recomendações de Investimentos")

    # Exibir recomendações baseadas no perfil de risco
    perfil = st.radio("Selecione o perfil de risco", ["Conservador", "Moderado", "Agressivo"])
    if perfil == "Conservador":
        st.write("Recomendamos: Tesouro Direto, CDB, Fundos de Renda Fixa")
    elif perfil == "Moderado":
        st.write("Recomendamos: Fundos Multimercados, Debêntures")
    elif perfil == "Agressivo":
        st.write("Recomendamos: Ações, ETFs, Criptomoedas")

# Função para análise de mercado
def analise_mercado():
    st.title("Análise do Mercado Financeiro")

    # Use a API do Yahoo Finance (via yfinance)
    mercado = st.selectbox("Selecione o índice do mercado", ["^GSPC", "^DJI", "^IXIC"])
    dados_mercado = yf.download(mercado, period="1mo", interval="1d")

    st.write(f"Exibindo dados do índice: {mercado}")

    # Plotar gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_mercado.index, y=dados_mercado['Close'], mode='lines', name='Fechamento'))
    st.plotly_chart(fig)

# Função para análise de ativo específico
def analise_ativo():
    st.title("Análise de Ativo Específico")

    ativo = st.text_input("Digite o código do ativo (ex: AAPL, TSLA)", "AAPL")
    dados_ativo = yf.Ticker(ativo)
    historico = dados_ativo.history(period="1mo")

    # Exibir informações
    st.write(f"Análise de {ativo}")
    st.write(f"Preço atual: {historico['Close'][-1]}")

    # Plotar gráfico do ativo
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historico.index, y=historico['Close'], mode='lines', name='Fechamento'))
    st.plotly_chart(fig)

# Função para o chat educacional
def chat_educacional():
    st.title("Chat de Educação Financeira")

    # Simulação de um chatbot simples
    pergunta = st.text_input("Pergunte sobre educação financeira", "O que é um ETF?")
    if st.button("Perguntar"):
        st.write(f"Pergunta: {pergunta}")
        # Aqui você pode usar um modelo de IA para responder a pergunta
        st.write("Resposta: Um ETF (Exchange-Traded Fund) é um fundo de investimento que pode ser negociado como uma ação na bolsa de valores.")

# Função para o feed de notícias
def feed_noticias():
    st.title("Notícias do Mercado Financeiro")

    api_key = "O7wcngTJlP1SKY44QzqLuaKBXwjrJzcSZanGcyYD"
    url = f"https://api.marketaux.com/v1/news/all?api_token={api_key}&filter_entities=true&language=pt"
    response = requests.get(url)

    if response.status_code == 200:
        noticias = response.json().get("data")

        if noticias:
            for noticia in noticias[:10]:  
                st.write(f"**{noticia['title']}**")
                st.write(noticia['description'])
                st.write(f"[Leia mais]({noticia['url']})")
                st.write("---")
        else:
            st.write("Nenhuma notícia disponível no momento.")
    else:
        st.write("Erro ao carregar notícias. Verifique sua chave de API ou limite de uso.")

# Função para a calculadora de impostos
def calculadora_impostos():
    st.title("Calculadora de Impostos sobre Investimentos")

    valor_investido = st.number_input("Valor investido", min_value=0.0)
    valor_resgatado = st.number_input("Valor resgatado", min_value=0.0)
    taxa_imposto = st.slider("Taxa de imposto sobre ganho de capital (%)", 0, 30, 15)

    if st.button("Calcular"):
        ganho = valor_resgatado - valor_investido
        if ganho > 0:
            imposto = ganho * (taxa_imposto / 100)
            st.write(f"Imposto a pagar: R${imposto:.2f}")
        else:
            st.write("Não há imposto a pagar, pois não houve ganho de capital.")

# Menu principal usando Streamlit
def main():
    st.sidebar.title("Menu")
    escolha = st.sidebar.radio("Selecione uma opção", 
                               ["Perfil do Investidor", 
                                "Recomendações de Investimentos", 
                                "Análise do Mercado",
                                "Análise de Ativo", 
                                "Chat Educacional", 
                                "Feed de Notícias",
                                "Calculadora de Impostos"])

    if escolha == "Perfil do Investidor":
        perfil_investidor()
    elif escolha == "Recomendações de Investimentos":
        recomendacoes_investimentos()
    elif escolha == "Análise do Mercado":
        analise_mercado()
    elif escolha == "Análise de Ativo":
        analise_ativo()
    elif escolha == "Chat Educacional":
        chat_educacional()
    elif escolha == "Feed de Notícias":
        feed_noticias()
    elif escolha == "Calculadora de Impostos":
        calculadora_impostos()

if __name__ == "__main__":
    main()
