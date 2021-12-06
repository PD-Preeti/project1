const renderCarouselForm = (() => {
    const carouselForm = document.querySelector('#carouselForm');
    
    const carouselType = carouselForm.querySelector('#carouselType'),
          carouselCourse = carouselForm.querySelector('.carousel-course'),
          carouselLink = carouselForm.querySelector('.carousel-link');

    let carouselTypeVal = '';

    carouselType.addEventListener('click', e => {
        if(e.target.dataset.id == 'input'){
            carouselTypeVal = e.target.value;
            if(carouselTypeVal === 'Other'){
                carouselLink.classList.remove('uk-hidden');
                carouselCourse.classList.add('uk-hidden');
                carouselCourse.querySelector('select').value = '';
                carouselCourse.querySelector('select').required = false;
            }else{
                carouselLink.classList.add('uk-hidden');
                carouselCourse.classList.remove('uk-hidden');
                carouselLink.querySelector('input').value = '';
                carouselCourse.querySelector('select').required = true;
            }
        }
    })
})();


try{
    $(document).ready(function() {
        var carouselData = $('#carouselData').DataTable({
            "bLengthChange": false,
            dom: 'Bfrtip',
        });
    });
}catch(err){}