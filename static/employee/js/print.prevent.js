
window.addEventListener("keyup", function (e) {
    const keyCode = e.keyCode ? e.keyCode : e.which;
    // console.log(keyCode);

    if (keyCode === 44 || keyCode === 91) {
        e.preventDefault();
    }

    if (keyCode === 44 || keyCode === 91 || keyCode === 9) {
        e.preventDefault();
        stopPrntScr();
    }
});

function stopPrntScr() {
    const inpFld = document.createElement("input");
    inpFld.setAttribute("value", ".");
    inpFld.setAttribute("width", "0");
    inpFld.style.height = "0px";
    inpFld.style.width = "0px";
    inpFld.style.border = "0px";
    document.body.appendChild(inpFld);
    inpFld.select();
    document.execCommand("copy");
    inpFld.remove(inpFld);
}

function AccessClipboardData() {
    try {
        window.clipboardData.setData('text', "Access   Restricted");
    } catch (err) {}
}
setInterval("AccessClipboardData()", 300);
