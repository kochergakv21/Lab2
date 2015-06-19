
self.addEventListener('message', function(e) {
    var row = e.data[0];
    var part = e.data[1];
    var substrings = part.split(row);
    self.postMessage(substrings.length - 1);
}, false);