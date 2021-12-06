// Min-Max Action
try{
    const minMaxForm = document.querySelector('#minMaxForm'),
          alert = document.createElement("div"),
          submissionMain = document.querySelector(".submission-main");

    minMaxForm.addEventListener('submit', async(e) => {
        e.preventDefault();
        const minMaxFormData = new FormData(minMaxForm);
        const url = minMaxForm.dataset.action;

        const minInput = minMaxForm.querySelector("[name='min']");
        const maxInput = minMaxForm.querySelector("[name='max']");
        if(parseInt(minInput.value) <= parseInt(maxInput.value)){
            const response = await fetch(url, {
                method: "POST",
                body: minMaxFormData
            });
    
            if(response.status === 200){
                alert.className = "success-alert";
                alert.innerText = "Min-Max value successfully changed";
    
                submissionMain.append(alert);
    
                setTimeout(() => alert.style = "right: 3rem", 10);
                setTimeout(() => alert.style = "right: -100%", 3010);
                setTimeout(() => alert.remove(), 3020);
            }
        }else{
            alert.className = "danger-alert";
            alert.innerText = "Min value cannot be greater than Max value";
            submissionMain.append(alert);
            
            setTimeout(() => alert.style = "right: 3rem", 10);
            setTimeout(() => alert.style = "right: -100%", 3010);
            setTimeout(() => alert.remove(), 3020);
        }
        
    })
}catch(err){}