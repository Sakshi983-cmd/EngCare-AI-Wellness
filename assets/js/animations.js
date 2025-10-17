// EngCare Advanced - JavaScript Animations & Interactions

class EngCareAnimations {
    constructor() {
        this.initializeAnimations();
        this.setupEventListeners();
        this.initializeParticles();
        this.startRealTimeUpdates();
    }

    // Initialize all animations
    initializeAnimations() {
        this.animateOnScroll();
        this.initializeStressMeter();
        this.setupTypingAnimations();
        this.initializeConfetti();
        this.setupMicroInteractions();
    }

    // Setup event listeners
    setupEventListeners() {
        // Stress meter hover effects
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('stress-meter')) {
                this.animateStressPulse(e.target);
            }
        });

        // Achievement badge animations
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('badge')) {
                this.animateBadgeClick(e.target);
            }
        });

        // Glass card interactions
        document.addEventListener('mouseenter', (e) => {
            if (e.target.classList.contains('glass-card')) {
                this.animateCardHover(e.target);
            }
        }, true);

        // Progress bar animations
        this.animateProgressBars();
    }

    // Initialize particles.js background
    initializeParticles() {
        if (typeof particlesJS !== 'undefined') {
            particlesJS('particles-js', {
                particles: {
                    number: {
                        value: 80,
                        density: {
                            enable: true,
                            value_area: 800
                        }
                    },
                    color: {
                        value: '#667eea'
                    },
                    shape: {
                        type: 'circle',
                        stroke: {
                            width: 0,
                            color: '#000000'
                        }
                    },
                    opacity: {
                        value: 0.5,
                        random: true,
                        anim: {
                            enable: true,
                            speed: 1,
                            opacity_min: 0.1,
                            sync: false
                        }
                    },
                    size: {
                        value: 3,
                        random: true,
                        anim: {
                            enable: true,
                            speed: 2,
                            size_min: 0.1,
                            sync: false
                        }
                    },
                    line_linked: {
                        enable: true,
                        distance: 150,
                        color: '#764ba2',
                        opacity: 0.4,
                        width: 1
                    },
                    move: {
                        enable: true,
                        speed: 2,
                        direction: 'none',
                        random: true,
                        straight: false,
                        out_mode: 'out',
                        bounce: false,
                        attract: {
                            enable: false,
                            rotateX: 600,
                            rotateY: 1200
                        }
                    }
                },
                interactivity: {
                    detect_on: 'canvas',
                    events: {
                        onhover: {
                            enable: true,
                            mode: 'grab'
                        },
                        onclick: {
                            enable: true,
                            mode: 'push'
                        },
                        resize: true
                    },
                    modes: {
                        grab: {
                            distance: 140,
                            line_linked: {
                                opacity: 1
                            }
                        },
                        push: {
                            particles_nb: 4
                        }
                    }
                },
                retina_detect: true
            });
        }
    }

    // Animate elements on scroll
    animateOnScroll() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    
                    // Add specific animations based on element type
                    if (entry.target.classList.contains('metric-card')) {
                        this.animateMetricCard(entry.target);
                    }
                    
                    if (entry.target.classList.contains('progress-bar')) {
                        this.animateProgressBar(entry.target);
                    }
                }
            });
        }, observerOptions);

        // Observe all animatable elements
        document.querySelectorAll('.glass-card, .metric-card, .badge, .progress-bar').forEach(el => {
            observer.observe(el);
        });
    }

    // Initialize stress meter with real-time updates
    initializeStressMeter() {
        const stressMeters = document.querySelectorAll('.stress-level');
        stressMeters.forEach(meter => {
            this.animateStressLevel(meter);
        });
    }

    // Animate stress level changes
    animateStressLevel(stressElement) {
        const currentLevel = parseFloat(stressElement.style.width) || 0;
        const targetLevel = parseFloat(stressElement.dataset.target) || currentLevel;
        
        if (currentLevel !== targetLevel) {
            stressElement.style.width = targetLevel + '%';
            
            // Update animation based on stress level
            if (targetLevel > 70) {
                stressElement.classList.remove('moderate');
                stressElement.classList.add('high');
            } else if (targetLevel > 40) {
                stressElement.classList.remove('high');
                stressElement.classList.add('moderate');
            } else {
                stressElement.classList.remove('moderate', 'high');
            }
        }
    }

    // Stress pulse animation on hover
    animateStressPulse(stressMeter) {
        const pulse = document.createElement('div');
        pulse.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.3);
            border-radius: 15px;
            animation: stressPulse 0.6s ease-out;
        `;
        
        stressMeter.appendChild(pulse);
        
        setTimeout(() => {
            pulse.remove();
        }, 600);
    }

    // Setup typing animations for AI responses
    setupTypingAnimations() {
        const typingElements = document.querySelectorAll('.typing-demo');
        typingElements.forEach(element => {
            this.startTypingAnimation(element);
        });
    }

    // Start typing animation
    startTypingAnimation(element) {
        const text = element.textContent;
        element.textContent = '';
        element.style.borderRight = '3px solid';
        
        let i = 0;
        const typing = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typing);
                element.style.borderRight = 'none';
            }
        }, 100);
    }

    // Initialize confetti for achievements
    initializeConfetti() {
        this.confettiCanvas = document.createElement('canvas');
        this.confettiCanvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
        `;
        document.body.appendChild(this.confettiCanvas);
    }

    // Launch confetti animation
    launchConfetti() {
        const confettiSettings = { target: this.confettiCanvas };
        const confetti = new ConfettiGenerator(confettiSettings);
        confetti.render();
        
        setTimeout(() => {
            confetti.clear();
        }, 3000);
    }

    // Animate badge clicks
    animateBadgeClick(badge) {
        badge.style.transform = 'scale(0.9)';
        setTimeout(() => {
            badge.style.transform = 'scale(1)';
        }, 150);
        
        // Add sparkle effect
        this.createSparkleEffect(badge);
    }

    // Create sparkle effect for badges
    createSparkleEffect(element) {
        const rect = element.getBoundingClientRect();
        for (let i = 0; i < 5; i++) {
            const sparkle = document.createElement('div');
            sparkle.style.cssText = `
                position: fixed;
                width: 6px;
                height: 6px;
                background: white;
                border-radius: 50%;
                pointer-events: none;
                z-index: 100;
                left: ${rect.left + Math.random() * rect.width}px;
                top: ${rect.top + Math.random() * rect.height}px;
                animation: sparkleFly 1s ease-out forwards;
            `;
            
            document.body.appendChild(sparkle);
            
            setTimeout(() => {
                sparkle.remove();
            }, 1000);
        }
    }

    // Animate card hover effects
    animateCardHover(card) {
        const glow = document.createElement('div');
        glow.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(102,126,234,0.1) 0%, transparent 70%);
            border-radius: 20px;
            pointer-events: none;
            z-index: -1;
        `;
        
        card.appendChild(glow);
        
        setTimeout(() => {
            if (glow.parentNode === card) {
                glow.remove();
            }
        }, 300);
    }

    // Animate progress bars
    animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            this.animateProgressBar(bar);
        });
    }

    // Animate individual progress bar
    animateProgressBar(progressBar) {
        const targetWidth = progressBar.dataset.width || '100%';
        progressBar.style.width = '0%';
        
        setTimeout(() => {
            progressBar.style.width = targetWidth;
        }, 500);
    }

    // Animate metric cards
    animateMetricCard(card) {
        const valueElement = card.querySelector('.metric-value');
        if (valueElement) {
            const finalValue = parseFloat(valueElement.textContent);
            this.animateCounter(valueElement, 0, finalValue, 2000);
        }
    }

    // Animate number counters
    animateCounter(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value;
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Setup micro-interactions
    setupMicroInteractions() {
        // Button ripple effect
        document.addEventListener('click', (e) => {
            if (e.target.closest('.stButton button')) {
                this.createRippleEffect(e);
            }
        });

        // Hover sound effects (optional)
        this.setupHoverSounds();
    }

    // Create ripple effect on buttons
    createRippleEffect(event) {
        const button = event.target.closest('.stButton button');
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 600ms linear;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
        `;
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Setup hover sounds (optional)
    setupHoverSounds() {
        // This can be implemented with Howler.js or similar library
        console.log('Hover sounds setup - ready for implementation');
    }

    // Real-time data updates
    startRealTimeUpdates() {
        // Simulate real-time stress level updates
        setInterval(() => {
            this.updateRealTimeData();
        }, 5000);
    }

    // Update real-time data displays
    updateRealTimeData() {
        // Update stress meters
        const stressMeters = document.querySelectorAll('.stress-level');
        stressMeters.forEach(meter => {
            const currentLevel = parseFloat(meter.style.width) || 50;
            const variation = (Math.random() - 0.5) * 20;
            const newLevel = Math.max(0, Math.min(100, currentLevel + variation));
            
            meter.dataset.target = newLevel;
            this.animateStressLevel(meter);
        });

        // Update metrics
        this.updateLiveMetrics();
    }

    // Update live metrics
    updateLiveMetrics() {
        const metrics = document.querySelectorAll('.metric-value');
        metrics.forEach(metric => {
            const currentValue = parseFloat(metric.textContent);
            const variation = (Math.random() - 0.5) * 10;
            const newValue = Math.max(0, currentValue + variation);
            
            this.animateCounter(metric, currentValue, Math.round(newValue), 1000);
        });
    }

    // Achievement unlock animation
    unlockAchievement(achievementName) {
        this.launchConfetti();
        
        // Create achievement notification
        this.createAchievementNotification(achievementName);
    }

    // Create achievement notification
    createAchievementNotification(achievementName) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--gradient-primary);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">🎉</span>
                <div>
                    <strong>Achievement Unlocked!</strong>
                    <div>${achievementName}</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Animate out
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }

    // Matrix rain effect for background
    createMatrixRain() {
        const canvas = document.createElement('canvas');
        canvas.className = 'matrix-rain';
        document.body.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const characters = '01';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        
        for (let i = 0; i < columns; i++) {
            drops[i] = 1;
        }
        
        function draw() {
            ctx.fillStyle = 'rgba(15, 15, 35, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#667eea';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = characters.charAt(Math.floor(Math.random() * characters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        setInterval(draw, 33);
    }
}

// CSS for dynamic animations
const dynamicStyles = `
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

@keyframes sparkleFly {
    0% {
        transform: translate(0, 0) scale(1);
        opacity: 1;
    }
    100% {
        transform: translate(${Math.random() * 100 - 50}px, -100px) scale(0);
        opacity: 0;
    }
}

@keyframes stressPulse {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.05);
        opacity: 0.8;
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}
`;

// Add dynamic styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.engCareAnimations = new EngCareAnimations();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EngCareAnimations;
}
