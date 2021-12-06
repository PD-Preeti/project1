// Collapsable Menu
function toggleNav(e) {
    if(e.getAttribute('data-toggle') === 'false'){
        openNav();
        e.setAttribute('data-toggle', 'true');
        document.querySelector('#courseApp').classList.add('has-sidebar')
        document.querySelector('.sidebar-list-item.active').scrollIntoView();
    }else{
        closeNav();
        e.setAttribute('data-toggle', 'false');
        document.querySelector('#courseApp').classList.remove('has-sidebar')
    }
}

function openNav() {
    document.querySelector(".sidebar").style.width = "25%";
    document.querySelector(".app-data").style.marginLeft = "25%";

    const resources = document.querySelector(".resources");
    const questSect = document.querySelector(".quest-section");

    resources && (resources.style = "max-width: calc(var(--custom-width-max) - 25%);");
    questSect && (questSect.style = "max-width: calc(var(--custom-width-max) - 25%);");
}

function closeNav() {
    document.querySelector(".sidebar").style.width = "0";
    document.querySelector(".app-data").style.marginLeft= "0";

    const resources = document.querySelector(".resources");
    const questSect = document.querySelector(".quest-section");

    resources && (resources.style = "max-width: var(--custom-width-max);");
    questSect && (questSect.style = "max-width: var(--custom-width-max);");
}

// Get current Date and time
function getCurrentDate() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const date = new Date();

    let hours = date.getHours(),
          minutes = date.getMinutes(),
          ampm = hours >= 12 ? 'p.m.' : 'a.m.';
    hours = hours % 12 === 0 ? 12 : hours % 12;
    minutes = minutes < 10 ? `0${minutes}` : minutes;

    const str = `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}, ${hours}:${minutes} ${ampm}`
    return str;
}

// Full Screen
function toggleScreen(e) {
    document.querySelector('#content').requestFullscreen();
}

// Toggle Between Q&A and Resource tab
function toggleTab(e) {
    const id = e.dataset.id;
    const extraListItems = document.querySelectorAll('.extra-list-item');
    const allTabs = document.querySelectorAll('.tab-item');
    if(id) {
        extraListItems.forEach(item => item.classList.remove('active'));
        e.classList.add('active');

        allTabs.forEach(tab => tab.classList.add('hidden'));
        document.querySelector(`#${id}`).classList.remove('hidden');
    }
}

// Rendering
const VIDEO_FILE_TYPES = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'];
const AUDIO_FILE_TYPES = ['mp3', 'wav', 'm4a', 'm4b'];
const DOCUMENT_FILE_TYPES = ['pdf'];
const IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif'];

function renderSidebar() {
    const sideBarList = document.querySelector('#sidebarList');
    Object.values(courseData).map((data, idx) => {
        const li = `
            <li 
                class="sidebar-list-item" 
                data-id="${data.module_name}" 
                title="${data.module_name}"
                onclick="renderContent('${data.module_name}')"
            >
                <input type="checkbox" ${data.completed && "checked"} readonly tab-index="-1" />
                <span>${idx + 1}. ${data.module_name}</span>
            </li>
        `;

        sideBarList.innerHTML += li;
    });

    if (courseCompleted && !testStatus) {
        const li = `
            <li 
                class="sidebar-list-item active" 
                data-id="last-sidebar-item" 
                title="Course Completed"
                onclick="renderFinal('completed')"
            >
                <span class="icon"><i class="fas fa-check-double"></i></span>
                <span>Course Completed</span>
            </li>
        `;

        sideBarList.innerHTML += li;
    }else if(courseCompleted && testStatus) {
        const li = `
            <li 
                class="sidebar-list-item active" 
                data-id="last-sidebar-item" 
                title="Final round"
                onclick="renderFinal('finalquest')"
            >
                <span class="icon"><i class="fas fa-clipboard"></i></span>
                <span>${courseData.length + 1}. Final Round</span>
            </li>
        `;

        sideBarList.innerHTML += li;
    }
}

