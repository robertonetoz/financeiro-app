import os
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests
import streamlit.components.v1 as components
from langflow.load import run_flow_from_json

# Estilo do Streamlit
st.set_page_config(page_title="Aplicativo Financeiro", page_icon="📈", layout="wide")

# Função para exibir o formulário de perfil do investidor
def perfil_investidor():
    with st.expander("📝 Análise de Perfil do Investidor", expanded=True):
        idade = st.slider("Idade", 18, 100)
        risco = st.selectbox("Nível de risco", ["Conservador", "Moderado", "Agressivo"])
        objetivo = st.text_input("Objetivo financeiro")
        prazo = st.selectbox("Prazo do investimento", ["Curto prazo", "Médio prazo", "Longo prazo"])

        if st.button("Analisar perfil"):
            st.success(f"Perfil analisado: Idade {idade}, Risco {risco}, Objetivo: {objetivo}, Prazo: {prazo}")

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

# Função para análise de mercado
def analise_mercado():
    with st.expander("📊 Análise do Mercado Financeiro", expanded=True):
        mercado = st.selectbox("Selecione o índice do mercado", ["^GSPC", "^DJI", "^IXIC"])
        dados_mercado = yf.download(mercado, period="1mo", interval="1d")

        st.write(f"Exibindo dados do índice: {mercado}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dados_mercado.index, y=dados_mercado['Close'], mode='lines', name='Fechamento'))
        st.plotly_chart(fig, use_container_width=True)

# Função para análise de ativo específico
def analise_ativo():
    with st.expander("🔍 Análise de Ativo Específico", expanded=True):
        ativo = st.text_input("Digite o código do ativo (ex: AAPL, TSLA)", "AAPL")
        dados_ativo = yf.Ticker(ativo)
        historico = dados_ativo.history(period="1mo")

        st.write(f"Análise de {ativo}")
        st.write(f"Preço atual: {historico['Close'][-1]}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=historico.index, y=historico['Close'], mode='lines', name='Fechamento'))
        st.plotly_chart(fig, use_container_width=True)

# Função para o chat educacional
def chat_educacional():
    with st.expander("💬 Chat de Educação Financeira", expanded=True):
        pergunta = st.text_input("Pergunte sobre educação financeira", "O que é um ETF?")

        if st.button("Perguntar"):
            st.write(f"Pergunta: {pergunta}")

            TWEAKS = {
                "SequentialCrewComponent-PG3Bu": {
                    "max_rpm": 100,
                    "memory": False,
                    "share_crew": False,
                    "use_cache": True,
                    "verbose": 0
                },
                "OpenAIModel-n4CxW": {
                    "api_key": "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",
                    "input_value": pergunta,
                    "json_mode": False,
                    "max_tokens": None,
                    "model_kwargs": {},
                    "model_name": "gpt-4",
                    "openai_api_base": "",
                    "output_schema": {},
                    "seed": 1,
                    "stream": False,
                    "system_message": "",
                    "temperature": 0.1
                },
                "ChatOutput-Kxx85": {
                    "data_template": "{text}",
                    "input_value": "",
                    "sender": "Machine",
                    "sender_name": "AI",
                    "session_id": "",
                    "should_store_message": True
                },
                "TextInput-MUVRZ": {
                    "input_value": pergunta
                }
            }

            result = run_flow_from_json(
                flow="Sequential Tasks Agent.json",
                input_value=pergunta,
                fallback_to_env_vars=True,
                tweaks=TWEAKS
            )

            st.write("Resposta do Modelo:", result)





# Função para o feed de notícias
def feed_noticias():
    with st.expander("📰 Feed de Notícias", expanded=True):
        st.markdown("### Últimas notícias do mercado financeiro")

        # Adiciona o widget de chat
        html_code = """
        <script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.6/dist/build/static/js/bundle.min.js"></script>
        <langflow-chat
          window_title="Mercado Financeiro Atendimento"
          flow_id="37e6036f-9e04-4e26-b83c-5783a46b98c5"
          host_url="http://localhost:7860"
          api_key="sk-_mWX47Dh_jg1zvQ4ALOugqC9PIWkegEkEGQP2Bh2880"
        ></langflow-chat>
        """
        components.html(html_code, height=800)

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
