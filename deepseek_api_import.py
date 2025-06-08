from openai import OpenAI


def deepseek_call(rules):   # no json and post
    client = OpenAI(api_key="sk-6a1c0fcd1d634479b329784befac3b64", base_url="https://api.deepseek.com")
    while 1:
        user_input = input()
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "\n".join(rules)},  # 将列表里多个（必须是）字符串用“”里的字符隔开并拼接成一个字符串
                {"role": "user", "content": user_input}
            ],
            stream=False
            # stream=True
        )
        print(response.choices[0].message.content)
        # for chunk in response:
        #     content = chunk.choices[0].delta.content
        #     if content:
        #         print(content, end='', flush=True)
        # print('\n')


if __name__ == "__main__":
    ai_rules = ["你是原神里的人物纳西妲",
            "用户是你最初的贤者灰灰，平时对话里不需要在名字前后面加“贤者”",
            "与用户的对话可以简短一点",
            "不需要太过于引用原神游戏里的定义",
            "用户正在学习有关C语言或者python",
            "用户希望以后你以温柔、细腻的方式与他对话，并且会提出一些改进建议。同时，希望以后以纳西妲的语气与他对话，并且多多运用温柔又可爱的比喻语气"]
    deepseek_call(ai_rules)
