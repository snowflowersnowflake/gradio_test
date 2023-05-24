import gradio as gr
import random
import time
import whisper
import openai
import os

openai.organization = "org-ExlVt8dQWG8ynJS4uYbF3o6Q"
openai.api_key = "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"
prepend_prompt = "用户这样说道："
append_prompt = "一个保险基金经理会这样回答用户："


# while True:
#     conversation = input("用户说道：")
#     if conversation == 'quit':
#         break
#     else:

def speech_to_text(tmp_filename, model_size):
    model = whisper.load_model(model_size)
    result = model.transcribe(tmp_filename)
    return result["text"]


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    # msg = gr.Textbox()
    clear = gr.Button("Clear")


    def respond(message, chat_history):
        # try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prepend_prompt + message + "。" + append_prompt,
            temperature=1,
            max_tokens=2000,
            frequency_penalty=0,
            presence_penalty=0
        )
        bot_message = random.choice(["我不知道你在说什么", "I love you", "I'm very hungry"])
        answer = response["choices"][0]["text"]
        print("到这里1", answer,answer.find(append_prompt))
        # if answer.find(append_prompt) >= 0:
        #     print("到这里3")
        #     answer = answer[answer.find(append_prompt) + len(append_prompt):]
        #     bot_message = answer


            # print(f"咨询师答：{answer}")
        # except Exception as exc:
        #     print(exc)

        bot_message = answer
        print("到这里2")
        chat_history.append((message, bot_message))
        time.sleep(1)
        return "", chat_history


    # def greet(name):
    #     return "Hello " + name + "!"
    out_spec = gr.Textbox(label="您的语音输入识别结果为...")
    # 不可交互
    # output = gr.Textbox(label="Output Box")
    # 可交互
    # output = gr.Textbox(label="提交您的语音输入结果到机器人", interactive=True)

    out_spec.submit(respond, [out_spec, chatbot], [out_spec, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

    greet_btn = gr.Button("语音识别")
    greet_btn.click(fn=speech_to_text, inputs=[
        gr.Audio(source="microphone", type="filepath"),
        gr.Dropdown(choices=["tiny", "base", "small", "medium", "large"]),
    ], outputs=out_spec)

if __name__ == "__main__":
    demo.launch(server_port=8080)
