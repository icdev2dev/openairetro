<script>

    import {replaceableSocket, replaceableThread, replaceableChatcompletionContent} from '../../stores/replaceable'
    import { v4 as uuidv4 } from 'uuid';

    let requestText

    function sendMessage(){
        let uuid = uuidv4()

        replaceableChatcompletionContent.set("")
        
        replaceableSocket.emit("stream_response_replaceable", {
            'uuid': uuid,
            'cmd': 'stream_response',
            'thread_id': $replaceableThread,
            'request_text': requestText, 
            }
        )
    }

</script>


<div>
    <textarea class="long-textbox" bind:value={requestText} ></textarea>
</div>


<div>
    <button on:click={sendMessage}> Click Me</button>
</div>


<div>
    <textarea class="large-textbox" readonly> {$replaceableChatcompletionContent} </textarea>
</div>


<style>
        .long-textbox {
      width: 800px; /* Set the width */
      height: 100px; /* Set the height */
      text-align: left;      /* Align text to the left */
      vertical-align: top;   /* Align text to the top */
    }

    .large-textbox {
      width: 800px; /* Set the width */
      height: 200px; /* Set the height */
      text-align: left;      /* Align text to the left */
      vertical-align: top;   /* Align text to the top */
    }

</style>