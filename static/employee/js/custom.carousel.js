console.log("carousel open");
$(document).ready(function () {
  let heroCarousel = $(".custom-carousel");
  heroCarousel.owlCarousel({
    items: 1,
    dotsEach: true,
    lazyLoad: true,
    margin: 0,
    responsiveClass: true,
    dots: true,
    loop: true,
    autoplay: true,
    autoplayTimeout: 8000,
  });
});
