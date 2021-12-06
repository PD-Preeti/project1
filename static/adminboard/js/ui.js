// Get Width and height of the browser
let w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
let h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

try{
    const loginSect = document.querySelector('login-sect');
    loginSect.style = `height: ${h}px`;
}catch(err){}

const header = document.querySelector('[data-class = "header"]');
header.style = `width: ${w}; height: 80px`;

// Main App Div
const resp = () => {
    const main = document.querySelector('#app');
    if(w >= 1400){
        main.style = `
            position: fixed;
            top: 80px;
            left: 250px;
            height: calc(100vh - 70px);
            width: ${w - 260}px;`;
    }else if(w > 959){
        main.style = `
            position: fixed;
            top: 80px;
            left: 200px;
            height: 100vh;
            width: ${w - 200}px;`;
    }
}

window.addEventListener('resize', resp());