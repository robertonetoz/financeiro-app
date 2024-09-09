import os
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests
import streamlit.components.v1 as components
from langflow.load import run_flow_from_json
import markdown
from markdown2 import markdown as md2html
import openai

# Estilo do Streamlit
st.set_page_config(page_title="Aplicativo Financeiro", page_icon="📈", layout="wide")

# Função para o chat com Buffet
def chat_com_buffet():
    with st.expander("💬 Chat com Buffet", expanded=True):
        st.markdown("### Converse com o Buffet")
        
        # Adiciona o widget de chat
        html_code = """
        <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.6/dist/build/static/js/bundle.min.js"></script>
        <langflow-chat
          window_title="Warren Buffett"
          flow_id="f44e61ee-0aa5-4e63-bdb5-0d44af5b0e93"
          host_url="http://localhost:7860"
        ></langflow-chat>
        """
        components.html(html_code, height=800)

# Função para recomendar investimentos
def recomendacoes_investimentos():
    with st.expander("💡 Recomendações de Investimentos", expanded=True):
        perfil = st.radio("Selecione o perfil de risco", ["Conservador", "Moderado", "Agressivo"])
        if perfil == "Conservador":
            st.info("Recomendamos: Tesouro Direto, CDB, Fundos de Renda Fixa")
        elif perfil == "Moderado":
            st.info("Recomendamos: Fundos Multimercados, Debêntures")
        elif perfil == "Agressivo":
            st.info("Recomendamos: Ações, ETFs, Criptomoedas")

# Função para analises
def analise_mercado_e_ativo():
    with st.expander("📊 Análise do Mercado Financeiro e Ativo Específico", expanded=True):
        # Seleção do tipo de análise
        tipo_analise = st.radio("Escolha o tipo de análise", ["Índice de Mercado", "Ativo Específico"])

        if tipo_analise == "Índice de Mercado":
            # Análise de índices de mercado
            mercado = st.selectbox("Selecione o índice do mercado", ["^GSPC", "^DJI", "^IXIC"])
            dados_mercado = yf.download(mercado, period="1mo", interval="1d")

            st.write(f"Exibindo dados do índice: {mercado}")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dados_mercado.index, y=dados_mercado['Close'], mode='lines', name='Fechamento'))
            st.plotly_chart(fig, use_container_width=True)

        elif tipo_analise == "Ativo Específico":
            # Análise de ativo específico
            ativo = st.text_input("Digite o código do ativo (ex: AAPL, TSLA)", "AAPL")
            
            # Chave da API Alpha Vantage
            api_key = "RN9SB6O0G6BJ7X7E"
            
            # URL da API Alpha Vantage
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ativo}&apikey={api_key}&outputsize=compact"
            
            # Faz a solicitação para a API
            response = requests.get(url)
            data = response.json()

            if "Time Series (Daily)" in data:
                # Extrair dados de preços
                time_series = data["Time Series (Daily)"]
                df = pd.DataFrame.from_dict(time_series, orient="index")
                df = df.rename(columns={
                    "1. open": "Open",
                    "2. high": "High",
                    "3. low": "Low",
                    "4. close": "Close",
                    "5. volume": "Volume"
                })
                df.index = pd.to_datetime(df.index)
                df = df.astype(float)
                
                # Exibe o preço atual
                st.write(f"Análise de {ativo}")
                st.write(f"Preço atual: {df['Close'].iloc[0]:.2f}")
                
                # Gráfico de fechamento
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Fechamento'))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Erro ao buscar dados do ativo. Verifique o código do ativo ou tente novamente mais tarde.")
        
        # Adiciona o widget Langflow
        st.write("### Para mais informações sobre ativos e do mercado financeiro, pergunte aqui!")
        html_code = """
        <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.6/dist/build/static/js/bundle.min.js"></script>
        <langflow-chat
          window_title="Ativos e Mercado Financeiro"
          flow_id="1c652faf-49cf-4f8a-b106-79d9dd75c54b"
          host_url="http://localhost:7860"
        ></langflow-chat>
        """
        components.html(html_code, height=800)


