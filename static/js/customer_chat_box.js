var chatWebSocket;
const chatRoomUuid = localStorage.getItem("chatroomuuid");
const chatName = localStorage.getItem("chatName");
const chatText = document.querySelector("#message_content");
const sendMessageButton = document.querySelector("#send_message");

$(document).ready(function () {
    if (chatRoomUuid){
        chatWebSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)
        chatWebSocket.onopen = function(e){
            console.log("chat socket open");
        }
        chatWebSocket.onclose = function(e){
            console.log("chat socket close");
        }
    }
})

function sendMesage(){
    if (chatWebSocket){
        chatWebSocket.send(JSON.stringify({
            "type": "message",
            "name": chatName,
            "message": chatText.value
        }))
        chatText.value = "";
    }
}

function onNewMessage(data){
    if (data.agent){

    }else{
        
    }
}

sendMessageButton.addEventListener("click", function(e){
    sendMesage();
});

chatWebSocket.onmessage = function(e){
    console.log("On message calls");
    onNewMessage(JSON.parse(e.data));
};