class Renderer {
    constructor(moduleName) {
        this.moduleName = moduleName;
        this.PAGE_COUNT = 0;
        this.value = Object.values(courseData).filter((value) => value.module_name === this.moduleName)[0];
        this.contentDiv = document.querySelector('#content');
        this.navigatorDiv = document.querySelector('#navigatorDiv');
        this.questTab = document.querySelector('#quest');
        this.resourceTab = document.querySelector('#resource');
        
        this.contentChild = null;
        this.nextBtn = null;
        this.prevBtn = null;
        this.scenarios = null;
        this.questionForm = null;
        
        this.nextBtn = document.querySelector('#next');
        this.prevBtn = document.querySelector('#prev');
    }

    initalize() {
        this.contentDiv.innerHTML = '';
        this.navigatorDiv.innerHTML = '';
        this.resourceTab.innerHTML = '';
        this.questTab.innerHTML = '';
        this.createElements();
        this.eventListeners();
    }

    createElements() {
        // Module Files
        if(this.value.module_files.length !== 0){
            this.value.module_files.map((file, idx) => {
                if(VIDEO_FILE_TYPES.includes(file.type.toLowerCase())){
                    const videoElem = `
                        <div class="content-child video media hidden" data-type="video">
                            <video class="module_media" controls controlsList="nodownload" oncontextmenu="return false;" data-type="video" width="100%" style="min-height: calc(100vh - 400px);" nodownload>
                                <source src="${file.url}" type="video/mp4">
                            </video>
                        </div>
                    `;
                    
                    this.contentDiv.innerHTML += videoElem;

                }else if(DOCUMENT_FILE_TYPES.includes(file.type.toLowerCase())){
                    const id = `slide_${idx}`;
                    const pdfElem = `
                        <div class="content-child document slide hidden" data-type="pdf" id="${id}" data-url="${file.url}">
                            <p class="text-lg font-medium slide-loader">Loading...</p>
                        </div>
                    `;
                    this.contentDiv.innerHTML += pdfElem;
                    renderPDF(id);
                }
            });
        }

        // Scenarios
        if(this.value.module_scenarios.length !== 0){
            this.value.module_scenarios.map((scenario, idx) => {
                const scenarioElem = `
                    <div class="content-child scenario hidden">
                        <h3 class="text-2xl font-semibold text-gray-700 mb-4">Scenario ${idx + 1}.</h3>
                        <p class="mb-4 text-lg font-medium">${scenario.description}</p>
                    
                        <form class="scenarios w-full" method="post" data-id="${idx}" data-assoc="${this.value.module_name}">
                            ${scenario.csrf_token}
                            <div class="hidden">
                                <input type="number" name="sId" value="${scenario.id}"/>
                                <input type="text" name="cname" value="${this.value.course_name}"/>
                                <input type="text" name="mname" value="${this.value.module_name}"/>
                            </div>
                    
                            ${
                                Object.keys(scenario.file).length !== 0
                                ? (
                                    `<div class="mb-4">
                                        ${
                                            VIDEO_FILE_TYPES.includes(scenario.file.type.toLowerCase())
                                            ? (
                                                `<video class="media scenario_video" controls controlsList="nodownload" oncontextmenu="return false;" data-type="video" width="100%" style="min-height: calc(100vh - 400px);" nodownload>
                                                    <source src="${scenario.file.url}" type="video/mp4">
                                                </video>`
                                            ) : ""
                                        }

                                        ${
                                            AUDIO_FILE_TYPES.includes(scenario.file.type.toLowerCase())
                                            ? (
                                                `<audio class="media scenario_audio" controls controlsList="nodownload" oncontextmenu="return false;" data-type="audio">
                                                    <source src="${scenario.file.url}" type="audio/mpeg">
                                                </audio>`
                                            ) : ""
                                        }

                                        ${
                                            IMAGE_FILE_TYPES.includes(scenario.file.type.toLowerCase())
                                            ? (
                                                `<img class="media scenario_image" src="${scenario.file.url}" alt="img" width="300px" height="300px">`
                                            ) : ""
                                        }
                                    </div>`
                                ) : ""
                            }
                    
                            <ul class="options w-full mb-4 ${Object.keys(scenario.answered).length !== 0 ? 'options-off' : ''}">
                                ${
                                    scenario.option1 !== ''
                                    ? (
                                        `<li class="options-item">
                                            <label class="radio">
                                                <input 
                                                    type="radio" 
                                                    name="sOpt" 
                                                    class="sOpt optBtn" 
                                                    value="${scenario.option1}" 
                                                    required 
                                                    ${Object.keys(scenario.answered).length !== 0 
                                                        ? (
                                                            (scenario.answered.value == scenario.option1) ? 'checked disabled' : 'disabled')
                                                        : ''
                                                    }
                                                />
                                                <span class="label"></span>${scenario.option1}
                                            </label>
                                        </li>`
                                    ) : ""
                                }
                                ${
                                    scenario.option2 !== ''
                                    ? (
                                        `<li class="options-item">
                                            <label class="radio">
                                                <input 
                                                    type="radio" 
                                                    name="sOpt" 
                                                    class="sOpt optBtn" 
                                                    value="${scenario.option2}" 
                                                    required
                                                    ${Object.keys(scenario.answered).length !== 0 
                                                        ? (
                                                            (scenario.answered.value == scenario.option2) ? 'checked disabled' : 'disabled')
                                                        : ''
                                                    }
                                                />
                                                <span class="label"></span>${scenario.option2}
                                            </label>
                                        </li>`
                                    ) : ""
                                }
                                ${
                                    scenario.option3 !== ''
                                    ? (
                                        `<li class="options-item">
                                            <label class="radio">
                                                <input 
                                                    type="radio" 
                                                    name="sOpt" 
                                                    class="sOpt optBtn" 
                                                    value="${scenario.option3}" 
                                                    required
                                                    ${Object.keys(scenario.answered).length !== 0 
                                                        ? (
                                                            (scenario.answered.value == scenario.option3) ? 'checked disabled' : 'disabled')
                                                        : ''
                                                    }
                                                />
                                                <span class="label"></span>${scenario.option3}
                                            </label>
                                        </li>`
                                    ) : ""
                                }
                                ${
                                    scenario.option4 !== ''
                                    ? (
                                        `<li class="options-item">
                                            <label class="radio">
                                                <input 
                                                    type="radio" 
                                                    name="sOpt" 
                                                    class="sOpt optBtn" 
                                                    value="${scenario.option4}" 
                                                    required
                                                    ${Object.keys(scenario.answered).length !== 0 
                                                        ? (
                                                            (scenario.answered.value == scenario.option4) ? 'checked disabled' : 'disabled')
                                                        : ''
                                                    }
                                                />
                                                <span class="label"></span>${scenario.option4}
                                            </label>
                                        </li>`
                                    ) : ""
                                }
                            </ul>

                            ${Object.keys(scenario.answered).length === 0
                                ? (
                                    `<button type="submit" class="btn--primary my-8 rounded-lg h-12 px-8 flex items-center justify-center text-white hover:text-white">Confirm Answer</button>`
                                ) : ""
                            }
                        </form>

                        ${Object.keys(scenario.answered).length !== 0
                            ? (
                                `<div class="alert my-6 ${scenario.answered.status ? 'alert-success' : 'alert-danger'}">
                                    <section class="alert-item">
                                        <h4 class="alert-item-title">Correct Answer</h4>
                                        <p>${scenario.correctoption}</p>
                                    </section>
                                    <section class="alert-item">
                                        <h4 class="alert-item-title">Reason</h4>
                                        <p>${scenario.reason}</p>
                                    </section>
                                </div>`
                            ) : ""
                        }
                    </div>
                `;

                this.contentDiv.innerHTML += scenarioElem;
            })
        }

        // Confidence Rating
        if(this.value.confidence_url !== ''){
            const confidenceElem = `
                <div class="content-child document grid place-items-center hidden">
                    <form action="${this.value.confidence_url}" method="post" class="w-full" id="confidence_${this.value.module_name}">
                        ${this.value.csrf_token}
                        <h3 class="text-2xl font-semibold mb-4 text-gray-700">Before moving forward,<br>Rate your confidence on this topic.</h3>
                        <div>
                            <div class="inputGroup high__inp mb-6">
                                <label for="high__${this.value.module_name}" class="block rounded-lg btn--success p-4 w-2/3">
                                    <input id="high__${this.value.module_name}" name="confidence_meter__${this.value.module_name}" type="radio" value="High"  ${this.value.confidence === 'High' ? 'checked' : ''} required/>
                                <span>High</span>
                                </label>
                            </div>
                            <div class="inputGroup med__inp mb-6">
                                <label for="medium__${this.value.module_name}" class="block rounded-lg btn--primary p-4 w-2/3">
                                    <input id="medium__${this.value.module_name}" name="confidence_meter__${this.value.module_name}" type="radio" value="Medium" ${this.value.confidence === 'Medium' ? 'checked' : ''} />
                                    <span>Medium</span>
                                </label>
                            </div>
                            <div class="inputGroup low__inp">
                                <label for="low__${this.value.module_name}" class="block rounded-lg btn--danger p-4 w-2/3">
                                    <input id="low__${this.value.module_name}" name="confidence_meter__${this.value.module_name}" type="radio" value="Low" ${this.value.confidence === 'Low' ? 'checked' : ''} />
                                    <span>Low</span>
                                </label>
                            </div>
                        </div>
                
                        <button type="submit" class="btn--primary mt-12 rounded-lg h-12 px-8 flex items-center justify-center text-white hover:text-white">Submit</button>
                    </form>
                </div>
            `;

            this.contentDiv.innerHTML += confidenceElem;
        }

        // Resources
        if(this.value.module_links.length !== 0 ){
            const resourceElem = `
                <ul class="resources">
                    ${this.value.module_links.map((link, idx) => (
                        `<li class="resources-item"><a href="${link}" target="_blank" rel="noopener noreferrer">Resource ${idx + 1}: <span class="text-blue-600 truncate">${link}</span></a></li>`
                    ))}
                </ul>
            `;

            this.resourceTab.innerHTML += resourceElem;
        }else {
            const resourceElem = `
                <ul class="resources">
                    <li class="resources-item resources-item--not"><a>No resources found</a></li>
                </ul>
            `;

            this.resourceTab.innerHTML += resourceElem;
        }

        // FAQ
        if(this.value.questURL !== ''){
            const questElem = `
                <div class="quest-section">
                    <form action="" method="POST" class="quest-form" id="questForm">
                        ${this.value.csrf_token && this.value.csrf_token}
                        <input type="text" class="hidden" name="module_name" value="${this.value.module_name}"/>
                        <input type="text" class="quest-input" name="question" placeholder="Have any doubts?" autocomplete="off" required />
                        <button type="submit" class="quest-button bg-blue-500 hover:bg-blue-600 text-white">Ask Question?</button> 
                    </form>

                    <div class="mt-12" id="allQuestions">
                        <div class="flex items-center justify-between mb-6">
                            <h3 class="text-xl font-semibold">All Questions in this module</h3>
                            <div class="input-div">
                                <i class="fas fa-search mr-4"></i>
                                <input type="text" name="" id="" class="search search-input" placeholder="search user asked questions">
                            </div>
                        </div>

                        <ul class="quest-list list">
                        ${(this.value.questions.length !== 0 )
                            ? this.value.questions.map((question, idx) => (
                                `<li class="quest-list-item">
                                    <section class="flex flex-col gap-y-2">
                                        <h4 class="text-lg font-medium question">${question.question}</h4>
                                        <p class="quest-list-item-detail text-gray-600 truncate">
                                            ${question.answer !== 'None' ? question.answer.replaceAll('<br />', '') : '<em>Not answered yet</em>'}
                                        </p>
                                        ${question.answer !== 'None'
                                            ? (`<a class="block mt-2 cursor-pointer text-blue-700" onclick="toggleText(this, ${this.value.id}, ${idx})" data-toggle="false">Read More</a>`)
                                            : ''
                                        }
                                    </section>

                                    <section class="text-sm flex items-center gap-x-4 text-gray-600 mt-6">
                                        <p class="flex items-center gap-x-1">
                                            <i class="far fa-user"></i>
                                            <span class="person_name">${question.person_name}</span>
                                            <span class="hidden person_email">${question.person_email}</span>
                                        </p>
                                        <p class="flex items-center gap-x-1">
                                            <i class="far fa-clock"></i>
                                            <span>${question.created_date}</span>
                                        </p>
                                        <p class="flex items-center gap-x-1">
                                            <i class="far fa-dot-circle"></i>
                                            <span>${question.status}</span>
                                        </p>
                                    </section>
                                </li>`
                            )) : ""
                        }
                        </ul>
                        <ul class="pagination flex items-center justify-start mt-16"></ul>
                    </div>
                </div>
            `;

            this.questTab.innerHTML += questElem;
            setTimeout(() => this.useList(), 50);
        }

        // Get Question Form
        this.questionForm = document.querySelector('#questForm');

        // Add Buttons
        this.nextBtn = document.createElement('button');
        this.nextBtn.setAttribute('type', 'button');
        this.nextBtn.classList.add('navigatorbtn', 'next');
        this.nextBtn.innerHTML = '<span>Next</span><i class="fas fa-chevron-right"></i>';

        this.prevBtn = document.createElement('button');
        this.prevBtn.setAttribute('type', 'button');
        this.prevBtn.classList.add('navigatorbtn', 'prev');
        this.prevBtn.innerHTML = '<i class="fas fa-chevron-left"></i><span>Prev</span>';

        this.navigatorDiv.appendChild(this.prevBtn);
        this.navigatorDiv.appendChild(this.nextBtn);

        this.contentChild = document.querySelectorAll('.content-child');
        if(this.contentChild.length !== 0){
            this.contentChild[0].classList.remove('hidden');
        }

        if (this.PAGE_COUNT === 0) {
            this.prevBtn.classList.add('invisible', 'pointer-events-none');
            this.nextBtn.classList.remove('invisible', 'pointer-events-none');
        }
    }

