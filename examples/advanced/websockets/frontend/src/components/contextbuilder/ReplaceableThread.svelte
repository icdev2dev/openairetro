<script>
    import { v4 as uuidv4 } from 'uuid';    
    import { replaceableThread, replaceableSocket, replaceableThreadMessages } from "../../stores/replaceable";

    $: rThread  = $replaceableThread
    $: rThreadMessages = $replaceableThreadMessages


    function handleButtonClick() {
     if ($replaceableThread) {
      // Logic to delete the thread

          let uuid = uuidv4()
          replaceableSocket.emit("stream_response_replaceable", {'uuid': uuid, 'cmd': 'delete_replaceable_thread', 'thread_id': $replaceableThread })


     } else {
      // Logic to create the thread
        console.log('Creating thread...');

        let uuid = uuidv4()
        
        replaceableSocket.emit("stream_response_replaceable", {'uuid': uuid, 'cmd': 'create_replaceable_thread' })

    }
  }
</script>


<div>
    <div class="grid">
        <div>
            Thread
        </div>
        <div>
            {rThread}
        </div>
        
        <div> 
            <button on:click={handleButtonClick}> 
                {#if $replaceableThread}
                    Delete Thread
                {:else}
                    Create Thread
                {/if}
            </button>
        </div>
    </div>

    <div> 
        <div>
            Thread's Message Content
        </div>
        <div>
            {rThreadMessages}            
        </div>
        
    </div>
</div>


<style>
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr; /* 20% and 80% */
    gap: 10px;
  }

</style>