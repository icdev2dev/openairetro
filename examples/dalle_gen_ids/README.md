As described earlier, all interactions and observations are through the command line in this example. 

This example is a PURE storage example. That is how can you use threads and messages for storage and retrieval. The use case is that calling the dall-e-3 interface with a prompt generates an image. We use thread and messages to store the prompt, the url associated with the generation of the image and the gen_id associated with the url. Given a gen_id, we can retrieve the URL associated with the image.



# How
You start out with a blank slate. 

## Step 1 : Listing threads
python core.py --list_threads 1
Observe an empty list

## Step 2: Add one thread
python core.py --add_thread 1
Note the thread_id

## Step 3 : Listing threads
python core.py --list_threads 1
Observe a list with one thread from **step 2** above.

## Step 4: Generate an image 
python core.py --prompt "a pink siamese cat"
note the id

## Step 5: Find url by ID
python core.py --find_by_gen_id <id>
Note the URL and then copy the url into the browser to observe the generated image



# Key takeaways
It is possible to use threads and messages in a pure storage fashion; morphing the meaning of threads and messages.