import gradio as gr
import requests

"""
Use Gradio library to create a form with a textbox to store the input text.
And API_KEY textbox to store the key.
Use api.openai.com to get the response.
"""


def generate_text(input_text, api_key, temperature, max_tokens, frequency_penalty, presence_penalty):
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    data = {
        "prompt": input_text,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    response = requests.post(url=url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Error: " + response.text


if __name__ == "__main__":
    gr.Interface(
        generate_text,  # function to be called
        [gr.inputs.Textbox(lines=1), gr.inputs.Textbox(lines=1), gr.inputs.Slider(minimum=0, maximum=1, step=0.01),
         gr.inputs.Slider(minimum=32, maximum=500, step=1), gr.inputs.Slider(minimum=0, maximum=1, step=0.01), gr.inputs.Slider(minimum=0, maximum=1, step=0.01)],  # input types
        gr.outputs.Textbox()  # output type
    ).launch()