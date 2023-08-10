const chatRoomUuid = document.querySelector("#room_uuid").textContent.replaceAll('"', '');
var chatWebSocket;

const chatText = document.querySelector("#message_content");
const sendMessageButton = document.querySelector("#send_message");
const messageBox = document.querySelector("#message_box");

$(document).ready(function () {
    if (chatRoomUuid){
        chatWebSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)
        chatWebSocket.onopen = function(e){
            console.log("chat socket open");
        }
        chatWebSocket.onclose = function(e){
            console.log("chat socket close");
        }
        if(chatWebSocket){
            chatWebSocket.onmessage = function(e){
                console.log("On message calls");
                onNewMessage(JSON.parse(e.data));
            };
        }
    }
})

function sendMesage(){
    if (chatWebSocket){
        chatWebSocket.send(JSON.stringify({
            "type": "message",
            "name": chatName,
            "message": chatText.value,
            "agent": "",
        }))
        chatText.value = "";
    }
}

function onNewMessage(data){
    if(data.type == "chat_message" && data.message && !data.agent){
        let new_message = '';
        new_message += `
            <div class="flex w-full max-w-md mt-2 space-x-3 ${data.agent ? "ml-auto justify-end" : ""}">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-500 text-center text-white mx-3 my-2 pt-2">
                    ${data.initials}
                </div>
            `
        new_message += `
                <div class="my-2">
                    <div class="p-3 rounded-xl ${data.agent ? "bg-gray-600": "bg-white"}">
                        <p class="text-sm">${data.message}</p>
                    </div>
                    <span class="text-xs text-gray-700 leading-none">${data.created_at} ago</span>
                </div>
            </div>
        `
        $("#message_box").append(new_message);
        messageBox.scrollTo(0, messageBox.scrollHeight);
    }
}