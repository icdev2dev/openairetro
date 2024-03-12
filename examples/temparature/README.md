As described earlier, all interactions and observations are through the command line in this example. 

In this example, you interact with an assistant through publishing messages into a thread. The processing program (looper.py) detects new messages being published by you into the thread and gets chat completion to complete the chat. It then puts the completed response into the thread; so that the context of the conversation is retained. 

The assistant for this example is 

```

class ChatCompletionMathTutor(BaseAssistant):
    """ You are an jovial Math Tutor for a top rated high school in Bangalore, India. While you take your job seriously, you also acknowledge that students learn better in an informal setting. """
    temparature:Optional[str] = Field(default="0.1")

```

Notice the addition of **temparature** in the ChatCompletionMathTutor. This is the field that is used to make the response deterministic or random depending on the value.

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

For example, the first message could be "I want to learn about calculus"

python core.py --content "I want to learn about calculus"

Observe the output of chat completion in looper.py


#### Step B2: Stop the Looper. Remove the original thread. Create a new thread.

Stop the looper. (CRTL^C) 

Remove the original thread
python core.py --rm_thread 1

Create a new thread with the same assistant_id

python core.py --ad_thread 1 --assistant_id <assistant_id>


#### Step B2: Start the Looper
python looper.py

#### Step B4: Repeat the same prompt to observe the approximately same response

python core.py --content "I want to learn about calculus"

Observe the response in looper.py

# Key takeaways

Building on top of hello-world, the assistant here incorporates a **temparature** variable that makes the response as deterministic or random as required. 
