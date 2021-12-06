const allModules = document.querySelectorAll('.tab-panel'),
      allReferences = document.querySelectorAll('.references'),
      tabList = document.querySelector('.side-tab__list');

// Script for reference tab movement
try{
    setTimeout(() => {
        function changeReferenceTabs(){
            allModules.forEach(mod => {
                if(mod.classList.contains('uk-active')){
                    if(mod.dataset.id){
                        let reference = document.querySelector(`[data-class = "${mod.dataset.id}"]`);
                        allReferences.forEach(ref => ref.classList.add('uk-hidden'));
                        reference.classList.remove('uk-hidden');
                    }
                }
            })
        }

        changeReferenceTabs();

        tabList.addEventListener('click', (e) => {
            if(e.target.dataset.id){
                setTimeout(() => {
                    changeReferenceTabs();
                }, 300);
            }
        });
    }, 300);
}catch(err){}

// Script to revisit
try{
    const revisitReference = () => {
        const revisitModName = localStorage.getItem('revisit_module'),
              spreadMods = [...allModules],
              tabListItem = tabList.querySelectorAll('li'),
              spreadTabs= [...tabListItem];

        if(revisitModName){
            // Making the tab visible
            spreadMods.map(mod => mod.classList.remove('uk-active'));
            const getMod = spreadMods.filter(mod => mod.dataset.id === revisitModName)[0];
            getMod.classList.add('uk-active');
    
            // Selection reference link
            spreadTabs.map(tab => tab.classList.remove('uk-active'));
            const getTab = spreadTabs.filter(tab => tab.querySelector('a').dataset.id === revisitModName)[0];
            getTab.classList.add('uk-active');        
        }
    }

    setTimeout(() => {
        revisitReference();
    }, 600);
}catch(err){console.log(err)}