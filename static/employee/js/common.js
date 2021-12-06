localStorage.clear();

const exploreBtn = document.querySelector('#exploreBtn');
if(exploreBtn){
    exploreBtn.addEventListener('click', (e) => {
        const main = document.querySelector('.main');
        // console.log(e)
        const pos = e.clientY + e.pageY
        scrollToSmoothly(pos, 480);
    });
}

function scrollToSmoothly(pos, time){
    /*Time is exact amount of time the scrolling will take (in milliseconds)*/
    /*Pos is the y-position to scroll to (in pixels)*/
    /*Code written by hev1*/
    if(typeof pos!== "number"){
    pos = parseFloat(pos);
    }
    if(isNaN(pos)){
     console.warn("Position must be a number or a numeric String.");
     throw "Position must be a number";
    }
    if(pos<0||time<0){
    return;
    }
    var currentPos = window.scrollY || window.screenTop;
      var start = null;
    time = time || 500;
    window.requestAnimationFrame(function step(currentTime){
        start = !start? currentTime: start;
      if(currentPos<pos){
      var progress = currentTime - start;
      window.scrollTo(0, ((pos-currentPos)*progress/time)+currentPos);
      if(progress < time){
          window.requestAnimationFrame(step);
      } else {
          window.scrollTo(0, pos);
      }
      } else {
       var progress = currentTime - start;
      window.scrollTo(0, currentPos-((currentPos-pos)*progress/time));
      if(progress < time){
          window.requestAnimationFrame(step);
      } else {
          window.scrollTo(0, pos);
      }
      }
    });
}