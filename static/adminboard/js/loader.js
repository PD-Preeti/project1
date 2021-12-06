function onReady(callback) {
    let intervalID = window.setInterval(checkReady, 2000);

    function checkReady() {
        if (document.getElementsByTagName('body')[0] !== undefined) {
            window.clearInterval(intervalID);
            callback.call(this);
        }
    }
}

function show(id, value) {
    if(value){
        document.getElementById(id).classList.remove('uk-hidden');
    }else{
        document.getElementById(id).classList.add('uk-hidden');
    }
}

onReady(function () {
    show('body', true);
    show('preloader', false);
});
