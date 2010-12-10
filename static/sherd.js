if (window.sherdTimeout) {
    cancelTimeout(window.sherdTimeout);
}

var Data = {
    db: {},
    visited: {}
}
var currentPath;
function loadPath(path) {
    if (path == undefined) {
        path = window.location.hash;
    }
}
