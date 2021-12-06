const starsTotal = 5;
let ratings = {};

// Run getRatings when dom loads
document.addEventListener('DOMContentLoaded', () => {
    ratingData();
    getRatings();
});

// Mutation Observer
const targetNode = document.querySelector('#courseCardList');
const config = { childList: true, subtree: true };
const callback = function(mutationsList, observer) {
    ratings = {};
    for(const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            ratingData();
        }
    }
    getRatings();
};

const observer = new MutationObserver(callback);
observer.observe(targetNode, config);

// Get ratings
function getRatings(){
    for(let rating in ratings){
        // Get Percentage
        const starPercentage = (ratings[rating] / starsTotal) * 100;

        // Round to nearest 10
        const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

        // set width of stars inner to percentage
        document.querySelector(`[data-id = "${rating}"] .stars-inner`).style.width = starPercentageRounded;
    }
}

function ratingData(){
    const allCourseCard = document.querySelectorAll('.course-card');
    allCourseCard.forEach(card => {
        const cName = card.getAttribute('data-id');
        const cRating = parseFloat(card.getAttribute('data-rating'));
        ratings[`${cName}`] = cRating;
    });
}