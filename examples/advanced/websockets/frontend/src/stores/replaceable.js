import { writable } from 'svelte/store';
import io from 'socket.io-client';

export const replaceableThread = writable(null);
export const replaceableThreadMessages = writable(null);

export const replaceableChatcompletionContent = writable("")

export const replaceableSocket = io('http://localhost:5000');

let buffer = "";
let updateScheduled = false;



replaceableSocket.on('stream_response_replaceable', (delta) => {
     
    if (delta['cmd_executed'] == "create_replaceable_thread") {
        replaceableThread.update(content => delta['thread_id'])
        replaceableThreadMessages.update(content => null)
    }

    if (delta['cmd_executed'] == "delete_replaceable_thread") {
        replaceableThread.update(content => null)
        replaceableThreadMessages.update(content => null)
    }

    if (delta['cmd_executed'] == "list_messages_in_thread") {
        replaceableThreadMessages.update(content => delta['messages'])
    }

    if (delta['cmd_executed'] == "stream_response") {

        if (delta['instruction'] == "beginStream") {
            buffer = ""
            replaceableChatcompletionContent.update(content => "");
        } 

        if (delta['instruction'] == "endStream") {
            replaceableChatcompletionContent.update(content => content);
        } 

        if (delta['instruction'] == "inStream") {
            buffer += delta['responseText'];
            replaceableChatcompletionContent.update(content => buffer)  
        }



    }


})

