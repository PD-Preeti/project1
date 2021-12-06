// Assign Form
try{
    // Chosen Select
    const assignTo = document.querySelectorAll('[name="assign_to"]');
    const teamsDiv = document.querySelector('#teams-div');
    const usersDiv = document.querySelector('#users-div');
    const teamSelect = teamsDiv.querySelector('select');
    const userSelect = usersDiv.querySelector('select');

    [...assignTo].map(w => {
        w.addEventListener('click', ()=> {
            if(w.value === 'teams'){
                teamSelect.required = true;
                userSelect.required = false;
                teamsDiv.classList.remove('uk-hidden');
                usersDiv.classList.add('uk-hidden');
                document.getElementById('output').innerHTML = location.search;
                $(".team-select").chosen();
            }else if(w.value === 'users'){
                teamSelect.required = false;
                userSelect.required = true;
                teamsDiv.classList.add('uk-hidden');
                usersDiv.classList.remove('uk-hidden');
                document.getElementById('output2').innerHTML = location.search;
                $(".user-select").chosen();
            }
        })
    })

}catch(err){}

// Corrected Option
try{
const correct = document.querySelector('#correct_opt');
const formOptions = document.querySelectorAll('.form_options');
const correct_opt = correct.options;

[...formOptions].map((fopt, index) => {
    fopt.addEventListener('blur', () => {
        if(fopt.value !== ''){
            correct_opt[index + 1].value = fopt.value;
            correct_opt[index + 1].innerHTML = fopt.value;
        }else{
            correct_opt[index + 1].value = '';
            correct_opt[index + 1].innerHTML = 'Nones';
        }
    });
});

}catch(err){}