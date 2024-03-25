<script>
    import { socketStore } from '../stores/socketStore.js';

    import { v4 as uuidv4 } from 'uuid';

    let socket;
    
    socketStore.subscribe(value => {
      socket = value;
    });


    $: if (socket) {

        socket.on('stream_response', (data) => {
            receivedText = data['responseText']; // Use dataKey to dynamically access the data
        });
    }


    let requestText
    let receivedText;

    function sendMessage() {
        let uuid = uuidv4()
        receivedText = ""
        socket.emit("stream_response", {'uuid': uuid, 'request_text': requestText, 'assistant_id': 'cool'})
    }




</script>

<div>
    <textarea class="large-textbox" bind:value={requestText} ></textarea>
</div>



<div>
    <button on:click={sendMessage}> Click Me</button>

</div>


<div>
    <textarea class="large-textbox" bind:value={receivedText} ></textarea>
</div>

<style>


    .large-textbox {
      width: 500px; /* Set the width */
      height: 300px; /* Set the height */
      text-align: left;      /* Align text to the left */
      vertical-align: top;   /* Align text to the top */
    }

</style>