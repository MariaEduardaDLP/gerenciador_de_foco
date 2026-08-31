import streamlit as st
from google.cloud import firestore

BANCO_DADOS = firestore.Client.from_service_account_json("firebase.json")
st.set_page_config(page_title="Tarefas", page_icon=":material/book_ribbon:", layout="wide", initial_sidebar_state="collapsed")

def pegar_tarefas():

  tarefas = []

  for tarefa in BANCO_DADOS.collection("tarefas").stream():
    tarefa_quadro = tarefa.to_dict()
    tarefas.append(tarefa_quadro)
  
  return tarefas

def recarregar_tarefas():

  tarefas = pegar_tarefas()

  if not tarefas:
    st.info(body="Não há tarefas adicionadas")
  else:
    st.data_editor(data=tarefas, column_config={ 
      "status": st.column_config.SelectboxColumn(
        "Status",
        options=["Não iniciada", "Concluída", "Em progresso"]
      ),
      "nome": "Nome",
      "id": None
    }, disabled=["id"], key="dados_editados", on_change=atualizar_tarefa)

def excluir_tarefas(lista_tarefas):

  for tarefa in lista_tarefas:
    BANCO_DADOS.collection("tarefas").document(tarefa["id"]).delete()

def atualizar_tarefa():

  dados_atualizados = st.session_state["dados_editados"]["edited_rows"]

  tarefas = pegar_tarefas()

  for id in dados_atualizados.items():
    BANCO_DADOS.collection("tarefas").document(tarefas[id[0]]["id"]).update(id[1])

    st.success(body="Dados alterados com sucesso!")

def main():

  with st.form("nova_tarefa"):

    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
      nova_tarefa = st.text_input(label="Nova tarefa", icon=":material/list_alt_add:", placeholder="Digite a sua tarefa do dia...")

    with col2:
      status = st.selectbox(label="Andamento da tarefa", options=("Não iniciada", "Concluída", "Em progresso"))

    with col3:
      enviado = st.form_submit_button(label="Adicionar", width="stretch")

    if enviado:
      tarefa_criada = BANCO_DADOS.collection("tarefas").document()
      tarefa_criada.set(
        {
          "id": tarefa_criada.id,
          "nome": nova_tarefa,
          "status": status
        }
      )

      st.toast(body="Tarefa criada!", duration="short")

  with st.form("excluir_tarefas"):

    col1, col2 = st.columns([4, 1])

    with col1:
      tarefas_selecionadas = st.multiselect(label="Excluir tarefas", options=pegar_tarefas(), format_func=lambda tarefa: tarefa["nome"])

    with col2:
      excluir = st.form_submit_button(label="Excluir", width="stretch", icon=":material/delete:")

    if not tarefas_selecionadas and excluir:
      st.warning(body="Nenhuma tarefa selecionada")
    elif excluir:
      excluir_tarefas(tarefas_selecionadas)
      st.toast(body="Tarefas excluídas!", duration="short")

  recarregar_tarefas()

main()