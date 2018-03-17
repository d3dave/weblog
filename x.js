(function(){
var records_table = document.querySelector('#records');
var record_template = document.querySelector('#record-template');
var ws = new WebSocket('ws://localhost');
ws.addEventListener('message', function (event) {
    var rec = JSON.parse(event.data);
    var new_row = record_template.cloneNode(true);
    new_row.removeAttribute('id');
    new_row.removeAttribute('style');
    new_row.querySelector('.record-time').textContent = rec.time;
    new_row.querySelector('.record-name').textContent = rec.name;
    new_row.querySelector('.record-level').textContent = rec.level;
    new_row.querySelector('.record-message').textContent = rec.msg;
    new_row.querySelector('.record-thread').textContent = rec.thread;
    new_row.classList.add(rec.level.toLowerCase());
    records_table.appendChild(new_row);
});
})();