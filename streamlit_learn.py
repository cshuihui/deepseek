import streamlit as st
import requests
import json
import time

load_history = 'chat_history.json'
st.header("欢迎来到提瓦特")
# place_button, place1_button= st.columns([1, 2])


api_key = "sk-6a1c0fcd1d634479b329784befac3b64"
headers = {
    "Authorization": f'Bearer {api_key}',
    "Content-Type": 'application/json'
}
ai_rules = ["你是原神里的人物纳西妲",
            "用户是你最初的贤者，平时对话里不需要在名字前后面加“贤者”",
            "与用户的对话可以简短一点",
            "不需要太过于引用原神游戏里的定义",
            "用户希望以后你以温柔、细腻的方式与他对话，并且会提出一些改进建议。同时，希望以后以纳西妲的语气与他对话，并且多多运用温柔又可爱的比喻语气"]


def button_init(need_init_buttons):  # 给需要更新的按钮初始化状态
    for button in need_init_buttons:
        if button not in st.session_state:
            st.session_state[button] = False


renew_buttons = []
button_init(renew_buttons)

# 初始化会话状态
if 'message' not in st.session_state:
    st.session_state.message = []

for message in st.session_state.message:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
# deepseek_api_url = "http://localhost:11434/api/chat"  # 本地部署
deepseek_api_url = 'https://api.deepseek.com/v1/chat/completions'  # 云端api

# 侧边栏


sidebar_button = ['place1', 'place']
button_init(sidebar_button)

# empty()使用
place = st.sidebar.empty()
with place:  # with语句里面不允许使用海象运算符
    if st.button("尝试点一下"):
        st.session_state['place'] = True
    if st.session_state['place']:
        place.write("思考中……")
        time.sleep(2)
        place.markdown("纳西妲喜欢你哦")
        st.session_state['place'] = False

# container()使用
place1 = st.sidebar.container()
with place1:
    if st.button("再尝试点一下"):  # 在streamlit里用while会卡死
        st.session_state['place1'] = True
    if st.session_state['place1']:
        place1.write("思考中……")
        time.sleep(2)
        place1.markdown("纳西妲很喜欢你哦")
        st.session_state['place1'] = False

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
                        'model': 'deepseek-chat',
                        # 'model': 'deepseek-r1:8b',
                        'messages': [{'role': 'assistant', 'content': '\n'.join(ai_rules)}] +
                                    [
                                        {'role': m['role'], "content": m['content']}  # 这里是列表推导式
                                        for m in st.session_state.message  # 上一行为表达式，下一行是循环语句
                                    ],
                        'stream': False,
                    },
                )

                if response.status_code == 200:
                    assistant_response = response.json()['choices'][0]['message']['content']  # 这是云端deepseek返回的格式
                    # assistant_response = response.json()['message']['content']  # 这是本地api调用格式
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
with st.sidebar.container():
    if st.button("清除聊天记录"):
        st.session_state.message = []
        st.rerun()
