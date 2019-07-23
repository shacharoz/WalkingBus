function changeBG(elem) {
    let parent = $(elem.parentElement);
    parent.toggleClass('yellow-bg');
    parent.toggleClass('normal-bg');
}
