const mainContainer = document.querySelector(".main-section");

for (let i = 0; i < 35; i++) {
    const blocks = document.createElement('div');
    blocks.classList.add('main-section__bg-block')
    mainContainer.appendChild(blocks);
}

let elements = document.querySelectorAll('.main-section__bg-block');

function animateMainBgBlocks() {
    anime({
        targets: elements,
        translateX: function () {
            return anime.random(-700, 700)
        },
        translateY: function () {
            return anime.random(-400, 400)
        },
        scale: function () {
            return anime.random(1, 5)
        },
        easing: "easeInQuad",
        duration: 3000,
        delay: 0,
        complete: animateMainBgBlocks,
    });
}

animateMainBgBlocks();


let timeTableRow = document.querySelectorAll(".timetable__dates__events-list__element");


timeTableRow.forEach(function (button) {
    button.querySelector('.timetable__dates__events-list__element__open-more').onclick = () => {
        $(button.querySelector('.timetable__dates__events-list__element__more-text')).slideToggle();
    }
})

// slideToggle