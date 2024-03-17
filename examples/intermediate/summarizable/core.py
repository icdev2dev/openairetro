import json
from typing import Dict, List, Optional, Type, TypeVar
from pydantic import Field, BaseModel, model_serializer

from openai_session_handler.models.assistants.baseassistant import BaseAssistant
from openai_session_handler.models.beta import register_composite_fields_and_type

from openai_session_handler.models.client import client

from openai_session_handler.models.threads.basethread import BaseThread


import argparse
T = TypeVar('T', bound='SummarizableThread')


class MetaClassPythonExpert(BaseAssistant):
    """ You are the world authority on Meta Classes in Python. You can answer any question on Meta Classes in Python; first at the conceptual level and
    then at implementation aka code level. Some questions might require a straight answer; while some questions require some amount of templatized code
    """
    

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


class SummarizedThread(BaseThread):
    parent_thread_id:Optional[str] = Field(default="")

    @classmethod
    def create(cls:Type[T], **kwargs) -> T:
        sum_text = kwargs.pop('sum_text')

        sum_thread =  super().create(**kwargs)
        client.beta.threads.messages.create(thread_id=sum_thread.id, content=sum_text, role="user")

        return sum_thread
    

    def get_summarized_text(self):
        thread_messages = client.beta.threads.messages.list(self.id)
        return thread_messages.data[0].content[0].text.value
    


    def summarize(self):
        summarizable_thread = SummarizableThread.retrieve(self.parent_thread_id)
        summarizable_thread.summarize(parent=True, child_thread_id=self.id)




class SummarizableThread(BaseThread):

    summarized_threads_1:str = Field(default="")
    summarized_threads_2:str = Field(default="")
    summarized_threads_3:str = Field(default="")
    summarized_threads_4:str = Field(default="")

    register_composite_fields_and_type("summarized_threads", ["summarized_threads_1", "summarized_threads_2", "summarized_threads_3", "summarized_threads_4" ], Thread)

    @property
    def summarized_threads(self) -> List[Thread]:
        return self.get_composite_field('summarized_threads')
    

    @classmethod
    def create(cls:Type[T], **kwargs) -> T:
        thread = super().create(**kwargs)

        thread_list = []
        thread_instance = Thread(thread_id=thread.id)
        thread_list.append(thread_instance)


        thread.save_composite_field('summarized_threads', thread_list)

        return thread


    @classmethod
    def delete(cls:Type[T], thread_id) :

        thread = cls.retrieve(thread_id=thread_id)

        summarized_threads_list = thread.summarized_threads

        if summarized_threads_list[-1].thread_id == thread_id:
            summarized_threads_list = summarized_threads_list[:-1]

        for summarized_thread in summarized_threads_list:
            SummarizedThread.delete(thread_id=summarized_thread.thread_id)

        return super().delete(thread_id=thread_id)


    def retrieve_lastest_summarized_thread_id(self):
        temp_thread = self.__class__.retrieve(thread_id=self.id)

        return temp_thread.summarized_threads[0].thread_id
    
    def get_latest_summary(self):
        latest_summarized_thread_id = self.retrieve_lastest_summarized_thread_id()
        thread_messages = client.beta.threads.messages.list(thread_id=latest_summarized_thread_id, order="desc")
        latest_summary = thread_messages.data[0].content[0].text.value
        
        return latest_summary
    

    def summarize(self, parent=False, child_thread_id=""):

        sum_text = "Can you please summarize the conversation so far so that anyone can follow the jist and can continue forward just based on the summary? "

        messages= []

        if parent:
            thread_messages = client.beta.threads.messages.list(thread_id=child_thread_id, order="asc")
        else:
            thread_messages = client.beta.threads.messages.list(thread_id=self.id, order="asc")

        assistant_id = None
        for thread_message in thread_messages:
            if thread_message.assistant_id == None:
                pass
            else: 
                assistant_id = thread_message.assistant_id

        if assistant_id != None:
            assistant = MetaClassPythonExpert.retrieve(assistant_id=assistant_id)
            messages.append({'role': 'system', 'content': assistant.instructions})

        print(messages)

        for thread_message in thread_messages:
            messages.append({'role': thread_message.role, 'content': thread_message.content[0].text.value})

#        print(messages)

        messages.append({'role': "user", 'content': sum_text})


        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

        print(sum_text)
        sum_text = completion.choices[0].message.content

        print(sum_text)


        summarized_thread = SummarizedThread.create(parent_thread_id=self.id, sum_text=sum_text)

        thread_list = self.summarized_threads
        thread_instance = Thread(thread_id=summarized_thread.id)
        thread_list = [thread_instance] + thread_list

        self.save_composite_field('summarized_threads', thread_list)
        return sum_text
    

def main(args):

    if args.create_thread != "":
        summarizable_thread = SummarizableThread.create()
        print (summarizable_thread.id)
        return
    
    if args.delete_thread != "":
        if args.thread_id != "":
            SummarizableThread.delete(thread_id=args.thread_id)
        else:
            print(f"YOu must specify --thread_id along with --delete_thread")
        return
    

    if args.mesgs != "":
      if args.thread_id != "":
        
        thread_messages = client.beta.threads.messages.list(thread_id=args.thread_id, order="asc")

        for thread_message in thread_messages:
            print(thread_message.content[0].text.value)
      else:
        print("you must also specify --thread_id along --mesgs")
    
      return


    if args.prompt != "":
        if args.thread_id != "":

            thread_id = args.thread_id

            list_assistants = MetaClassPythonExpert.list()
            assistant_id = ""
            if len(list_assistants) == 0 : 
                assistant = MetaClassPythonExpert.create(    model = "gpt-4-1106-preview")

                assistant_id =  assistant.id
            else: 
                assistant_id = list_assistants[0].id

            client.beta.threads.messages.create(thread_id=thread_id, role="user", content=args.prompt)

            run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
            print(run)
        
        else:
            print(f"YOu must specify --thread_id along with --prompt")

        return
    

    if args.summarize != "":
        if args.thread_id != "":
            base_thread = BaseThread.retrieve(thread_id=args.thread_id)
            sum_text = ""

            if base_thread.thread_type == "SummarizableThread":
                summarizable_thread = SummarizableThread.retrieve(thread_id=args.thread_id)
                sum_text = summarizable_thread.summarize()
            elif base_thread.thread_type == "SummarizedThread":
                summarized_thread = SummarizedThread.retrieve(thread_id=args.thread_id)
                sum_text = summarized_thread.summarize()

            print(f"summarized as --> {sum_text}")

        else:
            print("you must specify --thread_id along with --summarize")
    
        return
    

    
    if args.latest_summary_thread_id != "":
        if args.thread_id != "":
            summarizable_thread = SummarizableThread.retrieve(thread_id=args.thread_id)
            print(summarizable_thread.summarized_threads[0])
        else:
            print("you must also specify thread_id with --latest_summary_thread_id")

    if args.latest_summary != "":
        if args.thread_id != "":
            summarizable_thread = SummarizableThread.retrieve(thread_id=args.thread_id)
            latest_summary = summarizable_thread.get_latest_summary()
            print(latest_summary)
        else:
            print("you must specify --thread_id along with --latest_summary")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--create_thread", default="")
    parser.add_argument("--delete_thread", default="")
    
    parser.add_argument("--prompt", default="")
    parser.add_argument("--mesgs", default="")
    parser.add_argument("--summarize", default="")
    parser.add_argument("--latest_summary", default="")
    parser.add_argument("--latest_summary_thread_id", default="")


    parser.add_argument("--thread_id", default="")

    args = parser.parse_args()

    main(args)

