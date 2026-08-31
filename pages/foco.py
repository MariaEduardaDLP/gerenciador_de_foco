import time as t

import streamlit as st

def contar_tempo(tempo):

  with st.container(vertical_alignment="center", horizontal_alignment="center"):
    contador = st.empty()
    parar_contagem = st.form_submit_button(label="Parar")

  for x in range(0, tempo*60):
    contador.markdown(f"<p style='text-align: center; font-size: 4rem;'>{x//(60*60)}:{x//60}:{x}</p>", unsafe_allow_html=True)

    t.sleep(1)

    if parar_contagem: break

  st.balloons()
  st.success("Parabéns por ter concluído sua sessão de foco com sucesso!")
  st.image(image="https://i.pinimg.com/originals/f0/f7/46/f0f746550ba79a00b70af77ff690f23e.gif")

def main():
  st.header(body="Hora de focar!")

  with st.form("tempo_foco_min"):

    tempo_foco = st.slider(label="Tempo de foco (min)", max_value=180, min_value=5, step=5)

    focar = st.form_submit_button(label="Iniciar", width="stretch")

    if focar:
      contar_tempo(tempo_foco)


main()