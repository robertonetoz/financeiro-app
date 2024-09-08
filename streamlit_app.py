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
                "SequentialCrewComponent-AoXgm": {
                    "max_rpm": 100,
                    "memory": False,
                    "share_crew": False,
                    "use_cache": True,
                    "verbose": 0
                },
                "ChatOutput-kcdMZ": {
                    "data_template": "{text}",
                    "input_value": pergunta,
                    "sender": "Machine",
                    "sender_name": "AI",
                    "session_id": "",
                    "should_store_message": True
                },
                "TextInput-q5KbN": {
                    "input_value": pergunta
                },
                "Prompt-m0j1W": {
                    "template": "Topic: {topic}\n\nBuild a document about this document.",
                    "topic": pergunta
                },
                "Prompt-vu8ox": {
                    "template": "Topic: {topic}\n\nRevise this document.",
                    "topic": pergunta
                },
                "Prompt-ajPtk": {
                    "template": "Topic: {topic}\n\nEscreva um resumo conciso, mas informativo, trazendo especialmente as informações mais atuais e dados quantitativos.",
                    "topic": pergunta
                },
                "SequentialTaskAgentComponent-pkN2P": {
                    "agent_kwargs": {},
                    "allow_code_execution": False,
                    "allow_delegation": False,
                    "async_execution": False,
                    "backstory": "criar relatórios de informações relevantes, com dados e cenários econômicos.",
                    "expected_output": "Bullet points and small phrases about the research topic.",
                    "goal": "Buscar notícias mais atuais, especialmente do mesmo dia",
                    "memory": True,
                    "role": "Pesquisador",
                    "task_description": "",
                    "verbose": True
                },
                "SequentialTaskAgentComponent-tuwOX": {
                    "agent_kwargs": {},
                    "allow_code_execution": False,
                    "allow_delegation": False,
                    "async_execution": False,
                    "backstory": "You are the editor of the most reputable journal in the world.",
                    "expected_output": "Small paragraphs and bullet points with the corrected content.",
                    "goal": "You should edit the Information provided by the Researcher to make it more palatable and to not contain misleading information.",
                    "memory": True,
                    "role": "Editor",
                    "task_description": "",
                    "verbose": True
                },
                "SequentialTaskAgentComponent-saOps": {
                    "agent_kwargs": {},
                    "allow_code_execution": False,
                    "allow_delegation": False,
                    "async_execution": False,
                    "backstory": "Developed as a response to the growing need for real-time asset valuation in volatile markets, the agent was trained on vast datasets of historical market trends, corporate financials, and macroeconomic indicators. Initially designed to assist institutional investors, the agent quickly proved invaluable in predicting market shifts and asset pricing with high accuracy. Its algorithmic foundation is built on deep learning models that factor in both quantitative data and qualitative news analysis, making it highly versatile in various financial environments.",
                    "expected_output": "Escreva as informações em tópicos curtos e informativos, em português.",
                    "goal": "The agent's primary goal is to continuously monitor financial markets, assess the value of various assets, and predict future price movements. It aims to enhance decision-making for investors by offering accurate pricing models, risk assessments, and timely advice based on both historical and real-time data. The agent also adapts its strategies based on market shifts to optimize performance in varying conditions.",
                    "memory": True,
                    "role": "The agent is an expert in financial asset pricing, capaz de analisar dados de mercado, identificar tendências e fornecer informações em tempo real sobre avaliações de ativos. Utiliza modelos avançados para calcular previsões de preços, avaliar riscos e oferecer recomendações de investimento para uma variedade de instrumentos financeiros, como ações, títulos e commodities.",
                    "task_description": "",
                    "verbose": True
                },
                "DuckDuckGoSearchAPI-JZWLu": {
                    "input_value": pergunta
                },
                "ChatInput-b5XMZ": {
                    "files": "",
                    "input_value": pergunta,
                    "sender": "User",
                    "sender_name": "User",
                    "session_id": "",
                    "should_store_message": True
                },
                "AIMLModel-FpMCK": {
                    "aiml_api_base": "",
                    "api_key": "c6d20860e1f24a6da42f1d496cf0a66b",
                    "input_value": {
                        "text_key": "text",
                        "data": {
                            "text": pergunta,
                            "files": [],
                            "timestamp": "2024-09-07 18:31:19",
                            "flow_id": "1c091528-eacd-4c5c-a018-8b5362438ae9"
                        },
                        "default_value": "",
                        "text": pergunta,
                        "files": [],
                        "session_id": "",
                        "timestamp": "2024-09-07 18:31:19",
                        "flow_id": "1c091528-eacd-4c5c-a018-8b5362438ae9"
                    },
                    "max_tokens": None,
                    "model_kwargs": {},
                    "model_name": "gpt-4-turbo",
                    "seed": 1,
                    "stream": False,
                    "system_message": "",
                    "temperature": 0.1
                }
            }

            # Executar o fluxo
            result = run_flow_from_json(
                flow="Sequential Tasks Agent.json",
                input_value=pergunta,
                fallback_to_env_vars=True,
                tweaks=TWEAKS
            )

            # Mostrar o resultado
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
