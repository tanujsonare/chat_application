let windowUrl = window.location.href;
let chatName = '';
let chatRoomUuid = Math.random().toString(36).slice(2, 12);

const chatElement = document.querySelector("#chat");
const chatOpen = document.querySelector("#chat_open");
const joinChat = document.querySelector("#join_chat");
const chatWelcome = document.querySelector("#chat_welcome");
const chatIcon = document.querySelector("#chat_icon");
const chatNameElement = document.querySelector("#user_name");


// Remove unused elements from localstorage

localStorage.removeItem("chatroomuuid");
localStorage.removeItem("chatName");

// csrf token 

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

chatOpen.onclick = function(e){
    chatIcon.classList.add("hidden");
    chatWelcome.classList.remove('hidden');
    e.stopPropagation();   // Prevent click event from propagating to the body
}

document.addEventListener('click', function(event) {
    if (!chatWelcome.classList.contains("hidden")){
        if (!chatWelcome.contains(event.target)) {
            chatIcon.classList.remove("hidden");
            chatWelcome.classList.add('hidden');
        }
    }
});

async function joinChatRoom (){
    const data = new FormData();
    chatName = chatNameElement.value;
    if(chatName){
        data.append("name", chatName);
    }
    if(windowUrl){
        data.append("url", windowUrl);
    }

    var settings = {
        url: `api/create_room/${chatRoomUuid}/`,
        method: "POST",
        timeout: 2000,
        retryCount: 0,
        retryLimit: 4,
        processData: false,
        mimeType: "multipart/form-data",
        contentType: false,
        dataType: "json",
        headers:{"X-CSRFToken": Cookies.get('csrftoken')},
        data: data,
    };

    await $.ajax(settings).done(function (response) {
        if (response && response.message == "Room created successfully"){
            localStorage.setItem("chatroomuuid", chatRoomUuid);
            localStorage.setItem("chatName", chatNameElement.value);
            window.location.href = "/chat";
        }
    }).fail(function (errorThrown) {
    // is called if request fails or timeout is reached
    settings.retryCount++;
    if (settings.retryCount <= settings.retryLimit && Date.now() - settings.created < settings.retryTimeout) {
        console.log("Retrying");
        $.ajax(settings);
        return;
    }
    });
}

joinChat.addEventListener('click', function(e) {
    e.preventDefault();
    joinChatRoom();
})
