// Module Form
const mf = document.querySelector('#moduleForm'),
        ff = mf.querySelector('[data-class="form-fieldset"]'),
        rd = mf.querySelector('.reference-div'),
        addFileField = mf.querySelector('#addFileField'),
        al = mf.querySelector('#addLinks'),
        modName = mf.querySelector('.mod_name');
let fc = 2, fi, linkCount = 0, fieldCount = 1;

// Mod Name Check
modName.addEventListener('change', () => {
    if(moduleNames.includes(modName.value.toLowerCase())){
        modName.nextElementSibling.classList.remove('uk-hidden');
    }else{
        modName.nextElementSibling.classList.add('uk-hidden');
    }
});

mf.addEventListener('submit', (e) => {
    if(btnName === 'submit'){
        if(moduleNames.includes(modName.value)){
            e.preventDefault();
        }else{
            btnName.innerHTML = '<i class="fas fa-circle-notch"></i> Submitting';
            btnName.disabled = true;
        }
    }
})        

// Multiple process
$('.process-select').chosen();
document.getElementById('output-process').innerHTML = location.search;

// Multiple location
$('.location-select').chosen();
document.getElementById('output-location').innerHTML = location.search;

// Add process
const processForm = document.querySelector('#processForm'),
        processList = document.querySelector('#processList');

processForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const processNameNodes = processList.querySelectorAll('.process_name'),
            processNames = [],
            processWarning = processForm.querySelector('.process-warning');
    processNameNodes.forEach(node => processNames.push(node.textContent.toLowerCase()));

    const url = processForm.getAttribute('data-action'),
            inputVal = processForm.querySelector('.process-input').value,
            formData = new FormData(processForm);
    const liItem = `<li class="uk-flex">
                        <span class="uk-flex-1">${inputVal}</span>
                        <a class="uk-delete-icon" style="color: #ccc; cursor: not-allowed;" title="please refresh to delete item" disabled><span uk-icon="icon: trash"></span></a>
                    </li>`;

    if(processNames.includes(inputVal.toLowerCase())){
        return processWarning.classList.remove('uk-hidden');
    }
    
    processWarning.classList.add('uk-hidden');
    
    fetch(url, {
        method: 'POST',
        body: formData
    }).then(res => {
        if(res.status === 200){
            processForm.reset();
            processList.insertAdjacentHTML('beforeend', liItem);
        }
    }).catch(err => console.error(err));
});

// Delete process
const deleteBtns = processList.querySelectorAll('.uk-delete-icon');
deleteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const url = btn.getAttribute('data-href');

        fetch(url)
        .then(res => {
            if(res.status === 200){
                btn.parentElement.remove();
            }
        }).catch(err => console.error(err));
    })
})

// Add links 
al.addEventListener('click', () => addLinksFun());

function addLinksFun(){
    linkCount++;
    if(linkCount <= 10){
        const linkField = `
            <div class="uk-form-controls">
                <input class="uk-input" name="link${linkCount}" type="text" placeholder="Reference Link ${linkCount}">
            </div>
            `;

        rd.insertAdjacentHTML('beforeend', linkField);

        if(linkCount === 10){
            al.classList.add('uk-hidden');
        }
    }
}

// Module File Fields Addition
addFileField.addEventListener('click', () => addFileFieldFun());

function addFileFieldFun(){
    if(fieldCount < 15){
        fieldCount++;
        console.log(fieldCount);
        const getField = document.querySelector(`#file${fieldCount}`);
        if(fieldCount > 2){
            document.querySelector(`.close-btn--${fieldCount - 1}`).classList.add('uk-hidden');
        }
        getField.classList.remove('uk-hidden');
    }
}

function removeFileFieldFun(){
    console.log('hello')
    if(fieldCount > 1){
        document.querySelector(`#file${fieldCount}`).classList.add('uk-hidden');
        fieldCount--;
        document.querySelector(`.close-btn--${fieldCount}`).classList.remove('uk-hidden');
    }
}

