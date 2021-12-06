const assignForm = document.querySelector('#assignCourse');

assignForm.addEventListener('submit',(e) => {
    !proceed && forceAssign(e);
});

const forceAssign = (e) => {
    e.preventDefault();
    const assignWarn = assignForm.querySelector('#assignWarn'),
          assignCourse = assignForm.querySelector('[name="course"]').value,
          assignTo = assignForm.querySelector('[name="assign_to"]:checked').value,
          assignedUsers = assignForm.querySelector('#assignedUsers'),
          assignBtn = assignForm.querySelector('#assignBtn');
    
    let assignCounter = 0, assignedNames = '';

    if(assignTo === 'users'){
        const usersInput = assignForm.querySelector('[name="tags2[]"]');
        if(usersInput){
            const userVal = [...usersInput.options].filter(option => option.selected).map(option => option.value.split(',')[1]);
            if(assignedData.length !== 0){
                assignedData.map((data)  => {
                    if(assignCourse === data.course_name && userVal.includes(data.person_email)){
                        assignCounter++;
                        assignedNames !== '' 
                        ? assignedNames = `${assignedNames}, "${data.person_email.split('@')[0]}"`
                        : assignedNames = `"${data.person_email.split('@')[0]}"`
                    } 
                });

                // Check if course already assigned
                assignCounter > 0
                ? (
                    assignWarn.classList.remove('uk-hidden'),
                    assignBtn.classList.add('uk-hidden'),
                    assignedUsers.textContent = assignedNames
                )
                : assignForm.submit();

            }else{assignForm.submit();}
        }
    }else{assignForm.submit();}
}