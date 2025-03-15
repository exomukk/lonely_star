// Handle login/logout button
function toggleLoginLogout() {
    const loginButton = document.getElementById('loginBtn');
    const logoutButton = document.getElementById('logoutBtn');
    
    if (loginButton.style.display === 'none') {
        loginButton.style.display = 'block';
        logoutButton.style.display = 'none';
    } else {
        loginButton.style.display = 'none';
        logoutButton.style.display = 'block';
    }
}

// Play button action
document.getElementById('playBtn').addEventListener('click', function() {
    window.location.href = 'game.html';
});

// Option button action
document.getElementById('optionBtn').addEventListener('click', function() {
    alert('Options will be here!');
});

const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let waveHeight = 20;
let waveSpeed = 0.1;
let offset = 0;

function drawWave() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);

    // Tạo sóng động
    for (let x = 0; x < canvas.width; x++) {
        let y = Math.sin((x + offset) * 0.05) * waveHeight + canvas.height / 2;
        ctx.lineTo(x, y);
    }

    ctx.lineTo(canvas.width, canvas.height);
    ctx.closePath();

    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.fill();

    offset += waveSpeed;
    requestAnimationFrame(drawWave);
}

drawWave();