// Check for edit module stats
const editModuleFun = () => {
    const moduleName = mf.querySelector('#moduleName'),
            file1 = mf.querySelector('[name="modfile1"]'),
            file2 = mf.querySelector('[name="modfile2"]'),
            videoFile = mf.querySelector('[name="video_file"]'),
            file3 = mf.querySelector('[name="modfile3"]'),
            file4 = mf.querySelector('[name="modfile4"]'),
            file5 = mf.querySelector('[name="modfile5"]'),
            file6 = mf.querySelector('[name="modfile6"]'),
            file7 = mf.querySelector('[name="modfile7"]'),
            file8 = mf.querySelector('[name="modfile8"]'),
            file9 = mf.querySelector('[name="modfile9"]'),
            file10 = mf.querySelector('[name="modfile10"]'),
            file11 = mf.querySelector('[name="modfile11"]'),
            file12 = mf.querySelector('[name="modfile12"]'),
            file13 = mf.querySelector('[name="modfile13"]'),
            file14 = mf.querySelector('[name="modfile14"]');

    moduleName.value = editModule.name;
    // Set process values
    $('.process-select').val(editModule.process);
    $('.process-select').trigger("chosen:updated");

    // Set location values
    $('.location-select').val(editModule.location);
    $('.location-select').trigger("chosen:updated");

    // Links
    links = editModule.links.filter(link => link !== 'None');
    links.map(link => {
        addLinksFun();
        if(linkCount !== 0){
            mf.querySelector(`[name="link${linkCount}"]`).value = link;
        }
    });

    if(editModule.file1 !== ''){
        file1.required = false;
        file1.nextElementSibling.setAttribute('placeholder', editModule.file1);
    }
    if(editModule.file2 !== ''){
        addFileFieldFun();
        file2.nextElementSibling.setAttribute('placeholder', editModule.file2);
    }
    if(editModule.videoFile !== ''){
        addFileFieldFun();
        videoFile.nextElementSibling.setAttribute('placeholder', editModule.videoFile);
    }
    if(editModule.file3 !== ''){
        addFileFieldFun();
        file3.nextElementSibling.setAttribute('placeholder', editModule.file3);
    }
    if(editModule.file4 !== ''){
        addFileFieldFun();
        file4.nextElementSibling.setAttribute('placeholder', editModule.file4);
    }
    if(editModule.file5 !== ''){
        addFileFieldFun();
        file5.nextElementSibling.setAttribute('placeholder', editModule.file5);
    }
    if(editModule.file6 !== ''){
        addFileFieldFun();
        file6.nextElementSibling.setAttribute('placeholder', editModule.file6);
    }
    if(editModule.file7 !== ''){
        addFileFieldFun();
        file7.nextElementSibling.setAttribute('placeholder', editModule.file7);
    }
    if(editModule.file8 !== ''){
        addFileFieldFun();
        file8.nextElementSibling.setAttribute('placeholder', editModule.file8);
    }
    if(editModule.file9 !== ''){
        addFileFieldFun();
        file9.nextElementSibling.setAttribute('placeholder', editModule.file9);
    }
    if(editModule.file10 !== ''){
        addFileFieldFun();
        file10.nextElementSibling.setAttribute('placeholder', editModule.file10);
    }
    if(editModule.file11 !== ''){
        addFileFieldFun();
        file11.nextElementSibling.setAttribute('placeholder', editModule.file11);
    }
    if(editModule.file12 !== ''){
        addFileFieldFun();
        file12.nextElementSibling.setAttribute('placeholder', editModule.file12);
    }
    if(editModule.file13 !== ''){
        addFileFieldFun();
        file13.nextElementSibling.setAttribute('placeholder', editModule.file13);
    }
    if(editModule.file14 !== ''){
        addFileFieldFun();
        file14.nextElementSibling.setAttribute('placeholder', editModule.file14);
    }
}
editModule && editModuleFun();
