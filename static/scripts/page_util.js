function page_scroll_top() {
    const wrapper = document.getElementsByClassName("wrapper")[0];
    wrapper.scrollIntoView(true);
}

function page_scroll_bottom() {
    const wrapper = document.getElementsByClassName("wrapper")[0];
    wrapper.scrollIntoView(false);
}

function page_scroll_up() {
    let contents = document.getElementsByClassName("frame-contents");
    contents = [...contents].reverse();
    const scroll = document.documentElement.scrollTop;
    for (const content of contents) { 
        const top = content.getBoundingClientRect().top;
        if (Math.ceil(top + scroll) < Math.ceil(scroll)) {
            content.scrollIntoView(true);
            break;
        }
    }
}

function page_scroll_down() {
    const contents = document.getElementsByClassName("frame-contents");
    const scroll = document.documentElement.scrollTop;
    const vp_hegiht = window.innerHeight;
    for (const content of contents) { 
        const bottom = content.getBoundingClientRect().bottom;
        if (Math.ceil(bottom + scroll) > Math.ceil(vp_hegiht + scroll)) {
            content.scrollIntoView(false);
            break;
        }
    }
}