    eventListeners() {
        // Next, Prev navigator
        this.nextBtn.addEventListener('click', () => this.next());
        this.prevBtn.addEventListener('click', () => this.prev());

        // Scenario submission
        this.scenarios = document.querySelectorAll('.scenarios');
        if(this.scenarios.length !== 0) {
            this.scenarios.forEach(scenario => {
                scenario.addEventListener('submit', async(e) => {
                    e.preventDefault();

                    const selectedOption = scenario.querySelector('[name="sOpt"]:checked');
                    const id = parseInt(e.target.getAttribute('data-id'));

                    const module = Object.values(courseData).find((value) => value.module_name === e.target.getAttribute('data-assoc'));

                    const moduleScenario = module.module_scenarios[id];

                    const scenario_form_data = new FormData(scenario);
                    const URL = '/postscenario/';

                    const formResponse = await fetch(URL, {
                        method: 'POST',
                        body: scenario_form_data
                    });

                    if(formResponse.status === 200){
                        e.target.querySelector('button[type="submit"]').remove();

                        const answered = {
                            status: moduleScenario.correctoption === selectedOption.value,
                            value: selectedOption.value
                        };
                        Object.assign(moduleScenario.answered, answered);

                        const alertClass = answered.status ? 'alert-success' : 'alert-danger';

                        const alert = document.createElement('div');
                        alert.classList.add('alert', 'my-6', alertClass)
                        alert.innerHTML = `
                            <section class="alert-item">
                                <h4 class="alert-item-title">Correct Answer</h4>
                                <p>${moduleScenario.correctoption}</p>
                            </section>
                            <section class="alert-item">
                                <h4 class="alert-item-title">Reason</h4>
                                <p>${moduleScenario.reason}</p>
                            </section>
                        `;

                        e.target.parentElement.appendChild(alert);

                        const optionUl = document.querySelector('.options');
                        optionUl.classList.add('options-off');

                        const allOptions = optionUl.querySelectorAll('.options-item');
                        allOptions.forEach(item => item.querySelector('input').disabled = true)
                    }
                });
            })
        }

        // Question Submission
        this.questionForm.addEventListener('submit', async(e) => {
            e.preventDefault();
            const questFormData = new FormData(this.questionForm);
            const questionInput = e.target.querySelector('[name="question"]');
            const questList = document.querySelector('.quest-list');
            const URL = this.value.questURL;

            try{
                if (questionInput !== '') {
                    const formResponse = await fetch(URL, {
                        method: 'POST',
                        body: questFormData
                    });
        
                    if(formResponse.status === 200) {
                        const toast = document.createElement('div');
                        toast.classList.add('fixed', 'bottom-4', 'right-4', 'px-4', 'py-2', 'rounded-lg', 'bg-green-200', 'text-green-700');
                        toast.innerText = "Your question posted successfully";
                        document.body.appendChild(toast);

                        // Add item to list
                        const li = document.createElement('li');
                        li.innerHTML = `<li class="quest-list-item">
                            <section class="flex flex-col gap-y-2">
                                <h4 class="text-lg font-medium question">${sanitize(questionInput.value)}</h4>
                                <p class="quest-list-item-detail text-gray-600 truncate">
                                    <em>Not answered yet</em>
                                </p>
                            </section>

                            <section class="text-sm flex items-center gap-x-4 text-blue-700 mt-6">
                                <p class="flex items-center gap-x-1">
                                    <i class="far fa-user"></i>
                                    <span class="person_name">${userData.name}</span>
                                    <span class="hidden person_email">${userData.email}</span>
                                </p>
                                <p class="flex items-center gap-x-1">
                                    <i class="far fa-clock"></i>
                                    <span>${getCurrentDate()}</span>
                                </p>
                                <p class="flex items-center gap-x-1">
                                    <i class="far fa-dot-circle"></i>
                                    <span>Pending</span>
                                </p>
                            </section>
                        </li>`;

                        this.value.questions.unshift({
                            question: (`${sanitize(questionInput.value)}`).replace(/\n\r?/g, '<br />'),
                            answer: 'None',
                            person_name: `${userData.name}`,
                            person_email: `${userData.email}`,
                            created_date: `${getCurrentDate()}`,
                            status: "Pending"
                        })

                        questList.insertBefore(li, questList.firstChild);
                        questionInput.value = '';
                        setTimeout(() => toast.remove(), 3000);
                    }
                }
            }catch(err) {
                questionInput.value = '';
                const toast = document.createElement('div');
                toast.classList.add('fixed', 'bottom-4', 'right-4', 'px-4', 'py-2', 'rounded-lg', 'bg-red-200', 'text-red-700');
                toast.innerText = "Failed to post your question. Try again!";
                document.body.appendChild(toast);

                setTimeout(() => toast.remove(), 3000);
            }
        });
    }
  
