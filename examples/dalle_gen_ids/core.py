
from typing import Dict, List, Optional, Type, TypeVar
from pydantic import Field, BaseModel, model_serializer

from openai_session_handler.models.assistants.baseassistant import BaseAssistant
from openai_session_handler.models.beta import register_composite_fields_and_type

from openai_session_handler.models.threads.basethread import BaseThread
from openai_session_handler.models.messages.basemessage import BaseMessage


import hashlib
import argparse
import json

from openai import OpenAI
client = OpenAI()


T = TypeVar('T', bound='ImageThread')


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



class ImageThreadTracker(BaseAssistant):
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


class ImageThread(BaseThread):
    
    @classmethod
    def create(cls:Type[T], **kwargs) -> T:
        
        if len(ImageThreadTracker.list()) == 0:
            thread_tracker = ImageThreadTracker.create()
        else:
            thread_tracker = ImageThreadTracker.list()[0]     ## assume one threadtraccker
        thread = super().create(**kwargs)
        thread_tracker.add_thread(thread_id=thread.id)
        return thread
            

    @classmethod
    def delete(cls:Type[T], thread_id) :

        if len(ImageThreadTracker.list()) == 0:
            pass
        else:
            thread_tracker = ImageThreadTracker.list()[0]
            thread_tracker.delete_thread(thread_id=thread_id)
        return super().delete(thread_id=thread_id)
    
    @classmethod
    def list(cls:Type[T]): 
        if len(ImageThreadTracker.list()) == 0:
            return []
        else:
            return ImageThreadTracker.list()[0].threads
      


class ImageMessage(BaseMessage): 
    prompt:Optional[str] = Field(default="")
    sha256_sum_prompt:Optional[str] = Field(default="")
    image_url:Optional[str] = Field(default="")
    gen_id:Optional[str] = Field(default="")


def insert_gen_id_into_thread(prompt, sha256_sum_prompt, gen_id, image_url):
    image_thread = ImageThread.list()[0].thread_id
    image_thread = str(image_thread)

    msg = ImageMessage.create(thread_id = image_thread,  role="user",  content="", prompt=prompt, sha256_sum_prompt=sha256_sum_prompt, gen_id=gen_id, image_url=image_url  )

  #  print(f"{msg.id}")


def prompt_to_gen_id(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    
    response = client.images.generate(model=model, prompt=prompt, size=size, quality=quality, n=n)

    prompt = prompt.encode(encoding = 'UTF-8', errors = 'strict')

    image_url = response.data[0].url.encode(encoding = 'UTF-8', errors = 'strict')


    m = hashlib.sha256()
    m.update(image_url)
    gen_id = m.hexdigest()

    sha256_sum_prompt = hashlib.sha256()
    sha256_sum_prompt.update(prompt)
    sha256_sum_prompt = sha256_sum_prompt.hexdigest()


    insert_gen_id_into_thread(
                             prompt,
                              sha256_sum_prompt,
                              gen_id,
                              response.data[0].url.encode(encoding = 'UTF-8', errors = 'strict'))
    
     
    return gen_id

def get_sha256_sum_prompt(prompt):
    sha256_sum_prompt = hashlib.sha256()
    sha256_sum_prompt.update(prompt)
    sha256_sum_prompt = sha256_sum_prompt.hexdigest()
    return sha256_sum_prompt


def find_by_prompt(prompt):

    image_thread = ImageThread.list()[0].thread_id
    images = ImageMessage.list(thread_id = image_thread)
    prompt = prompt.encode(encoding = 'UTF-8', errors = 'strict')

    sha256_sum_prompt = get_sha256_sum_prompt(prompt)

    image_urls = []
    for image in images: 
        if image.sha256_sum_prompt == sha256_sum_prompt:
            image_urls.append(image.image_url)
    return image_urls


def find_by_gen_id(gen_id):
    image_thread = ImageThread.list()[0].thread_id
    images = ImageMessage.list(thread_id = image_thread)
 
    image_urls = []
    for image in images: 
        if image.gen_id == gen_id:
            image_urls.append(image.image_url)
    return image_urls


def main(args):

    if args.find_by_gen_id != "":
        image_urls = find_by_gen_id(args.find_by_gen_id)
        for image_url in image_urls: 
            print(image_url)  
        return

    if args.find_by_prompt != "":
        image_urls = find_by_prompt(args.find_by_prompt)
        for image_url in image_urls: 
            print(image_url)  
        return
    if args.list_threads != "":
        print(ImageThread.list())
        return

    if args.add_thread != "":
        thread = ImageThread.create()
        print(thread.id)

        return

    if args.rm_thread != "":
        if args.thread_id != "": 
            ImageThread.delete(thread_id=args.thread_id)
        else: 
            print("you must also specify a thread_id to delete")

        return
        
    if args.prompt != "":
        gen_id = prompt_to_gen_id(args.prompt)
        print (gen_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="")

    parser.add_argument("--list_threads", default="")

    parser.add_argument("--add_thread", default="")
    parser.add_argument("--rm_thread", default="")
    parser.add_argument("--thread_id", default="")
    
    parser.add_argument("--find_by_prompt", default="")
    parser.add_argument("--find_by_gen_id", default="")
    
    args = parser.parse_args()
    main(args)
    




