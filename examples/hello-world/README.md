As described earlier, all interactions and observations are through the command line in this example. 

In this example, you interact with an assistant through publishing messages into a thread. The processing program (looper.py) detects new messages being published by you into the thread and gets chat completion to complete the chat. It then puts the completed response into the thread; so that the context of the conversation is retained. 

The assistant for this example is 

```
class ChatCompletionPhysicsTutor(BaseAssistant):
    """ You are an acclaimed Physics Tutor for a top rated high school in the Bay Area of California, USA. """
    pass 

```

# How
You start out with a blank slate. 

## A) Initial Setup

### Step A0
python core.py --ls_assistant 1 
python core.py --ls_thread 1 

### Step A1 : Create a assistant
python core.py --ad_assistant 1 
python core.py --ls_assistant 1 

### Step A2 : Create a thread associating the previous assistant with the thread
python core.py --ad_thread 1 --assistant_id <assistant_id>
python core.py --ls_thread 1

## B) Chat Completion Loop

### Step B0: Start the looper
The looper detects a new user message to which it attempts to complete using the chat completion api. 

Launch another terminal . In that terminal, start the looper. 
python looper.py

### Step B1: Create user message/s
Use the core.py to publish "user" message into the thread.

#### Step B1.a

For example, the first message could be "How did the universe begin?"

python core.py --content "How did the universe begin?"

Observe the output of chat completion in looper.py

#### Step B1.b
The second message should be terse; because the context of first question and the chat completion as the answer is already in the thread. It could be as simple as "what models?"

python core.py --content "what models?"
Observe the output of chat completion in looper.py to be consistent with the initial context of "how did the universe begin"

#### Step B1.c 
The third messag should also be terse; because the context of first and second questions and answers are already in the thread. It could be "what experiments?"

python core.py --content "what experiments?"
Observe the output of chat completion in looper.py to be consistent with the context.


# Key takeaways

## All data is self-contained within the relevant structures of Assistant API.
No need for any additional database

## ThreadTracker
The ThreadTracker is an assistant that can keep track of multiple threads. In this example, we are only using the first thread in the first ThreadTracker instance. 

## ChatCompletionThread 
```
class ChatCompletionThread(BaseThread):

    assistant_id:Optional[str] = Field(default="")
    hwm:Optional[str] = Field(default="")

    chat_completion_model:Optional[str] = Field(default="gpt-3.5-turbo")

```
Apart from the usual thread attributes, the ChatCompletionThread incorporates the following attributes.

**assistant_id** The assistant_id is used to identify the assistant to be used with this thread.

**hwm** The high water mark (hwm) represents the last user_message that the thread has processed.

**chat_completion_model** is self explanatory

## Doing away with the Run

The looper is async polling for any new message in the ChatCompletionThread. In this example, there is no need for a separate run; because the thread has all the necessary information (in particular, the assistant) to enable Chat Completion.



