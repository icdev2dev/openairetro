import json
from typing import Dict, List, Optional, Type, TypeVar
from pydantic import Field, BaseModel, model_serializer

from openai_session_handler.models.assistants.baseassistant import BaseAssistant
from openai_session_handler.models.beta import register_composite_fields_and_type

from openai_session_handler.models.threads.basethread import BaseThread

import argparse
T = TypeVar('T', bound='ListableThread')




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



class ListableThreadTracker(BaseAssistant):
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


class ListableThread(BaseThread):
    
    @classmethod
    def create(cls:Type[T], **kwargs) -> T:
        
        if len(ListableThreadTracker.list()) == 0:
            thread_tracker = ListableThreadTracker.create()
        else:
            thread_tracker = ListableThreadTracker.list()[0]     ## assume one threadtraccker
        thread = super().create(**kwargs)
        thread_tracker.add_thread(thread_id=thread.id)
        return thread
            

    @classmethod
    def delete(cls:Type[T], thread_id) :

        if len(ListableThreadTracker.list()) == 0:
            pass
        else:
            thread_tracker = ListableThreadTracker.list()[0]
            thread_tracker.delete_thread(thread_id=thread_id)
        return super().delete(thread_id=thread_id)
    
    @classmethod
    def list(cls:Type[T]): 
        if len(ListableThreadTracker.list()) == 0:
            return []
        else:
            return ListableThreadTracker.list()[0].threads
        


def main(args):
    if args.list_threads != "":
        print(ListableThread.list())
        return

    if args.create_thread != "":
        thread = ListableThread.create()
        print(f"Now created thread : {thread.id}")
        return
    
    if args.delete_thread != "":
        if args.thread_id != "":
            print(f"Now deleting {args.thread_id}")
            ListableThread.delete(thread_id=args.thread_id)
            print(f"Deleted {args.thread_id}")
        else:
            print("you must also specify --thread_id <> to indicate which thread to delete")

        return            

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--list_threads", default="")
    arg_parser.add_argument("--create_thread", default="")
    arg_parser.add_argument("--delete_thread", default="")
    arg_parser.add_argument("--thread_id", default="")
    
    args = arg_parser.parse_args()

    main(args)

    
