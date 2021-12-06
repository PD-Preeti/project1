$(document).ready(function() {
    var peopleTable = $('#contributions').DataTable({
        "bLengthChange": false,
        "pagingType": "input",
        "pageLength": 10,
        stateSave: true,
        stateDuration:-1,
        dom: 'Bfrt<"#datatable_detail_wrapper" ip>',
        buttons: [
            {
                extend: 'csvHtml5',
                text: 'Export CSV',
                exportOptions: {
                    columns: 'th:not(:last-child)'
                }
            }
        ],
    });

    // Filter Position
    const contributionsFilter = document.querySelector('#contributions_filter');
    const dtButtons = document.querySelector('.dt-buttons');
    contributionsFilter.appendChild(dtButtons);
    contributionsFilter.classList.add('uk-flex');
});


// Popup remark section on click
function popupTab(e){
    const grabForm = e.querySelector('form');
    grabForm.classList.add('popupForm');
    grabForm.querySelector('.scorebox').classList.remove('uk-hidden');
    const div = document.createElement('div');
    div.classList.add('popupBack');
    div.style = `
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 999;
    `;
    div.addEventListener('click', (e) => removePopupTab(e));
    document.querySelector('.submission-main').appendChild(div);
}

function removePopupTab(e){
    const grabForm = document.querySelector('.popupForm');
    if(grabForm){
        grabForm.classList.remove('popupForm');
        grabForm.querySelector('.scorebox').classList.add('uk-hidden');
    }
    e.target.remove();
}

// Status Action
try{
    const statusForm = document.querySelectorAll('.statusForm');

    statusForm.forEach(form => {
        form.addEventListener('submit', async(e) => {
            e.preventDefault();

            const action = e.target.dataset.action,
                  remark = form.querySelector('[name="remark"]'),
                  status = form.querySelector('[name="status"]'),
                  score = form.querySelector('[name="score"]');

            const actionBox = e.target.parentElement.nextElementSibling.nextElementSibling;
                actionBox.innerHTML = `<i class="fas fa-circle-notch load-icon"></i>`;

            const statusValue = e.submitter.getAttribute('name');
            status.value = statusValue;
            
            if(e.submitter.getAttribute('name') === 'Rejected'){
                score.value = 0;
            }

            const statusData = new FormData(form);
            
            const response = await fetch(action, {
                method: 'POST',
                body: statusData
            });

            if(response.status === 200){
                const scoreBox = e.target.parentElement.nextElementSibling;

                remark.value !== '' 
                ? form.innerHTML = remark.value
                : form.innerHTML = 'No Remark';
                actionBox.innerHTML = statusValue;
                
                statusValue === 'Accepted' 
                ? scoreBox.innerHTML = score.value
                : scoreBox.innerHTML = 'NA';
            }else{
                actionBox.style = "color: tomato;"
                actionBox.title = `${response.status} - Oops! Something went wrong... Please refresh`
                actionBox.innerHTML = `<i class="fas fa-exclamation-circle"></i> &nbsp; ${response.status} - Oops! Something went wrong`
            }
        })
    })
}catch(err){}