import streamlit as st
import requests
import json
import deepseek_api_import as dp

st.title("欢迎来到提瓦特")

# 初始化会话状态
if 'message' not in st.session_state:
    st.session_state.message = []

for message in st.session_state.message:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
# deepseek_api_url = "http://localhost:11434/api/chat"  # 本地部署
deepseek_api_url = 'https://api.deepseek.com/v1/chat/completions'  # 云端api

api_key = "sk-6a1c0fcd1d634479b329784befac3b64"
headers = {
    "Authorization": f'Bearer {api_key}',
    "Content-Type": 'application/json'
}

# 用户输入
if user_input := st.chat_input("你想对纳西妲说什么呢"):
    # 添加用户信息至聊天记录
    st.session_state.message.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # 调用api
    with st.chat_message('assistant'):
        with st.spinner("思考中……"):
            try:
                response = requests.post(
                    url=f'{deepseek_api_url}',
                    headers=headers,
                    json={
                        'model': 'deepseek-reasoner',
                        #'model': 'deepseek-r1:8b',
                        'messages': [
                            {'role': m['role'], "content": m['content']}  # 这里是列表推导式
                            for m in st.session_state.message  # 上一行为表达式，下一行是循环语句
                        ],
                        'stream': False,
                    },
                )

                if response.status_code == 200:
                    assistant_response = response.json()['choices'][0]['message']['content']  # 这是云端deepseek返回的格式
                    #assistant_response = response.json()['message']['content']  # 这是本地api调用格式
                    st.markdown(assistant_response)
                    st.session_state.message.append(
                        {'role': 'assistant', 'content': assistant_response}
                        # 是一个按对话顺序排列的列表，每条记录是一个字典，包含 'role' 和 'content'
                    )
                else:
                    st.error(f'Api调用失败：{response.status_code}')
                    st.error(response.text)
            except Exception as e:  # Exception 是所有普通错误的“妈妈类”，能抓住大部分的错误
                st.error(f'发生错误：{str(e)}')
if st.button("清除聊天记录"):
    st.session_state.message = []
    st.rerun()
