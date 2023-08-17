const chatRoomUuid = document.querySelector("#room_uuid").textContent.replaceAll('"', '');
var chatWebSocket;

const chatText = document.querySelector("#message_content");
const sendMessageButton = document.querySelector("#send_message");
const messageBox = document.querySelector("#message_box");
const userName = document.querySelector('#user_name').textContent.replaceAll('"', '')
const userId = document.querySelector('#user_id').textContent.replaceAll('"', '')
const typingMessage = document.querySelector("#typing_message");

$(document).ready(function () {
    messageBox.scrollTo(0, messageBox.scrollHeight);
    if (chatRoomUuid){
        chatWebSocket = new WebSocket(`wss://${window.location.host}/ws/${chatRoomUuid}/`)
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

function sendMessage() {
    if (chatWebSocket){
        chatWebSocket.send(JSON.stringify({
            'type': 'message',
            'message': chatText.value,
            'name': userName,
            'agent': userId
        }))

        chatText.value = '';
        messageBox.scrollTo(0, messageBox.scrollHeight);
    }
}

function onNewMessage(data){
    if(data.type == "chat_message" && data.message){
        let tmpInfo = document.querySelector(".tmp-info");
        if (tmpInfo){
            tmpInfo.remove();
        }
        let new_message = '';
        new_message += `
            <div class="flex w-full max-w-md mt-2 space-x-3 ${data.agent ? "ml-auto justify-end mx-5" : ""}">
            `;
        if (!data.agent){
            new_message += `
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-600 text-center text-white mx-3 my-2 pt-2">
                        ${data.initials}
                    </div>`;
        }
        new_message += `
                <div class="my-2">
                    <div class="p-3 rounded-xl ${data.agent ? "bg-gray-500": "bg-gray-300"}">
                        <p class="text-sm">${data.message}</p>
                    </div>
                    <span class="text-xs text-gray-700 leading-none">${data.created_at} ago</span>
                </div>
                `;
        if(data.agent){
            new_message += `
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-600 text-center text-white mx-3 my-2 pt-2">
                        ${data.initials}
                    </div>`;
        }
        new_message +=`
            </div>
        `;
        $("#message_box").append(new_message);
        messageBox.scrollTo(0, messageBox.scrollHeight);
    } else if(data.type == "writing_message"){
        if(!data.agent){
            let tmpInfo = document.querySelector(".tmp-info");
            if (tmpInfo){
                tmpInfo.remove();
            }
        }
        if(!data.agent){
            typingMessage.innerHTML += `
                <div class="tmp-info flex w-full max-w-md mt-3 mx-3 space-x-3">
                    <i class="text-blue-600">${data.message}</i>
                    <img src="/static/images/typing.gif" class="w-12 h-4 mt-1"></img>
                </div>
            `
        }
   }

}

sendMessageButton.addEventListener("click", function(e){
    e.preventDefault();
    sendMessage();
});

chatText.addEventListener("keyup", function(e){
    if (e.keyCode == 13){
        sendMessage();
    }
})

chatText.addEventListener("change", function(e){
    if(chatText.value != "" && chatText != null && chatText != undefined){
        chatWebSocket.send(JSON.stringify({
            'type': 'update',
            'message': `${userName} (admin/agent) is typing`,
            'name': document.querySelector('#user_name').textContent.replaceAll('"', ''),
            'agent': document.querySelector('#user_id').textContent.replaceAll('"', ''), 
        }))
    }else{
        let tmpInfo = document.querySelector(".tmp-info");
        if (tmpInfo){
            tmpInfo.remove();
        }
    }
})