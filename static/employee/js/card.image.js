const setCourseImage = (e) => {
    const source = e.getAttribute('data-src');
    let count;
    if(!source){
        count = Math.ceil(Math.random() * 4);
        e.src = `/static/employee/images/bg_${count}.svg`;
    }
}

const checkImageExist = (() => {
    const courseCardImageDivs = document.querySelectorAll('.course-cover');
    courseCardImageDivs.forEach(div => {
        if(div.childElementCount === 0){
            const img = document.createElement('img');
            setCourseImage(img);
            div.appendChild(img);
        }
    })
})();