
const editorElement = document.getElementById('editor');
const outputElement = document.getElementById('output');
const runCodeButton = document.getElementById('run-code');

// console.log(editorElement);
// Initialize CodeMirror editor
const editor = CodeMirror.fromTextArea(editorElement, {
  mode: 'text/x-csrc', // or whatever language you want to use
  lineNumbers: true,
  indentWithTabs: true, // Whether to indent with tabs instead of spaces
  smartIndent: true, // Enable smart indentation
  matchBrackets: true, // Highlight matching brackets
  autoCloseBrackets: true, // Automatically close brackets
  styleActiveLine: true, // Highlight the active line
  lineWrapping: true,
});

runCodeButton.addEventListener('click', () => {
  // console.log("hi");
  event.preventDefault();
  const code =  editor.getValue();;
  // console.log(code);
  // console.log(editorElement.value);
  var datacode={
    'code':code
  };

  try {
    // const result = eval(code); // Warning: eval can be dangerous, use with caution.
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/my-django-view/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body:JSON.stringify(datacode),
    })
    .then(response => response.text())
    .then(data => {
        console.log('Success:', data);
        outputElement.textContent = data;
    })
    .catch((error) => {
        console.error('Error:', error);
        outputElement.textContent = error;

    });


  } catch (error) {
    outputElement.textContent = 'Error: ' + error.message;
  }
});

