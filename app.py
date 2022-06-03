import json
from config import api_key
import requests

headers = {
        'authorization': api_key, 
        'content-type': 'application/json'
    } 

def sumbit_transcription(body):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    try:
        res = requests.post(endpoint, json=body, headers=headers)
        return {'status': res.json().get('status'),
        'id': res.json().get('id')
        }
    except Exception as e:
        return {'status': 'error'}


def hello(audio_url, speaker_labeling):
    body = {
        'audio_url': audio_url
    }
    
    res = sumbit_transcription(body)
    
    list_of_transcriptions['entries'][res.get('id')] = res.get('status') 
    with open('transcriptions.json', 'w') as f:
        json.dump(list_of_transcriptions, f)

    return res.get('id')

def get_status(transcription_id):
    print('--->', transcription_id)
    endpoint_status = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"
    print('--->', endpoint_status)
    res = requests.get(endpoint_status, headers=headers)
    list_of_transcriptions['entries'][transcription_id] = res.json().get('status')
    with open('transcriptions.json', 'w') as f:
        json.dump(list_of_transcriptions, f)

    return res.json().get('status')

def get_results(transcription_id):
    endpoint_result = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"
    res = requests.get(endpoint_result, headers=headers)
    return res.json().get('text')

def refresh_list():
    results = '''Transaction ID \t\t\t\t Status\n'''
    for entry, status in list_of_transcriptions['entries'].items():
        results += f'{entry} {status}'

    return list_of_transcriptions['entries'].items()

import gradio as gr 

demo = gr.Blocks()

with demo:
    gr.Markdown('![#c5f015](https://i.ytimg.com/vi/-NRGVCHI4WM/maxresdefault.jpg)')
    with gr.Tabs():
        with gr.TabItem('Submit Audio for Transcription'):
            text_input = gr.Textbox(label='Audio URL')
            speaker_choice  = gr.Checkbox(label='Speaker Labeling')
            output = gr.Textbox(label='Transcrption ID')
            text_button = gr.Button('Submit')
        with gr.TabItem('Get Transcription Status'):
            transcription_id_status = gr.Textbox(label='Transcription ID')
            status = gr.Textbox(label='Status')
            status_button = gr.Button('Get Status')
        with gr.TabItem('Submittted Transcriptions'):
            list_of_transcriptions = {}
            with open('transcriptions.json', 'r') as f:
                list_of_transcriptions = json.load(f)
            print(list_of_transcriptions['entries'])
            data_frame = gr.DataFrame(list(list_of_transcriptions['entries'].items()), headers=['Transaction ID', 'status'])
            # refresh_button = gr.Button('Refresh')
        with gr.TabItem('Get Transcription Result'):
            transcription_id = gr.Textbox(label='Transcription ID')
            results = gr.Textbox(label='Full Transcript')
            results_button = gr.Button('Get Full Transctipt')

    text_button.click(hello, inputs=[text_input, speaker_choice], outputs=output)
    status_button.click(get_status, inputs=transcription_id_status, outputs=status)
    results_button.click(get_results, inputs=[transcription_id], outputs=results)
    # refresh_button.click(refresh_list, inputs = None, outputs=None)
# iface = gr.Interface(fn=hello, inputs=['text', 'checkbox'], outputs=['text'])

if __name__ == "__main__":
    # iface.launch(server_port=7860, debug=True)
    demo.launch(server_port=7860, debug=True)