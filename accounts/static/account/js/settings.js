$('.nav.nav-tabs > .nav-item').click(function () {
    let navItem = $(this);
    let navLink = $(navItem.children()[0]);
    let tab = navLink.attr('href');
    let tabContentURL = navLink.attr('data-tab-content-href');
    $(tab).load(tabContentURL);
});

$(document).ready(function () {
    $('#account-tab-md').click();
})