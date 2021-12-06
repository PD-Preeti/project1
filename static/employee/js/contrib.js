const tabContrib = document.querySelector('#tab-contrib'),
      yourTab = document.querySelector('#yourTab'),
      makeTab = document.querySelector('#makeTab'),
      gotoMake = document.querySelector('#gotomake'),
      contrib = document.querySelectorAll('.contrib');

tabContrib.addEventListener('click', (e) => {
    const id = e.target.dataset.id;
    if(id){
        tabContrib.querySelectorAll('.tab-list').forEach(item => item.classList.remove('active'));
        tabContrib.querySelector(`[data-id="${id}"]`).classList.add('active');

        document.querySelectorAll('.tab-content').forEach(item => item.classList.add('hidden'));
        document.querySelector(`#${id}Tab`).classList.remove('hidden');
    }
});

try{
    gotoMake.addEventListener('click', () => {
        tabContrib.querySelectorAll('.tab-list').forEach(item => item.classList.remove('active'));
        tabContrib.querySelector(`[data-id="make"]`).classList.add('active');
        yourTab.classList.add('hidden');
        makeTab.classList.remove('hidden');
    });
}catch(err){}

contrib.forEach(cont => {
    const orgHeight = cont.offsetHeight;
    const baseHeight = '100px';
    cont.style.height = baseHeight;

    cont.addEventListener('mouseover', () => cont.style.height = `${orgHeight}px`);
    cont.addEventListener('focusin', () => cont.style.height = `${orgHeight}px`);

    cont.addEventListener('mouseout', () => cont.style.height = baseHeight);
    cont.addEventListener('focusout', () => cont.style.height = baseHeight);
})