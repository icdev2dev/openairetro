<script>

    import {chatcompletionContent, chatcompletionSocket} from "../stores/oneshotstreamingchatcompletion"

    import { selectedAssistant } from "../stores/selectedAssistant";
    import {selectedModel} from "../stores/selectedModel"

    import { v4 as uuidv4 } from 'uuid';
 


    let requestText
    let receivedText;


    function sendMessage() {
        let uuid = uuidv4()
        receivedText = ""
        
        chatcompletionContent.update(content => content + "YOU : " + requestText +  "\n\n");
        chatcompletionSocket.emit("stream_response", {'uuid': uuid, 'request_text': requestText, 'assistant_id': $selectedAssistant, 'model': $selectedModel})

        chatcompletionContent.update(content => content + "ASSISTANT :"+ "  \n\n");
    }

</script>


<div>
    <textarea class="long-textbox" bind:value={requestText} ></textarea>
</div>


<div>
    <button on:click={sendMessage}> Click Me</button>
</div>


<div>
    <textarea class="large-textbox" readonly>{$chatcompletionContent}</textarea>
</div>

<style>


    .long-textbox {
      width: 1000px; /* Set the width */
      height: 100px; /* Set the height */
      text-align: left;      /* Align text to the left */
      vertical-align: top;   /* Align text to the top */
    }

    .large-textbox {
      width: 1000px; /* Set the width */
      height: 200px; /* Set the height */
      text-align: left;      /* Align text to the left */
      vertical-align: top;   /* Align text to the top */
    }


</style>