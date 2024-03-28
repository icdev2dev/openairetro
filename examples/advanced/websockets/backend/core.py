from typing import Dict, List, Optional, Type, TypeVar


from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_socketio import SocketIO
from flask_socketio import emit
import eventlet

from openai import OpenAI


import uuid
import random


from openai_session_handler.models.assistants.baseassistant import BaseAssistant
from openai_session_handler.models.threads.basethread import BaseThread


from typing import Optional
from pydantic import Field


client2 = OpenAI()

T = TypeVar('T', bound='ReplaceableThread')

MAX_TASKS = 3
ACTIVE_ASSISTANTS = ['ChatCompletionMathTutor', 'ChatCompletionPhysicsTutor', 'MetaClassPythonExpert' ]
RANDOM_DELAY_INTERVALS = [7, 11, 13]

class ChatCompletionMathTutor(BaseAssistant):
    """ You are an jovial Math Tutor for a top rated high school in Bangalore, India. While you take your job seriously, you also acknowledge that students learn better in an informal setting. """
    temparature:Optional[str] = Field(default="0.1")

class ChatCompletionPhysicsTutor(BaseAssistant):
    pass 

class MetaClassPythonExpert(BaseAssistant):
    pass 



class ReplaceableAssistant(BaseAssistant):
    """ You are omnipotent allknowing philosopher who can opine about different terms in different contexts."""


class ReplaceableThread(BaseThread):
    side_thread:Optional[str] = Field(default="")

    @classmethod
    def create(cls:Type[T], **kwargs) -> T:
        real_side_thread = client2.beta.threads.create()        
        thread = super().create(side_thread = real_side_thread.id )
        return thread
       
    @classmethod
    def delete(cls:Type[T], thread_id) :
        r_thread = cls.retrieve(thread_id=thread_id)
        client2.beta.threads.delete(thread_id=r_thread.side_thread)
        return super().delete(thread_id=thread_id)

    @classmethod
    def clone_rev(cls:Type[T], thread_id):

        print(f"in clone rev {thread_id}")
        c_thread = client2.beta.threads.retrieve(thread_id)
        r_thread = client2.beta.threads.create()

        real_messages = client2.beta.threads.messages.list(c_thread.id, order='desc')
        
        for message in real_messages:
            client2.beta.threads.messages.create(r_thread.id, content=message.content[0].text.value,  role='user')

        print(f"in clone rev rthread {r_thread.id}")

        return r_thread.id
    



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    print(f"Client connected {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected {request.sid}")




@socketio.on('stream_response_replaceable')
def handle_stream_response_replaceable(data):
    sid = request.sid  # Obtain the client's session ID

    if 'cmd' in data:
        if data['cmd'] == "create_replaceable_thread":
            thread = ReplaceableThread.create()
            socketio.emit('stream_response_replaceable', 
                          {'uuid': data['uuid'], 
                           'cmd_executed': 'create_replaceable_thread', 
                           'thread_id': thread.id
                           }, 
                           room=sid)

        elif data['cmd'] == "delete_replaceable_thread" and 'thread_id' in data:
            ReplaceableThread.delete(thread_id=data['thread_id'])
            socketio.emit('stream_response_replaceable', 
                          {'uuid': data['uuid'], 
                           'cmd_executed': 'delete_replaceable_thread'
                           }, 
                           room=sid)

        elif data['cmd'] == "list_messages_in_thread" and 'thread_id' in data:
            real_messages = client2.beta.threads.messages.list(thread_id=data['thread_id']).data

            messages = []

            for message in real_messages:
                messages.append(message.id)



            socketio.emit('stream_response_replaceable', 
                          {'uuid': data['uuid'], 
                           'cmd_executed': 'list_messages_in_thread',
                           'messages': messages
                           }, 
                           room=sid)
            
        elif data['cmd'] == "stream_response" and 'thread_id' in data and 'request_text' in data:
            
            print("in here")
            r_thread = ReplaceableThread.retrieve(data['thread_id'])
            s_thread_id = r_thread.side_thread

            real_messages = client2.beta.threads.messages.list(thread_id=s_thread_id).data
            
            if len(real_messages) < 2: 
                client2.beta.threads.messages.create(s_thread_id, content=data['request_text'],role="user")

            eventlet.spawn(stream_response_replaceable, sid, data, s_thread_id)


    else :
        print("This is a NOOP")


def stream_response_replaceable(sid, data, s_thread_id):

    print("in spawn")



    socketio.emit('stream_response_replaceable', {'uuid': data['uuid'], 
                                                  'cmd_executed': 'stream_response',
                                                  'instruction': 'beginStream'}, 
                                                  room=sid)

    c_assistant = ReplaceableAssistant.create()
    c_thread = ReplaceableThread.clone_rev(s_thread_id)

    stream = client2.beta.threads.runs.create(
                thread_id=c_thread,
                assistant_id=c_assistant.id,
                stream=True
    )


    event_count = 0
    for event in stream:
        event_count = event_count + 1

        if event.event == 'thread.message.delta':
            socketio.emit('stream_response_replaceable', {'uuid': data['uuid'], 
                                                          'cmd_executed': 'stream_response',
                                                          'instruction': 'inStream', 
                                                          'responseText': event.data.delta.content[0].text.value}
                                                          , room=sid)

            which_prime = random.randint(0, len(RANDOM_DELAY_INTERVALS) - 1)
            if event_count % RANDOM_DELAY_INTERVALS[which_prime] == 0:
                eventlet.sleep(0)
    eventlet.sleep(0)

    client2.beta.threads.delete(c_thread)
    ReplaceableAssistant.delete(c_assistant.id)

    socketio.emit('stream_response_replaceable', {'uuid': data['uuid'],
                                                  'cmd_executed': 'stream_response', 
                                                  'instruction': 'endStream'}, room=sid)


    real_messages = client2.beta.threads.messages.list(thread_id=s_thread_id).data

    messages = []
    for message in real_messages:
        messages.append(message.content[0].text.value)

    socketio.emit('stream_response_replaceable', 
                    {'uuid': data['uuid'], 
                    'cmd_executed': 'list_messages_in_thread',
                    'messages': messages
                    }, 
                    room=sid)



@socketio.on('stream_response')
def handle_stream_response(data):
    
    sid = request.sid  # Obtain the client's session ID
    eventlet.spawn(stream_response, sid, data)


def stream_response(sid, data):

    stream_thread = client2.beta.threads.create()
    thread_id = stream_thread.id

    client2.beta.threads.messages.create(thread_id, content=data['request_text'],role="user")

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




