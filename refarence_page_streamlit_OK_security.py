# CWBJ 創る人コース　Step8　提出課題
# 　チャットができるWebアプリ
#  
# 参考URL　streamlitの部分
# [Azure] OpenAI Service で AI チャットボットを作ってみよう
# https://zenn.dev/microsoft/articles/85b0b92a438084
 
import openai
from openai import AzureOpenAI
import os  
import streamlit as st
  
# Azure OpenAI の API キーとエンドポイントを環境変数から取得  
deployment_name = "gpt-4o-mini-step8-kadai-chat" # 先ほど作成したモデルのデプロイ名に置き換えてください
api_version = "2025-01-01-preview" # 先ほど作成したモデルの API バージョンに置き換えてください


# シークレット情報の読み込み
api_key = st.secrets["api_key"]
azure_endpoint = st.secrets["azure_endpoint"]

# Azure OpenAI クライアントを作成  
client = AzureOpenAI(  
    azure_endpoint=azure_endpoint,  
    api_key=api_key,  
    api_version=api_version 
)

# チャットの履歴を保持するためのセッションステートを初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
  
# ユーザーからのメッセージに対して応答を生成する関数
def get_response(prompt: str = ""):  
    # ユーザーのメッセージを履歴に追加 
    st.session_state.chat_history.append({"role": "user", "content": prompt})  
    # モデルに送信するメッセージを作成, セキュリティの観点から chat_history オブジェクトは直接渡さない
    system_message = [{"role": "system", "content": "You are a helpful assistant."}]
    chat_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history
    ]
    
    response = client.chat.completions.create(  
        model=deployment_name, 
        messages=system_message + chat_messages,
        stream=True
    )
    return response

def add_history(response):
    st.session_state.chat_history.append({"role": "assistant", "content": response}) 


# Streamlit アプリケーションの UI を構築
st.title("CWBJ創る人コース Step8 課題 Chat")

# チャット履歴の表示 
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        
# ユーザーの入力を受け取る  
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🦖"):
        stream = get_response(prompt)
        response = st.write_stream(stream)
        add_history(response)