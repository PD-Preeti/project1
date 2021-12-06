$(document).ready(function() {
    var peopleTable = $('#people').DataTable({
        "bLengthChange": false,
        "pagingType": "input",
        "pageLength": 10,
        stateDuration:-1,
        stateSave: true,
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
        initComplete: function () {
            const th = document.querySelectorAll('#people > thead > tr > th');
            this.api().columns([3, 4, 5, 6, 7]).every( function (i) {
                var column = this;
                let titleHead = [...th][i].innerHTML;
                var label = $('<label class="uk-form-label">'+ titleHead +'<br></label>')
                    .appendTo( $('#filters') );
                var select = $('<select class="uk-select"><option value="">--select--</option></select>')
                    .appendTo( $(label))
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
    
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
    
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        },

    });

    // Filter Position
    const peopleFilter = document.querySelector('#people_filter');
    const dtButtons = document.querySelector('.dt-buttons');
    peopleFilter.appendChild(dtButtons);
    peopleFilter.classList.add('uk-flex');
});

try{
    $('.date_range_filter').daterangepicker();
    
    const dateForm = document.querySelector('#dateRange');
    const applyBtn = document.querySelector('.applyBtn');
    
    applyBtn.addEventListener('click', (e) => {
        setTimeout(() => {dateForm.submit();}, 500)
    });
}catch(err){}

// Extend Form Submission
try{
    const extendForms = document.querySelectorAll('.extend-form');
    
    extendForms.forEach(extendForm => {
        extendForm.addEventListener('submit', async(e) => {
            e.preventDefault();
    
            const actionURL = e.target.dataset.action,
                  getInput = e.target.querySelector('.expired-input'),
                  getName = getInput.getAttribute('name'),
                  extendData = new FormData(extendForm);
            
            const response = await fetch(actionURL, {
                method: 'POST',
                body: extendData
            })
    
            if(response.status === 200){
                const expirationDateField = document.querySelector(`#${getName}`);
                expirationDateField.innerHTML = moment(getInput.value).format('ll');
                expirationDateField.style = 'color: #2eb582; transition: all .3s ease;'
    
                setTimeout(() => {
                    expirationDateField.style = 'color: #666'
                }, 4000)
            }
        });
    });
}catch(err){console.log(err)}

// Retest
try{
    const testRestartBtns = document.querySelectorAll('.test-restart');

    testRestartBtns.forEach(restartBtn => {
        restartBtn.addEventListener('click', async(e) => {
            const getURL = e.target.dataset.href;
            const response = await fetch(getURL);
            
            if(response.status === 200){
                restartBtn.parentElement.parentElement.querySelector('.test-reset > i').style = `
                    animation: spin 2s forwards ease;
                    transition: all .3s ease;
                `
            }
        })
    })
}catch(err){console.log(err)}

// Revoke user
try{
    const revokeBtns = document.querySelectorAll('.revoke');

    revokeBtns.forEach(revokeBtn => {
        revokeBtn.addEventListener('click', async(e) => {
            const getURL = e.target.dataset.href;
            const response = await fetch(getURL);

            if(response.status === 200){
                e.target.parentElement.parentElement.parentElement.remove();
            }
        });
    })

}catch(err){console.log(err)}