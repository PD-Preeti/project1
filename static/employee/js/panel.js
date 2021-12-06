// Timer Countdown
let timer;
let savedDate = localStorage.getItem('savedDate');
let compareDate = new Date();
const monitorTime = document.querySelector('.monitor--time'),
      form = document.querySelector('#finalTest');

if (savedDate)  {
    compareDate = new Date(savedDate);
}
else {
    compareDate.setMinutes(compareDate.getMinutes() + parseInt(testTime)); // Set time here
    localStorage.setItem('savedDate', compareDate);
}

timer = setInterval(function() {
    timeBetweenDates(compareDate);
}, 1000);

function timeBetweenDates(toDate) {
    let dateEntered = toDate;
    let now = new Date();
    let difference = dateEntered.getTime() - now.getTime();
    if (difference <= 0) {
        // Timer done
        clearInterval(timer);
    } else {

        let seconds = Math.floor(difference / 1000);
        let minutes = Math.floor(seconds / 60);
        let hours = Math.floor(minutes / 60);

        hours %= 24;
        minutes %= 60;
        seconds %= 60;

        if(seconds <= 9){
            monitorTime.innerHTML = `${hours}:${minutes}:0${seconds}`;
        }else{
            monitorTime.innerHTML = `${hours}:${minutes}:${seconds}`;
        }

        if(minutes <= 5){
            monitorTime.style.color = 'tomato';
        }

        if(hours === 0 && minutes === 0 && seconds === 0){
            monitorTime.innerHTML = `0:00:00`;
            form.submit();
        }
    }
}
  


// Panel
const panel = document.querySelectorAll('.finalTest__quest');
const nextBtn = document.querySelector('.finalTest__next');
const prevBtn = document.querySelector('.finalTest__prev');
const submitBtn = document.querySelector('.finalTest__submit');

const questCount = document.querySelector('[name="quest_count"]');
questCount.value = panel.length;

const navSwitch = document.querySelectorAll('.switch__a');

let counterPanel = 0;

// Default Trigger
navSwitch[0].style = 'background-color: var(--custom-blue-1); border: 2px solid var(--custom-blue-1); color: var(--custom-white-1);';
panel[0].classList.remove('hidden');

nextBtn.addEventListener('click', e => {
    prevBtn.classList.remove('hidden');

    if(counterPanel < panel.length - 1){
        panel[counterPanel].classList.add('hidden');
        panel[counterPanel + 1].classList.remove('hidden');
        navigator(counterPanel);
        counterPanel++;
        navSwitch[counterPanel].style = 'background-color: var(--custom-blue-1); border: 2px solid var(--custom-blue-1); color: var(--custom-white-1);';
    }

    // When last panel reached change nextBtn type & text to submit
    if(counterPanel === panel.length - 1){
        nextBtn.classList.add('hidden');
        submitBtn.parentElement.classList.remove('hidden');
    }
});

prevBtn.addEventListener('click', e => {
    nextBtn.classList.remove('hidden');
    submitBtn.parentElement.classList.add('hidden');

    if(counterPanel > 0 ){
        panel[counterPanel - 1].classList.remove('hidden');
        panel[counterPanel].classList.add('hidden');
        navigator(counterPanel);
        counterPanel--;
        navSwitch[counterPanel].style = 'background-color: var(--custom-blue-1); border: 2px solid var(--custom-blue-1); color: var(--custom-white-1);';
    }

    // When first panel reached
    if(counterPanel === 0){
        prevBtn.classList.add('hidden');
    }
});


// Navigation
[...navSwitch].map(f => {
    f.addEventListener('click', () => {
        f.style = 'background-color: var(--custom-blue-1); border: 2px solid var(--custom-blue-1); color: var(--custom-white-1);';
        navigator(counterPanel);
        const num = parseInt(f.innerHTML);
        const dataComp = f.getAttribute('data-comp');

        [...panel].map(p => {
            const dataPan = p.getAttribute('data-id');

            if(dataPan === dataComp){
                p.classList.remove('hidden');

                if([...panel].indexOf(p) === 0){
                    prevBtn.classList.add('hidden');
                    nextBtn.classList.remove('hidden');
                    submitBtn.parentElement.classList.add('hidden');
                }else if([...panel].indexOf(p) === panel.length-1){
                    prevBtn.classList.remove('hidden');
                    nextBtn.classList.add('hidden');
                    submitBtn.parentElement.classList.remove('hidden');
                }else{
                    prevBtn.classList.remove('hidden');
                    nextBtn.classList.remove('hidden');
                    submitBtn.parentElement.classList.add('hidden');
                }

                counterPanel = [...panel].indexOf(p);
            }else{
                p.classList.add('hidden');
            }

        });

    });
});

// Play with lights
let navigator = (x) => {
    const opt = panel[x].querySelectorAll('.optBtn');
    const id = panel[x].getAttribute('data-id');
    let state = false;

    [...opt].map((e)=>{
        if(!state){
            if(e.checked) {
                [...navSwitch].map(z => {
                    const comp = z.getAttribute('data-comp');
                    if (id === comp) {
                        z.style = 'background-color: var(--custom-green-1); border: 2px solid var(--custom-green-1); color: var(--custom-white-1);';
                    }
                });
                state = true;
            }else{
                [...navSwitch].map(z => {
                    const comp = z.getAttribute('data-comp');
                    if (id === comp) {
                        z.style = 'background-color: var(--custom-red-1); border: 2px solid var(--custom-red-1); color: var(--custom-white-1);';
                    }
                });
            }
        }

    });
};