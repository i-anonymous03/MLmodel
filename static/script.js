document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const imagePreview = document.getElementById('imagePreview');
    const uploadContent = document.querySelector('.upload-content');
    
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');
    const emotionBadge = document.getElementById('emotionBadge');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    
    const toggleBreakdownBtn = document.getElementById('toggleBreakdownBtn');
    const breakdownContainer = document.getElementById('breakdownContainer');
    const chartWrapper = document.getElementById('chartWrapper');

    // Click to upload
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and Drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // File Input Change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            showError("Please upload an image file (JPG, PNG).");
            return;
        }

        // Display Preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
            
            // Add loaded class for animation
            setTimeout(() => {
                imagePreview.classList.add('loaded');
            }, 50);
            
            uploadContent.classList.add('hidden');
            
            // Upload to backend
            uploadImage(file);
        };
        reader.readAsDataURL(file);
    }

    async function uploadImage(file) {
        // Reset UI
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        breakdownContainer.classList.add('hidden');
        loader.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(window.location.origin + '/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            loader.classList.add('hidden');

            if (data.success) {
                // Show Result
                emotionBadge.textContent = data.complex_emotion;
                resultContainer.classList.remove('hidden');
                
                // Build Chart
                buildChart(data.breakdown);
            } else {
                showError(data.error || "Failed to analyze image.");
            }
        } catch (error) {
            loader.classList.add('hidden');
            showError("Network error. Please make sure the server is running.");
        }
    }

    function buildChart(breakdown) {
        chartWrapper.innerHTML = '';
        
        // Sort breakdown by value descending
        const sorted = Object.entries(breakdown).sort((a, b) => b[1] - a[1]);

        sorted.forEach(([emotion, value], index) => {
            const percentage = Math.max(0.5, value).toFixed(1); // Min 0.5% for visibility
            
            const row = document.createElement('div');
            row.className = 'chart-row';
            // Staggered animation delay
            row.style.animationDelay = `${index * 0.1}s`;
            
            row.innerHTML = `
                <div class="chart-label">${emotion}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: 0%" data-width="${percentage}%"></div>
                </div>
                <div class="chart-value">${value < 0.1 ? '<0.1' : value.toFixed(1)}%</div>
            `;
            
            chartWrapper.appendChild(row);
        });

        // Animate bars after a short delay
        setTimeout(() => {
            const bars = document.querySelectorAll('.chart-bar');
            bars.forEach(bar => {
                bar.style.width = bar.getAttribute('data-width');
            });
        }, 150);
    }

    toggleBreakdownBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering upload zone click
        breakdownContainer.classList.toggle('hidden');
        if (breakdownContainer.classList.contains('hidden')) {
            toggleBreakdownBtn.textContent = 'View Breakdown';
        } else {
            toggleBreakdownBtn.textContent = 'Hide Breakdown';
        }
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorContainer.classList.remove('hidden');
    }
});

// --- Antigravity Background Animation Engine ---
const canvas = document.getElementById('antigravity-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.4;
            this.speedY = Math.random() * -0.8 - 0.1;
            const hue = 200 + Math.random() * 50; 
            this.color = `hsla(${hue}, 100%, 70%, ${Math.random() * 0.5 + 0.2})`;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.y + this.size < 0) {
                this.y = height + this.size;
                this.x = Math.random() * width;
            }
            if (this.x > width + this.size) this.x = -this.size;
            if (this.x < -this.size) this.x = width + this.size;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 12;
            ctx.shadowColor = this.color;
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        const particleCount = Math.floor((width * height) / 12000); 
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        requestAnimationFrame(animateParticles);
    }

    initParticles();
    animateParticles();
}
