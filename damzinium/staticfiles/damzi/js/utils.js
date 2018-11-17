// hide network status when user has internet connection
window.addEventListener("online", function () {
    const networkStatus = document.querySelector(".network-status");
    networkStatus.classList.remove("visible");
    networkStatus.classList.add("hidden");
});
// show network status when user has lost internet connection
window.addEventListener("offline", function () {
    const networkStatus = document.querySelector(".network-status");
    networkStatus.classList.remove("hidden");
    networkStatus.classList.add("visible");
});