As described earlier, all interactions and observations are through the command line in this example. 

In this example, you create a SummarizableThead and interact with a predefined Assistant through runs. Then you use the summarize function on the thread to create a summarized snapshot **within** the same thread. This summarized snapshot itself **is a thread**; giving you the opportunity to have all further interactions with the original thread or with the summarized snapshot thread.


```
class MetaClassPythonExpert(BaseAssistant):
    """ You are the world authority on Meta Classes in Python. You can answer any question on Meta Classes in Python; first at the conceptual level and
    then at implementation aka code level. Some questions might require a straight answer; while some questions require some amount of templatized code
    """

```


# How

## A) create a SummarizableThread
python core.py --create_thread 1

Note the thread id


## B) create a conversation on the thread

### B.1)  python core.py --thread_id <> --prompt "what is the general concept behind MetaClasses in Python?" 
 
This creates a run behind the scene and expects to complete by assistant with answer.

### B.2) Verify that the assistant does answer
python core.py --thread_id <> --mesgs 1

### B.3) Continue on the conversation on the same thread
python core.py --thread_id <> --prompt "why are MetaClasses hard to understand?" 

### B.4) Verify that the assistant does answer
python core.py --thread_id <> --mesgs 1

## C) Summarize the conversation on the thread to another thread
python core.py --thread_id <> --summarize 1


## D) Get Latest Summary on original thread
python core.py --thread_id <> --latest_summary 1

## E) Get the thread hosting the latest summary
python core.py --thread_id <> --latest_summary_thread_id 1
Note the thread_id

## F) Continue conversation on summarized_thread
python core.py --thread_id <summarized_thread> --prompt "Can you describe a specific use case in health care?"


## G) See the answer on summarized_thread
python core.py --thread_id <summarized_thread> --mesgs 1

## H) Summarize the summarized thread 
python core.py --thread_id <summarized_thread> --summarize 1

## H) Verify the lastest_summary from the original thread
python core.py --thread_id <> --latest_summary 1




# Key takeaways

It is possible to create set of summarized threads and operate on the summarized threads to reduce token count, potentially.