    next() {
        if(this.PAGE_COUNT < (this.contentChild.length - 1)) {
            this.contentChild[this.PAGE_COUNT].classList.add('hidden');
            this.contentChild[this.PAGE_COUNT + 1].classList.remove('hidden');

            if(this.prevBtn.classList.contains('invisible')) {
                this.prevBtn.classList.remove('invisible', 'pointer-events-none');
            }

            this.PAGE_COUNT++;
        }
        
        if(this.PAGE_COUNT >= (this.contentChild.length - 1)) {
            this.nextBtn.classList.add('invisible', 'pointer-events-none');
        }

        this.pauseMedia();
    }

    prev() {
        if(this.PAGE_COUNT > 0) {
            this.contentChild[this.PAGE_COUNT].classList.add('hidden');
            this.contentChild[this.PAGE_COUNT - 1].classList.remove('hidden');
            this.PAGE_COUNT--;

            if(this.nextBtn.classList.contains('invisible')) {
                this.nextBtn.classList.remove('invisible', 'pointer-events-none');
            }
        }

        if(this.PAGE_COUNT === 0) {
            this.prevBtn.classList.add('invisible', 'pointer-events-none');
        }

        this.pauseMedia();
    }

    pauseMedia() {
        const getAllMedia = document.querySelectorAll('.media');
        getAllMedia.forEach(media => {
            if(media.dataset.type === 'video'){
                return media.querySelector('video').pause();
            }else if(media.dataset.type === 'audio'){
                return media.querySelector('audio').pause();
            }
        })
    }

