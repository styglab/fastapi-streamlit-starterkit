import streamlit as st
import time
from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import validate_token, get_user_info
from modules.security.encryption import str_to_asterisk
from modules.validation.key_validation import validate_openai_api_key
from modules.validation.form_validation import validate_text

from modules.osstem.api_rag import get_batch_rag

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "token_status" not in st.session_state:
    st.session_state["token_status"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "key_status" not in st.session_state:
    st.session_state["key_status"] = None
if st.session_state["auth_status"]==True:
    st.session_state["user_info"] = get_user_info(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])


#redirect
if not st.session_state["auth_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")
st.session_state["token_status"] = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])["status"]
if not st.session_state["token_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")

#settings

#page
set_page_config(auth_status=st.session_state["auth_status"],
                layout="wide")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])

#style
style_global()

#custom style
with open('/app/src/modules/quiz/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

#func
def reset_conversation():
  #message 초기화
  st.session_state["rag_messages"] = [st.session_state["rag_messages"][0]]
  ##st.session_state.chat_history = None
  
#title
col_1, col_2 = st.columns([1,1])
with col_1:
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> RAG 답변 생성 </div>""", unsafe_allow_html=True)
with col_2:
    col_2_1, col_2_2, col_2_3 = st.columns([8,1,1])
    with col_2_2:
        if st.button(":material/account_circle:",key="df", use_container_width=False):
            st.switch_page("pages/my_profile.py")
    with col_2_3:     
        if st.button(":material/logout:",key="asdf", use_container_width=False):
            st.session_state = {}
            st.switch_page("main.py")
st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
#main

username = st.session_state["user_info"]["username"]
if "rag_messages" not in st.session_state:
    st.session_state["rag_messages"] = [{"role": "assistant", "content": f"안녕하세요 {username} 님 !  \n '퀴즈 생성' 버튼을 클릭하여 퀴즈를 생성해 주세요!","ref1":"1","ref2":"2","ref3":"3"}]

if "rag_ready" not in st.session_state:
    st.session_state["rag_ready"] = False

# 답변 ui 만들기

with st.container(height=500):
    if st.session_state["rag_messages"]:
        for idx, msg in enumerate(st.session_state["rag_messages"]):
            with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                with st.container():
                    st.markdown(msg["content"])
                    if (idx !=0) and (msg["role"]=="assistant"):
                        col1,col2,col3 = st.columns([1,1,1])
                        with col1:
                            with st.popover("Reference1",use_container_width=True):
                                st.markdown(msg["ref1"])
                        with col2:
                            with st.popover("Reference2",use_container_width=True):
                                st.markdown(msg["ref2"])
                        with col3:
                            with st.popover("Reference3",use_container_width=True):
                                st.markdown(msg["ref1"])
                        # with st.expander("Reference1"):
                        #     st.markdown(msg["ref1"])
                        # with st.expander("Reference2"):
                        #     st.markdown(msg["ref2"])
                        # with st.expander("Reference3"):
                        #     st.markdown(msg["ref3"])
        question = st.empty()
        answer = st.empty()
        if st.session_state["rag_ready"]:
            with st.spinner('답변 중입니다...'):
                generated_text = get_batch_rag(
                    token_type = st.session_state["token_type"], 
                    access_token = st.session_state["access_token"],
                    openai_api_key = st.session_state["openai_api_key"],
                    query = st.session_state["rag_messages"][-1]["content"]
                )

            generated_text = generated_text["results"]

            with answer.chat_message(name="assistant", avatar="/app/src/images/bot_icon_2.jpg"):
                with st.container():
                    st.markdown(generated_text[0])
                    col1,col2,col3 = st.columns([1,1,1])
                    with col1:
                        with st.popover("Reference1",use_container_width=True):
                            st.markdown(generated_text[1])
                    with col2:
                        with st.popover("Reference2",use_container_width=True):
                            st.markdown(generated_text[2])
                    with col3:
                        with st.popover("Reference3",use_container_width=True):
                            st.markdown(generated_text[3])
                st.session_state["rag_messages"].append({"role": "assistant", "content": generated_text[0],"ref1":generated_text[1],"ref2":generated_text[2],"ref3":generated_text[3]})
            st.session_state["rag_ready"]=False
            
if prompt := st.chat_input("번역할 문장을 입력해 주세요"):
    with question.chat_message(name="user", avatar="/app/src/images/bot_icon_2.jpg"):
        st.markdown(prompt)
    st.session_state["rag_messages"].append({"role":"user","content":prompt, "ref1":"1", "ref2":"2","ref3":"3"})
    st.session_state["rag_ready"] = True
    st.rerun()

    
        