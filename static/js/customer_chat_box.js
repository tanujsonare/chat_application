var chatWebSocket;
const chatRoomUuid = localStorage.getItem("chatroomuuid");
$(document).ready(function () {
    if (chatRoomUuid){
        chatWebSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)
        chatWebSocket.onmessage = function(e){
            console.log("On message calls");
        }
        chatWebSocket.onopen = function(e){
            console.log("chat socket open");
        }
        chatWebSocket.onclose = function(e){
            console.log("chat socket close");
        }
    }
})