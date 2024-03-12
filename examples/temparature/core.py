from typing import Dict, Optional, List, Type, TypeVar

import json
from pathlib import Path
import re

from pydantic import BaseModel, Field, model_serializer

from openai_session_handler.models.beta import register_composite_fields_and_type
from openai_session_handler.models.assistants.baseassistant import BaseAssistant


from openai_session_handler.models.threads.basethread import BaseThread
from openai_session_handler.models.messages.basemessage import BaseMessage


import argparse




class Thread(BaseModel): 
    thread_id:str = Field(...)

    @model_serializer
    def compact_ser(self) -> str:
        return json.dumps([self.thread_id])

    @staticmethod
    def compact_deser(string: str) -> Dict :
        list_fields = json.loads(string)
        return {
            'thread_id': list_fields[0]
        }


class ThreadTracker(BaseAssistant):
    threads_1:str = Field(default="")
    threads_2:str = Field(default="")
    threads_3:str = Field(default="")
    threads_4:str = Field(default="")

    register_composite_fields_and_type("threads", ["threads_1", "threads_2", "threads_3", "threads_4" ], Thread)

    @property
    def threads(self) -> List[Thread]:
        return self.get_composite_field('threads')
    
    
    def add_thread(self, thread_id):

        thread_list = self.threads
        thread_instance = Thread(thread_id=thread_id)
        thread_list.append(thread_instance)
        self.save_composite_field('threads', thread_list)

    
    def delete_thread(self, thread_id):
        thread_list = self.threads
        thread_list_updated = []

        for thread in thread_list:
            if thread.thread_id == thread_id:
                pass
            else:
                thread_list_updated.append(thread)

        self.save_composite_field('threads', thread_list_updated)






class ChatCompletionMathTutor(BaseAssistant):
    """ You are an jovial Math Tutor for a top rated high school in Bangalore, India. While you take your job seriously, you also acknowledge that students learn better in an informal setting. """
    temparature:Optional[str] = Field(default="0.1")



class ChatCompletionThread(BaseThread):

    assistant_id:Optional[str] = Field(default="")
    hwm:Optional[str] = Field(default="")

    chat_completion_model:Optional[str] = Field(default="gpt-3.5-turbo")
    


class ChatCompletionMessage(BaseMessage):
    actual_role:Optional[str] = Field(default="")



def main(args):

    if len(ThreadTracker.list()) == 0 :
        thread_tracker = ThreadTracker.create()
        current_thread_tracker = ThreadTracker.list()[0]
    else:
        current_thread_tracker = ThreadTracker.list()[0]


    if args.ls_assistant != "":
        print(ChatCompletionMathTutor.list())
        return
    
    if args.ad_assistant != "":

        assistant = ChatCompletionMathTutor.create()
        print(assistant.id)

        return

    if args.rm_assistant != "":
        assistants = ChatCompletionMathTutor.list()
        for assistant in assistants:
            ChatCompletionMathTutor.delete(assistant_id=assistant.id)
        return
    

    if args.ad_thread != "" and len(current_thread_tracker.threads) == 0:    # only limiting to one thread artificially

        if args.assistant_id == "":
            print("You must also specifcy an assistant id along with add thread")
            return
        else:
            current_thread = ChatCompletionThread.create(assistant_id = args.assistant_id)
            print(f"NOw creating new thread -- >  {current_thread.id}")
                
            current_thread_tracker = ThreadTracker.list()[0]
            current_thread_tracker.add_thread(thread_id=current_thread.id)
            return
    
    if args.ad_thread != "" and len(current_thread.threads) > 0:
        print("one thread already exists in threadtracker. COnsider rm_thread to remove bf adding") 
        return       


    if len(current_thread_tracker.threads) > 0:
        current_thread = current_thread_tracker.threads[0]

        if args.ls_thread != "":
            print(current_thread.thread_id)
            return

        if args.rm_thread != "":
            print(f"Now deleting  {current_thread.thread_id}")
            ChatCompletionThread.delete(thread_id=current_thread.thread_id)

            current_thread_tracker = ThreadTracker.list()[0]
            current_thread_tracker.delete_thread(thread_id=current_thread.thread_id)
            return
        

        if args.content != "":
            print("Now creating message")
            ChatCompletionMessage.create(thread_id = current_thread.thread_id, 
                                      role="user",
                                      actual_role=args.role,
                                      content=args.content
                                      )
            return
        
        if args.ls_msgs != "":
            thread_messages = ChatCompletionMessage.list(thread_id = current_thread.thread_id)
            for thread_message in thread_messages:
                print(thread_message) 
            return


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--content", default="")
    arg_parser.add_argument("--role", default="user")

    arg_parser.add_argument("--ls_thread", default="")
    arg_parser.add_argument("--rm_thread", default="")
    arg_parser.add_argument("--ad_thread", default="")

    arg_parser.add_argument("--ls_assistant", default="")
    arg_parser.add_argument("--rm_assistant", default="")
    arg_parser.add_argument("--ad_assistant", default="")


    arg_parser.add_argument("--assistant_id", default="")


    arg_parser.add_argument("--ls_msgs", default="")


    args = arg_parser.parse_args()

    main(args)



