document.addEventListener("DOMContentLoaded", function() {
    const guestButton = document.querySelector('#guest');

    guestButton.addEventListener("mouseover", function () {
        window.alert("As a guest you won't be able to use full functionality of our application" +
            " like creating plans, " +
            "recipes nad help in creating best diet possible, " +
            "but you are welcome to try it and decide later.")
        });
})