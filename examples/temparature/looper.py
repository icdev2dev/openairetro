import asyncio

from openai import OpenAI
from core import ThreadTracker, ChatCompletionThread, ChatCompletionMessage, ChatCompletionMathTutor

client = OpenAI()

async def main(current_thread):
        
    while True:     
        await asyncio.sleep(2)

        actual_thread  = ChatCompletionThread.retrieve(thread_id=current_thread.thread_id)
        assistant_id = ChatCompletionMathTutor.retrieve(assistant_id=actual_thread.assistant_id)
        

        messages = []
        messages.append({'role': 'system', 'content': assistant_id.instructions})


        if actual_thread.hwm == "":
            last_user_msg_id = ""

            thread_messages = ChatCompletionMessage.list(thread_id = current_thread.thread_id, order='asc')
            for thread_message in thread_messages:
                messages.append({'role': thread_message.actual_role, 'content': thread_message.content[0]['text']['value']})
                if (thread_message.actual_role == "user"):
                    last_user_msg_id = thread_message.id


            if last_user_msg_id != "":
               
                completion = client.chat.completions.create(model=actual_thread.chat_completion_model,
                                                            temperature=float(assistant_id.temparature), 
                                                    messages=messages)
                completion_message = completion.choices[0].message
                print(completion_message)

                ccm = ChatCompletionMessage.create(thread_id = current_thread.thread_id, 
                                      role="user",
                                      actual_role="assistant",
                                      content=completion_message.content
                                      )


                actual_thread.update(hwm=last_user_msg_id)
                
        else:

            last_user_msg_id = ""
            thread_messages = ChatCompletionMessage.list(thread_id = current_thread.thread_id, order='desc')
            thread_message =  thread_messages[0]

            if thread_message.actual_role == "user" and  actual_thread.hwm == thread_message.id :  # This should never happen 
                pass
            elif  thread_message.actual_role == "user" and actual_thread.hwm != thread_message.id :
#                print (f"The hwm{actual_thread.hwm} is different than the user message{thread_message.id}")

                thread_message_id = thread_message.id
                thread_messages = ChatCompletionMessage.list(thread_id = current_thread.thread_id, order='asc')
                for thread_message in thread_messages:
                    messages.append({'role': thread_message.actual_role, 'content': thread_message.content[0]['text']['value']})
                

                
                completion = client.chat.completions.create(model=actual_thread.chat_completion_model,
                                                            temperature=float(assistant_id.temparature), 
                                                    messages=messages)
                completion_message = completion.choices[0].message
                print(completion_message)

                ccm = ChatCompletionMessage.create(thread_id = current_thread.thread_id, 
                                      role="user",
                                      actual_role="assistant",
                                      content=completion_message.content
                                      )


                actual_thread.update(hwm=thread_message_id)

            else:   # Nothing to be done because the assistant has already replied
                pass



def run_main():

    current_thread_tracker = ThreadTracker.list()[0]
    current_thread = current_thread_tracker.threads[0]    # assuming that we will have at least one thread in thread tracker

    asyncio.run(main=main(current_thread))

if __name__ == "__main__":
    run_main()
