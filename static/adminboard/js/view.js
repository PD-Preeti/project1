// List and Grid View

const listViewButton = document.querySelector('.list-view-button');
const gridViewButton = document.querySelector('.grid-view-button');
const list = document.querySelector('.list');
const actionDiv = document.querySelectorAll('.action-div');

listViewButton.onclick = function () {
    list.classList.remove('grid-view-filter');
    list.classList.add('list-view-filter');
}

gridViewButton.onclick = function () {
    list.classList.remove('list-view-filter');
    list.classList.add('grid-view-filter');
}

const NUMBER_OF_ITEMS = 15;

let monkeyList = new List('module-box', {
    valueNames: ['module__name', 'module__process', 'module__location'],
    page: NUMBER_OF_ITEMS,
    pagination: {
        left: 2,
        right: 2,
        innerWindow: 2
    },
});

const LIST_SIZE = monkeyList.size()
const PAGE_SIZE = Math.floor(monkeyList.size() / NUMBER_OF_ITEMS)
const STORAGE_KEY = 'MODULE_PAGE_NO'

function pageUpdate(value) {
    if (PAGE_SIZE < 1) return

    window.sessionStorage.setItem(STORAGE_KEY, value)
    value = parseInt(value) - 1;
    idx = value * (NUMBER_OF_ITEMS) + 1;
    monkeyList.i = (idx);
    monkeyList.update();
}

window.addEventListener('load', (event) => {
    if (PAGE_SIZE < 1) {
        return document.querySelector('.page_input').classList.add('uk-invisible', 'pointer-none')
    }

    const getPageNumber = window.sessionStorage.getItem(STORAGE_KEY)
    if( getPageNumber ) {
        document.querySelector('[name="page_number"]').value = getPageNumber;
        pageUpdate(getPageNumber);
    }
});

function updateState (e) {
    if (!e.target.classList.contains('page')) return
    document.querySelector('[name="page_number"]').value = parseInt(e.target.innerText);
    pageUpdate(e.target.innerText)
}

const paginationDiv = document.querySelector('.pagination');
paginationDiv.addEventListener('click', e => updateState(e));