const chatRoomUuid = document.querySelector("#room_uuid").textContent.replaceAll('"', '');
var chatSocket;

const chatText = document.querySelector("#message_content");
const sendMessageButton = document.querySelector("#send_message");
const messageBox = document.querySelector("#message_box");

chatWebSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`);

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
                     <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                 </div>
             </div>
         </div>
         `
    }
 }

if (chatSocket){
    chatSocket.onmessage = function(e){
        onNewMessage(JSON.parse(e.data));
    }
}

chatSocket.onopen = function(e){

}

chatSocket.onclose = function(e){

}