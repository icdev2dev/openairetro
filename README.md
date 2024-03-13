# Introduction
I believe that the Assistant API ( https://platform.openai.com/docs/assistants/overview ) from OpenAI provides a decent architectural lens for interacting with the large language models (aka LLMs). Checkout some more of my thoughts here (https://community.openai.com/t/right-semantics-for-assistants-api/564374).


# Motivation
That said, the current (March 2024) implementation of the Assistant API is in Beta. It has several limitations and sometimes just plain does not work. Many people have explored the idea of switching to Chat Completion from Assistant API; with increasing urgency (https://community.openai.com/t/switching-from-assistants-api-to-chat-completion/663018/2). I believe that completely switching would be a step in the wrong direction. This repo explores the possibility of using Chat Completion to complete the conversations within Assistant API; thereby giving a middle path to developers. 

# High Level Mechanics
Specifically , in this paradigm, the assistants, threads and messages are created using the same semantics of the Assistant API. However the completion of the "run" occurs through Chat Completion; thereby seperating the data plane from the execution plane. It is all put together through the betaassi framework (https://github.com/icdev2dev/betaassi); which relies on the metadata exposed at Assistant API Level. Betaassi is in development and therefore all sub-directories here require the installation of betaassi separetely.

# Core Feature

The core feature exposed through the betaassi is the ability to extend different classes. 

For example, an ordinary thread (https://platform.openai.com/docs/api-reference/threads/object) has the following structure: 

```
{
  "id": "thread_abc123",
  "object": "thread",
  "created_at": 1698107661,
  "metadata": {}
}
```


By declaring a Chat Completion class like so : 
```
class ChatCompletionThread(BaseThread):

    assistant_id:Optional[str] = Field(default="")
    hwm:Optional[str] = Field(default="")

    chat_completion_model:Optional[str] = Field(default="gpt-3.5-turbo")
```

provides additional attributes for assistant_id, hwm (high water mark) and chat_completion_model in a ChatCompletionThread.

Similarly assistant class as well as message class can be subclassed. 

# Use Cases

The examples directories provide a "learn by example" methodology for the betaassi framework. Most examples are command-line driven. This section provides the high level view of the examples. The detailed README.md within each example exposes more details in context of the example.

## hello-world
This is a simple example intending to show how the basic chat completion works in conjunction with the assistant api.

## temparature 
This example, which builds on top of the hello-world example, to include temparature as a actionable field on the Assistant structure. This means that you can set the temparature in such a manner to make the response as deterministic or random as required. 

## listablethreads
This example has NOTHING to do with chat-completion. Instead it is a powerful demo of what can be accomplished through metadata. As of March 2024, there is no native programmatic way of listing threads that have been created. Here ,using metadata,  one can keep a track of threads that have been created (and removed from list when deleted)



# Pre-requisites

You must, currently, git clone the betaassi repository from here ((https://github.com/icdev2dev/betaassi) at the same level as this repository. Then in the virtual environment for execuction of openairetro, you must pip install -e ../betaassi

YOu must also export the OPENAI_API_KEY into your environment.
