document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const subject = document.getElementById('subject').value;
    const experience = document.getElementById('experience').value;
    const address = document.getElementById('address').value;

    if (firstName && lastName && email && phone && subject && experience && address) {
        if (experience < 0) {
            alert('Years of Experience cannot be negative.');
        } else {
            alert('Registration successful!');
            // Here you can add code to handle the form submission, e.g., sending data to a server
        }
    } else {
        alert('Please fill out all fields.');
    }
});

