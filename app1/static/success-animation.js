// GSAP Animation Timeline
gsap.timeline({
    defaults: { ease: "back.out(1.7)" }
})
.from(".checkmark", { 
    duration: 0.8, 
    scale: 0, 
    rotation: -180,
    opacity: 1 
})
.to(".checkmark__circle", { 
    duration: 0.6, 
    strokeDashoffset: 0 
}, "-=0.5")
.to(".checkmark__check", { 
    duration: 0.4, 
    strokeDashoffset: 0 
}, "-=0.4")
.to(".checkmark", { 
    duration: 0.3, 
    scale: 1.1 
}, "-=0.2")
.to(".checkmark", { 
    duration: 0.3, 
    scale: 1 
}, "-=0.3")

// Stagger content reveals
.from(".fade-in", { 
    duration: 0.8, 
    y: 30, 
    opacity: 0,
    stagger: 0.2 
}, "-=0.5")

.from(".slide-in", { 
    duration: 0.6, 
    y: 20, 
    opacity: 0,
    stagger: 0.1 
}, "-=0.6")

// Optional: Quick confetti burst
function createConfetti() {
    const wrapper = document.querySelector('.animation-wrapper');
    const colors = ['#FFD700', '#FF69B4', '#00FF00', '#4169E1'];
    for (let i = 0; i < 15; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        wrapper.appendChild(confetti);
        
        // Remove after animation
        setTimeout(() => confetti.remove(), 3000);
    }
}

// Trigger confetti after checkmark
gsap.delayedCall(1, createConfetti);