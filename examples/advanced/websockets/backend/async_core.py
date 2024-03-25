
import asyncio
import threading
import uuid, random


MAX_TASKS = 3


async def task(number, sleep_time):
    print(f"Task {number} starting with sleep time {sleep_time}")

    with open("cool1.txt", "w+") as FILE:
        FILE.writelines(f"Task {number} starting with sleep time {sleep_time}")
    await asyncio.sleep(sleep_time)
    print(f"Task {number} finished")
    return f"Result from task {number}"



def create_additional_task():
    return asyncio.create_task(task(uuid.uuid4(), random.randint(5,10)))

def create_additional_tasks (n):

    additional_tasks = []

    for _ in range(n):
        additional_tasks.append(create_additional_task())

    return additional_tasks




async def main():

  # Creating tasks that will run concurrently
    
    pending = create_additional_tasks(MAX_TASKS)

    # Wait for tasks to complete with a timeout of 3 seconds
    while True: 
        if len(pending) < MAX_TASKS:
            print(f"NOW ADDING ADDITIONAL   {MAX_TASKS - len(pending)} TASKS ")
            additional_tasks = create_additional_tasks(MAX_TASKS - len(pending))
            pending = list(pending) + additional_tasks
        else:
            done, pending = await asyncio.wait(
                pending,
                timeout=3,
                return_when=asyncio.FIRST_COMPLETED
            )

            for t in done:
                if t.exception():
                    print(f"Task ended with exception: {t.exception()}")
                else:
                    result = await t
                    print(f"Completed task result: {result}")

            for t in pending:
                print(f"Task {t.get_name()} did not complete in time and is still pending.")


def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_async_loop():

    loop = asyncio.new_event_loop()

    t = threading.Thread(target=start_background_loop, args=(loop,))
    t.start()

    asyncio.run_coroutine_threadsafe(main(), loop)

