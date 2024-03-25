import { writable } from 'svelte/store';
import io from 'socket.io-client';

export const chatcompletionSocket = io('http://localhost:5000');

export const chatcompletionContent = writable("")




let buffer = "";
let updateScheduled = false;



chatcompletionSocket.on('stream_response', (delta) => {



    if (delta['instruction'] == "beginStream") {
        chatcompletionContent.update(content => "");

    } 
    else {
        if (delta['instruction'] == "endStream") {
            chatcompletionContent.update(content => content + "\n\n");
    
        }
        else {

            if (delta['instruction'] == "inStream") {
                buffer += delta['responseText'];

        
                if (!updateScheduled) {
                    updateScheduled = true;
                    requestAnimationFrame(() => {
                        chatcompletionContent.update(content => content + buffer);
                    buffer = "";
                    updateScheduled = false;
                    });
                }
            }

        }   
    }

})

export default chatcompletionSocket;
