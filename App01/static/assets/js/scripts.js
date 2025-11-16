const editorElement = document.getElementById('editor');
const outputElement = document.getElementById('output');
const runCodeButton = document.getElementById('run-code');


// Default code templates for different languages
const templateCode = {
  'C': `#include <stdio.h>
int main() {
    // Write your code here
    return 0;
}`,
  'C++': `#include <iostream>

int main() {
    // Your code here
    return 0;
}`,
  'JAVA': `public class Main {
    public static void main(String[] args) {
        // Your code here
    }
}`,
  'PYTHON': `# Your code here in Python`,
  'JavaScript': `// Your code here in JavaScript`
};

// Set initial code template for C language
editorElement.value = templateCode[lang_name];

// Initialize CodeMirror editor with auto-indentation and other settings
const editor = CodeMirror.fromTextArea(editorElement, {
  mode: languageMode, // Set the language mode (e.g., text/x-csrc, text/x-c++src, etc.)
  lineNumbers: true,
  indentWithTabs: true, // Indent with tabs instead of spaces
  smartIndent: true, // Enable smart indentation
  matchBrackets: true, // Highlight matching brackets
  autoCloseBrackets: true, // Automatically close brackets
  styleActiveLine: true, // Highlight the active line
  lineWrapping: true,
  theme: 'material', // Set the CodeMirror theme
});

// Event listener for running code
runCodeButton.addEventListener('click', () => {
  event.preventDefault();
  const code = editor.getValue();
  const datacode = {
    'code': code,
    'id': document.getElementById('hid').value,
  };

  try {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/my-django-view/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(datacode),
    })
    .then(response => response.text())
    .then(data => {
      console.log('Success:', data);
      outputElement.textContent = data;
      outputElement.style.color = 'green';
    })
    .catch((error) => {
      console.error('Error:', error);
      outputElement.textContent = error;
      outputElement.style.color = 'red';
    });
  } catch (error) {
    outputElement.textContent = 'Error: ' + error.message;
  }
});

// Event listener for submitting code
submitButton.addEventListener("click", function(event) {
  document.getElementById("hidden-editor").value = editor.getValue();
  form.submit();
  // Prevent the default form submission
});
 