# Função para o chat educacional
def chat_educacional():
    with st.expander("💬 Chat de Educação Financeira", expanded=True):
        st.write("### Aprenda tópicos e assuntos sobre o mercado financeiro")

        # Adiciona o widget Langflow para chat
        html_code = """
        <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.6/dist/build/static/js/bundle.min.js"></script>
        <langflow-chat
          window_title="Aprenda sobre assuntos do mercado"
          flow_id="1c652faf-49cf-4f8a-b106-79d9dd75c54b"
          host_url="http://localhost:7860"
        ></langflow-chat>
        """
        components.html(html_code, height=800)


# Função para o feed de notícias
def feed_noticias():
    with st.expander("📰 Feed de Notícias", expanded=True):
        st.markdown("### Últimas notícias do mercado financeiro")

        api_key = "O7wcngTJlP1SKY44QzqLuaKBXwjrJzcSZanGcyYD"
        url = f"https://api.marketaux.com/v1/news/all?api_token={api_key}&filter_entities=true&language=pt"
        response = requests.get(url)

        if response.status_code == 200:
            noticias = response.json().get("data")

            if noticias:
                for noticia in noticias[:5]:  
                    st.write(f"**{noticia['title']}**")
                    st.write(noticia['description'])
                    st.write(f"[Leia mais]({noticia['url']})")
                    st.write("---")
            else:
                st.write("Nenhuma notícia disponível no momento.")
        else:
            st.error("Erro ao carregar notícias. Verifique sua chave de API ou limite de uso.")

        # Adiciona o widget Langflow
        st.write("### Para mais noticias do mundo financeiro, pergunte aqui")
        html_code = """
        <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.6/dist/build/static/js/bundle.min.js"></script>
        <langflow-chat
          window_title="Notícias do Mercado Financeiro"
          flow_id="1c652faf-49cf-4f8a-b106-79d9dd75c54b"
          host_url="http://localhost:7860"
        ></langflow-chat>
        """
        components.html(html_code, height=800)


# Função para a calculadora de impostos
def calculadora_impostos():
    with st.expander("💰 Calculadora de Impostos sobre Investimentos", expanded=True):
        valor_investido = st.number_input("Valor investido", min_value=0.0)
        valor_resgatado = st.number_input("Valor resgatado", min_value=0.0)
        taxa_imposto = st.slider("Taxa de imposto sobre ganho de capital (%)", 0, 30, 15)

        if st.button("Calcular"):
            ganho = valor_resgatado - valor_investido
            if ganho > 0:
                imposto = ganho * (taxa_imposto / 100)
                st.success(f"Imposto a pagar: R${imposto:.2f}")
            else:
                st.info("Não há imposto a pagar, pois não houve ganho de capital.")

# Menu principal usando Streamlit
def main():
    st.sidebar.title("Menu")
    escolha = st.sidebar.radio("Selecione uma opção", 
                               ["Chat com Buffet",
                                "Recomendações de Investimentos", 
                                "Análise do Mercado e Ativo Específico",  # Atualizado
                                "Chat Educacional", 
                                "Feed de Notícias",
                                "Calculadora de Impostos"])
    
    if escolha == "Chat com Buffet":
        chat_com_buffet()
    elif escolha == "Recomendações de Investimentos":
        recomendacoes_investimentos()
    elif escolha == "Análise do Mercado e Ativo Específico":  # Atualizado
        analise_mercado_e_ativo()  # Atualizado
    elif escolha == "Chat Educacional":
        chat_educacional()
    elif escolha == "Feed de Notícias":
        feed_noticias()
    elif escolha == "Calculadora de Impostos":
        calculadora_impostos()

if __name__ == "__main__":
    main()
