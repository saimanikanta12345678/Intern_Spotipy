document.addEventListener('DOMContentLoaded', function() {
    var current_time = new Date().getHours();
    var greeting = '';

    if (6 <= current_time && current_time < 12) {
        greeting = "Good Morning!";
    } else if (12 <= current_time && current_time < 16) {
        greeting = "Good Afternoon!";
    } else if (16 <= current_time && current_time < 22) {
        greeting = "Good Evening!";
    } else {
        greeting = "Good Night!";
    }

    document.getElementById('greeting').textContent = greeting;
});
