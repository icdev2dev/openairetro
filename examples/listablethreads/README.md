As described earlier, all interactions and observations are through the command line in this example. 

In this example, you can create, delete and **list** threads. This example has nothing to do with using ChatCompletion. Just simply keeping a track of threads created (and deleted). Meaning that you can use this mechanism whether or not you use ChatCompletion or AssistantAPI.


# How
You start out with a blank slate. 

## Step 1 : Listing threads
python core.py --list_threads 1
Observe an empty list

## Step 2: Create one thread
python core.py --create_thread 1
Note the thread_id

## Step 3 : Listing threads
python core.py --list_threads 1
Observe a list with one thread from **step 2** above.

## Step 4: Create one more thread
python core.py --create_thread 1
Note the thread_id


## Step 5 : Listing threads
python core.py --list_threads 1
Observe a list with two threads from **step 2** and **step4** above.

## Step 6 : Delete a thread; picking one of the two threads created.
python core.py --delete_thread 1 --thread_id  <>
Observe the delete of the thread

## Step 7 : Listing threads
python core.py --list_threads 1
Observe a list with the deleted thread no longer on the list.




# Key takeaways
It is possible, using metadata, to keep a track of created threads.