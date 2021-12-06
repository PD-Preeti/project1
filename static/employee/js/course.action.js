const enrollForm = document.querySelector('#enrollForm');
if(enrollForm) enrollForm.addEventListener('submit', e => enroll(e));
async function enroll(e){
    e.preventDefault();
    enrollForm.querySelector('button').innerHTML = `<i class="fas fa-circle-notch load-icon"></i>`;
    
    try{
        const url = enrollForm.getAttribute('data-href');
        const enrollFormData = new FormData(enrollForm);
        const submission = await fetch(url, {
            method: 'POST',
            body: enrollFormData
        });

        if(submission.status === 200){
            enrollForm.querySelector('button').classList.remove('btn--primary');
            enrollForm.querySelector('button').classList.add('btn--success');
            enrollForm.querySelector('button').innerHTML = `<i class="fas fa-check mr-2"></i>Enrolled`;

            setTimeout(() => {
                const courseURL = enrollForm.getAttribute('data-course');
                document.querySelector('.enroll-action').innerHTML = `<a href="${courseURL}" class="btn btn--secondary block">Start Course</a>`;
            }, 3000);
        }
    }catch(err){
        enrollForm.querySelector('button').classList.remove('btn--primary');
        enrollForm.querySelector('button').classList.add('btn--danger');
        enrollForm.querySelector('button').innerHTML = `<i class="fas fa-times mr-2"></i> Error`;
    }
    
}

const recommend = document.querySelector('.recommend'),
      popupCancel = document.querySelector('#cancelPopup'),
      popupSect = document.querySelector('#popupSect');

let boolRec = false;

recommend.addEventListener('click', () => {
    if(!boolRec){
        popupSect.classList.remove('hidden');
        boolRec = true;
    }
});

popupCancel.addEventListener('click', () => {
    if(boolRec){
        popupSect.classList.add('hidden');
        boolRec = false;
    }
})


