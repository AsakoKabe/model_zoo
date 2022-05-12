const dropArea = document.getElementsByClassName("drop-area")[0];
const fileInput = document.getElementById("id_input_img");

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});
['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropArea.classList.add('highlight');
}
function unhighlight() {
    dropArea.classList.remove('highlight');
}

fileInput.addEventListener("change", () => {
    if (!fileInput.files || !fileInput.files.length) {
      return
    }
    else {
      const files = fileInput.files;
      const foo = document.getElementById("foo");
      const bar = Array.from(files).map((e) => e.name)
      foo.innerText = bar.toString()
    }
 });

