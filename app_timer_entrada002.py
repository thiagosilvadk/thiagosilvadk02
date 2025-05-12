
import streamlit as st
import time

st.set_page_config(page_title="Blaze Branco V2", layout="centered", page_icon="🎯")
st.markdown("# 🎯 Blaze Branco V2 – Estratégia Ativa")
st.markdown("Insira os resultados da roleta e receba previsões com base em padrões avançados.")

# Inicializar sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "ultima_entrada" not in st.session_state:
    st.session_state.ultima_entrada = time.time()

# Exibir cronômetro
def mostrar_cronometro():
    tempo_decorrido = int(time.time() - st.session_state.ultima_entrada)
    tempo_restante = max(0, 15 - (tempo_decorrido % 15))
    st.markdown(f"### 🕒 Próxima rodada em: `{tempo_restante}` segundos")

# Mostrar histórico com quadrado colorido
def mostrar_historico():
    st.markdown("### 🧾 Histórico (últimos 30):")
    historico_exibicao = st.session_state.historico[-30:][::-1]
    for cor, numero in historico_exibicao:
        if cor == "vermelho":
            cor_html = f'<div style="display:inline-block; background-color:#ff4d4d; color:white; padding:6px 12px; border-radius:8px; margin:2px;">{numero}</div>'
        elif cor == "preto":
            cor_html = f'<div style="display:inline-block; background-color:#333; color:white; padding:6px 12px; border-radius:8px; margin:2px;">{numero}</div>'
        else:  # branco
            cor_html = f'<div style="display:inline-block; background-color:#ddd; color:black; padding:6px 12px; border-radius:8px; margin:2px; border:1px solid #999;">{numero}</div>'
        st.markdown(cor_html, unsafe_allow_html=True)

# Verificar padrões e alertas
def verificar_alerta():
    historico = st.session_state.historico
    cores = [cor for cor, _ in historico]

    alerta = ""
    entrada_ativa = False

    if len(cores) >= 15 and cores[-10:].count("preto") >= 10 and cores[-15:].count("vermelho") >= 5:
        alerta += "⚠️ **10 pretos + 5 vermelhos detectados!**
"
        entrada_ativa = True
    if len(cores) >= 130 and "branco" not in cores[-130:]:
        alerta += "⚠️ **Ausência de branco nas últimas 130 jogadas!**
"
        entrada_ativa = True
    if ''.join(cores[-24:]) == "pretopretopreto"*8:
        alerta += "⚠️ **Padrão raro: 12P + 8P + 4V pode estar próxima.**
"
        entrada_ativa = True
    if len(cores) >= 7 and cores[-7:] == ["vermelho"]*7:
        alerta += "⚠️ **Após 7 vermelhos, tendência de vir 14 encontrada.**
"
        entrada_ativa = True
    if len(cores) >= 9:
        seq = cores[-9:]
        if seq[0:4] == ["vermelho"]*4 and seq[5:9] == ["vermelho"]*4:
            alerta += "⚠️ **Confirmação: 4V + 4V detectado — possível branco a seguir!**
"
            entrada_ativa = True

    return alerta.strip(), entrada_ativa

# Entrada de nova jogada
st.markdown("## 🎰 Inserir nova jogada:")
col1, col2 = st.columns(2)
with col1:
    cor = st.selectbox("Cor", ["vermelho", "preto", "branco"])
with col2:
    numero = st.number_input("Número sorteado", min_value=0, max_value=14, step=1)

if st.button("Adicionar"):
    st.session_state.historico.append((cor, numero))
    st.session_state.ultima_entrada = time.time()

# Mostrar cronômetro
mostrar_cronometro()

# Mostrar histórico
if st.session_state.historico:
    mostrar_historico()

    alerta, entrada = verificar_alerta()
    if alerta:
        st.markdown("---")
        st.markdown("### 🚨 ALERTAS:")
        st.warning(alerta)
    if entrada:
        st.success("✅ **ENTRADA ATIVA: Apostar no Branco!**")
