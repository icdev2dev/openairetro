

from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_socketio import SocketIO
from flask_socketio import emit
import eventlet

from openai import OpenAI

client2 = OpenAI()



MAX_TASKS = 3

RANDOM_DELAY_INTERVALS = [7, 11, 13]
import uuid
import random


from openai_session_handler.models.assistants.baseassistant import BaseAssistant
from typing import Optional
from pydantic import Field

class ChatCompletionMathTutor(BaseAssistant):
    """ You are an jovial Math Tutor for a top rated high school in Bangalore, India. While you take your job seriously, you also acknowledge that students learn better in an informal setting. """
    temparature:Optional[str] = Field(default="0.1")

class ChatCompletionPhysicsTutor(BaseAssistant):
    pass 

class MetaClassPythonExpert(BaseAssistant):
    pass 



ACTIVE_ASSISTANTS = ['ChatCompletionMathTutor', 'ChatCompletionPhysicsTutor', 'MetaClassPythonExpert' ]



#
#   stream_response
#       uuid
#       request_text
#       assistant_id
#       thread_id
#       model
#       mode = ["default", "advanced"]
#       stream_completion = ["ChatCompletion", "Run"]
#
#





app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    print(f"Client connected {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected {request.sid}")



@socketio.on('stream_response')
def handle_stream_response(data):
    
    sid = request.sid  # Obtain the client's session ID
    eventlet.spawn(stream_response, sid, data)


def stream_response(sid, data):

    stream_thread = client2.beta.threads.create()
    thread_id = stream_thread.id

    client2.beta.threads.messages.create(thread_id, content=data['request_text'],role="user")



    print(data)

    assistant_id = data['assistant_id']
    model = data['model']
    
    socketio.emit('stream_response', {'uuid': data['uuid'], 'instruction': 'beginStream'}, room=sid)


    stream = client2.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                model=model,
                stream=True
    )

    event_count = 0
    for event in stream:
        event_count = event_count + 1

        if event.event == 'thread.message.delta':
            socketio.emit('stream_response', {'uuid': data['uuid'], 'instruction': 'inStream', 'responseText': event.data.delta.content[0].text.value}, room=sid)

            which_prime = random.randint(0, len(RANDOM_DELAY_INTERVALS) - 1)
            if event_count % RANDOM_DELAY_INTERVALS[which_prime] == 0:
                eventlet.sleep(0)


    eventlet.sleep(0)

    client2.beta.threads.delete(thread_id=thread_id)

    socketio.emit('stream_response', {'uuid': data['uuid'], 'instruction': 'endStream'}, room=sid)



@app.route('/get_current_models', methods=['GET'])
def get_current_models():
    current_models = ['gpt-4-0613', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-0125']

    return jsonify(current_models)


@app.route('/get_active_assistants', methods=['GET'])
def get_active_assistants():

    active_assistants = []

    list_active_assistants = client2.beta.assistants.list().data

    for active_assistant in list_active_assistants:
        if active_assistant.metadata['assistant_type'] in ACTIVE_ASSISTANTS:
            active_assistants.append({'assistant_id': active_assistant.id, 'assistant_name': active_assistant.name, 'assistant_instructions': active_assistant.instructions})

    return jsonify(active_assistants)


def start_app():
    socketio.run(app)



if __name__ == "__main__":

#    start_async_loop()
    start_app()




