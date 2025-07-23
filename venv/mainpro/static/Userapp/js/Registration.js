// Registration.js
// Simple client-side validation
document.getElementById('regForm').onsubmit = function (e) {
    var errorMsg = "";
    var fname = document.getElementById('fname').value.trim();
    var sname = document.getElementById('sname').value.trim();
    var email = document.getElementById('email').value.trim();
    var pho = document.getElementById('pho').value.trim();
    var addr = document.getElementById('addr').value.trim();
    var uname = document.getElementById('uname').value.trim();
    var pswd = document.getElementById('pswd').value;

    if (fname.length < 3 || !/^[A-Za-z\s]+$/.test(fname)) {
        errorMsg = "Please enter a valid first name (letters only, min 3 chars).";

    } else if (sname.length < 3 || !/^[A-Za-z\s]+$/.test(sname)) {
        errorMsg = "Please enter a valid last name (letters only, min 3 chars).";

    } else if (!email.match(/^[^@]+@[^@]+\.[^@]+$/)) {
        errorMsg = "Please enter a valid email address.";

    } else if (!pho.match(/^\+?[0-9]{10,15}$/)) {
        errorMsg = "Please enter a valid phone number (10-15 digits, optional leading +).";

    } else if (addr.length < 5) {
        errorMsg = "Please enter a valid address (min 5 chars).";

    } else if (uname.length < 4 || !/^[A-Za-z0-9_]+$/.test(uname)) {
        errorMsg = "Username must be at least 4 characters and contain only letters, numbers, or underscores.";

    } else if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(pswd)) {
        errorMsg = "Password must be 8+ chars with 1 uppercase, 1 lowercase, 1 number, and 1 special character";
    }

    if (errorMsg) {
        document.getElementById('formError').innerText = errorMsg;
        document.getElementById('formError').style.display = 'block';
        e.preventDefault();
        return false;
    }
    document.getElementById('formError').style.display = 'none';
    return true;
}

function closeMessage() {
    const popup = document.getElementById('message-popup');
    if (popup) {
        popup.style.display = 'none';
    }
}

window.onload = function() {
    const popup = document.getElementById('message-popup');
    if (popup) {
        setTimeout(() => {
            popup.style.display = 'none';
        }, 5000);

        const successMsg = popup.querySelector('.success');
        if (successMsg) {
            setTimeout(() => {
                window.location.href = homeUrl;  // use the global variable
            }, 2000);
        }
    }
};
