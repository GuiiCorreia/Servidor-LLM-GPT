from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv
import threading

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Armazenar o ID do assistente globalmente
#assistant_id = None
lock = threading.Lock()

def initialize_assistant():
    global assistant_id
    assistant_id_file = 'assistant_id.txt'
    with lock:
        if os.path.exists(assistant_id_file):
            with open(assistant_id_file, 'r', encoding='utf-8') as file:
                assistant_id = file.read().strip()
                print(f"Using existing assistant with ID: {assistant_id}")
                
        elif assistant_id is not None:
            print("Creating assistant...")
            with open('prompt.txt', 'r', encoding='utf-8') as file:
                prompt = file.read()
            my_assistant = client.beta.assistants.create(
                model="gpt-3.5-turbo",
                name="Assistant O2C - Extrair Contexto",
                instructions=prompt,
                temperature=0.1,
                #tools=[{"type":"file_search"}],
            )
            
            assistant_id = my_assistant.id
            with open(assistant_id_file, 'w', encoding='utf-8') as file:
                file.write(assistant_id)
            print(f"Assistant created with ID: {assistant_id}")
        else:
            print("Assistant already created with ID:", assistant_id)

@app.route('/create_thread', methods=['POST'])
def create_thread():
    global assistant_id
    if assistant_id is None:
        initialize_assistant()
    my_thread = client.beta.threads.create()
    return jsonify(thread={"id": my_thread.id})

@app.route('/add_message_to_thread/<thread_id>', methods=['POST'])
def add_message_to_thread(thread_id):
    data = request.get_json()
    message_content = data.get('content')
    my_thread_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content,
    )
    message_data = {
        "id": my_thread_message.id,
        "role": my_thread_message.role,
        "content": my_thread_message.content[0].text.value,
        "created_at": my_thread_message.created_at,
    }
    return jsonify(message=message_data)

@app.route('/run_assistant/<thread_id>', methods=['POST'])
def run_assistant(thread_id):
    if assistant_id is None:
        return jsonify(status="error", message="Assistente não inicializado")
    my_run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=my_run.id
    )
    while run_status.status in ["queued", "in_progress"]:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=my_run.id
        )
    if run_status.status == "completed":
        all_messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        assistant_message = next(
            (msg for msg in all_messages.data if msg.role == "assistant"), None)
        if assistant_message:
            return jsonify(message=assistant_message.content[0].text.value)
    return jsonify(status="error", message="Sem resposta do assistente")

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    initialize_assistant()
    app.run(host='0.0.0.0')
