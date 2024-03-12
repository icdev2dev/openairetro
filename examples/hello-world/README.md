As described earlier, all interactions and observations are through the command line in this example. 

In this example, you interact with an assistant through publishing messages into a thread. The processing program (looper.py) detects new messages being published by you into the thread and gets chat completion to complete the chat. It then puts the completed response into the thread; so that the context of the conversation is retained. 

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
Launch another terminal . In that terminal, start the looper. 
python looper.py
