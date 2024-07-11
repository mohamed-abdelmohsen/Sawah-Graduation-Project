document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const ratingContainer = document.getElementById("star-rating");

    stars.forEach(star => {
        star.addEventListener("click", function () {
            const ratingValue = parseInt(star.getAttribute("data-rating"));
           
            console.log("تم تقييم بـ " + ratingValue + " نجوم.");
            resetStars();
            markStars(ratingValue);
        });
    });

    function resetStars() {
        stars.forEach(star => {
            star.classList.remove("active");
        });
    }

    function markStars(rating) {
        for (let i = 0; i < rating; i++) {
            stars[i].classList.add("active");
        }
    }
});

