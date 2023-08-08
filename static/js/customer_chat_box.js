var chatWebSocket;
const chatRoomUuid = localStorage.getItem("chatroomuuid");
const chatName = localStorage.getItem("chatName");
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
   if(data.type == "chat_message" && data.message){
        messageBox.innerHTML += `
        <div class="col-start-1 col-end-8 p-3 rounded-lg">
            <div class="flex flex-row items-center">
                <div
                    class="flex items-center justify-center h-10 w-10 rounded-full bg-indigo-500 flex-shrink-0">
                    ${data.initials}
                </div>
                <div class="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl">
                    <div>
                        ${data.message}
                    </div>
                </div>
            </div>
        </div>
        `
   }
}

sendMessageButton.addEventListener("click", function(e){
    sendMesage();
});