    useList() {
        let monkeyList = new List('allQuestions', {
            valueNames: ['question', 'person_email', 'person_name'],
            page: 10,
            pagination: true
        });
    }

}

function toggleText(e, moduleId, questionIDX) {
    const detail = e.previousElementSibling;
    const module = Object.values(courseData).find(value => value.id === moduleId);
    let answer = module.questions[questionIDX].answer;

    if(e.dataset.toggle === 'false'){
        detail.innerHTML = answer;
        detail.classList.remove('truncate');
        e.dataset.toggle = 'true';
        e.innerText = 'Read Less';
    }else {
        answer = answer.replaceAll('<br />', '');
        detail.innerHTML = answer;
        detail.classList.add('truncate');
        e.dataset.toggle = 'false';
        e.innerText = 'Read More';
    }
}

function renderContent(moduleName) {
    hideUnhide(false);

    const renderer = new Renderer(moduleName);
    renderer.initalize();

    toggleActive(moduleName);
}

function renderFinal(type) {
    hideUnhide(true);
    toggleActive('last-sidebar-item');

    const finalDiv = document.querySelector('#finalDiv');
    finalDiv.innerHTML = '';
    let elem = '';

    if(type === 'finalquest') {
        elem = `
            <div>
                <img src="${completionIMG}" alt="graphic" class="completion-graphic" />

                <div class="flex flex-col gap-y-1 mt-4 items-center">
                    ${testgiven_status !== 'True' ? (
                        `<p class="text-2xl font-semibold">Good Job, Coming so far...</p>
                        <p class="text-lg font-medium">Now its time for <span class="text-blue-800">Final Round</span></p>
                        <a href="${finalURL}" class="mt-4 px-4 bg-blue-600 text-white font-medium flex items-center justify-center h-12 w-40 rounded-lg">Start Test</a>`
                    ): (
                        `<p class="text-2xl font-semibold">Hurray!! 🎉🎉</p>
                        <p class="text-lg font-medium">You have completed the course.</p>`
                    )}
                </div>
            </div>
        `;
    }else if(type === 'completed') {
        elem = `
            <div>
                <img src="${completionIMG}" alt="graphic" class="completion-graphic" />

                <div class="flex flex-col gap-y-1 mt-4 items-center">
                    <p class="text-2xl font-semibold">Hurray!! 🎉🎉</p>
                    <p class="text-lg font-medium">You have completed the course.</p>

                    ${!ratingFlag 
                        ? (
                        `<a href="${rateURL}" class="mt-4 px-4 bg-blue-600 text-white font-medium flex items-center justify-center h-12 w-40 rounded-lg">Rate the course</a>`
                        ) : ''
                    }
                </div>
            </div>
        `;
    }

    finalDiv.innerHTML += elem;
}

function hideUnhide(hide) {
    const container = document.querySelector('.main-container'),
        extra = document.querySelector('#extra'),
        finalDiv= document.querySelector('#finalDiv');
    if(hide) {
        container.classList.add('hidden');
        extra.classList.add('hidden');
        finalDiv.classList.remove('hidden');
    }else {
        container.classList.remove('hidden');
        extra.classList.remove('hidden');
        finalDiv.classList.add('hidden');
    }
}

function toggleActive(name) {
    const navListItems = document.querySelectorAll('.sidebar-list-item');
    navListItems.forEach(item => item.classList.contains('active') && item.classList.remove('active'));
    document.querySelector(`[data-id="${name}"]`).classList.add('active');
}

function completedModule() {
    if(!courseCompleted){
        const module = Object.values(courseData).find((value) => value.completed === false);
        renderContent(module.module_name);
    }else{
        courseCompleted && !testStatus ? renderFinal('completed') : renderFinal('finalquest');
    }
}

renderSidebar()
completedModule();