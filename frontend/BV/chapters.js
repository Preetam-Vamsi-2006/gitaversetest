// Chapter data
const chapters = [
    {
        number: 1,
        name: "Arjuna's Vishada Yoga",
        sanskrit: "अर्जुनविषादयोग",
        verses: 47,
        description: "The Yoga of Arjuna's Dejection"
    },
    {
        number: 2,
        name: "Samkhya Yoga",
        sanskrit: "सांख्ययोग",
        verses: 72,
        description: "The Yoga of Knowledge"
    },
    {
        number: 3,
        name: "Karma Yoga",
        sanskrit: "कर्मयोग",
        verses: 43,
        description: "The Yoga of Action"
    },
    {
        number: 4,
        name: "Jnana Karma Sanyasa Yoga",
        sanskrit: "ज्ञानकर्मसंन्यासयोग",
        verses: 42,
        description: "The Yoga of Knowledge and Renunciation"
    },
    {
        number: 5,
        name: "Karma Sanyasa Yoga",
        sanskrit: "कर्मसंन्यासयोग",
        verses: 29,
        description: "The Yoga of Renunciation of Action"
    },
    {
        number: 6,
        name: "Dhyana Yoga",
        sanskrit: "ध्यानयोग",
        verses: 47,
        description: "The Yoga of Meditation"
    },
    {
        number: 7,
        name: "Jnana Vijnana Yoga",
        sanskrit: "ज्ञानविज्ञानयोग",
        verses: 30,
        description: "The Yoga of Knowledge and Wisdom"
    },
    {
        number: 8,
        name: "Akshar Brahma Yoga",
        sanskrit: "अक्षरब्रह्मयोग",
        verses: 28,
        description: "The Yoga of the Imperishable Brahman"
    },
    {
        number: 9,
        name: "Rajavidya Rajaguhya Yoga",
        sanskrit: "राजविद्याराजगुह्ययोग",
        verses: 34,
        description: "The Yoga of Royal Knowledge and Royal Secret"
    },
    {
        number: 10,
        name: "Vibhuti Yoga",
        sanskrit: "विभूतियोग",
        verses: 42,
        description: "The Yoga of Divine Glories"
    },
    {
        number: 11,
        name: "Visvarupa Darsana Yoga",
        sanskrit: "विश्वरूपदर्शनयोग",
        verses: 55,
        description: "The Yoga of the Vision of the Universal Form"
    },
    {
        number: 12,
        name: "Bhakti Yoga",
        sanskrit: "भक्तियोग",
        verses: 20,
        description: "The Yoga of Devotion"
    },
    {
        number: 13,
        name: "Kshetra Kshetrajna Vibhaga Yoga",
        sanskrit: "क्षेत्रक्षेत्रज्ञविभागयोग",
        verses: 35,
        description: "The Yoga of Distinction between Field and Knower"
    },
    {
        number: 14,
        name: "Guna Traya Vibhaga Yoga",
        sanskrit: "गुणत्रयविभागयोग",
        verses: 27,
        description: "The Yoga of the Division of Three Gunas"
    },
    {
        number: 15,
        name: "Purushottama Yoga",
        sanskrit: "पुरुषोत्तमयोग",
        verses: 20,
        description: "The Yoga of the Supreme Person"
    },
    {
        number: 16,
        name: "Daivasura Sampad Vibhaga Yoga",
        sanskrit: "दैवासुरसम्पद्विभागयोग",
        verses: 24,
        description: "The Yoga of Divine and Demoniac Qualities"
    },
    {
        number: 17,
        name: "Shraddha Traya Vibhaga Yoga",
        sanskrit: "श्रद्धात्रयविभागयोग",
        verses: 28,
        description: "The Yoga of the Division of Three Types of Faith"
    },
    {
        number: 18,
        name: "Moksha Sanyasa Yoga",
        sanskrit: "मोक्षसंन्यासयोग",
        verses: 78,
        description: "The Yoga of Liberation through Renunciation"
    }
];

// Generate chapter cards
function generateChapterCards() {
    const container = document.querySelector('.chapters-container');
    
    chapters.forEach(chapter => {
        const card = document.createElement('div');
        card.className = 'chapter-card';
        card.onclick = () => navigateToChapter(chapter.number);
        
        card.innerHTML = `
            <div class="chapter-number">${chapter.number}</div>
            <div class="chapter-header">
                <h2 class="chapter-name">${chapter.name}</h2>
                <p class="chapter-sanskrit">${chapter.sanskrit}</p>
                <p class="chapter-verses">${chapter.verses} verses</p>
            </div>
            <p class="chapter-description">${chapter.description}</p>
        `;
        
        container.appendChild(card);
    });
}

// Navigate to individual chapter page
function navigateToChapter(chapterNumber) {
    // Add transition effect
    document.body.classList.add('warp');
    document.querySelector('.chakra-layer').classList.add('portal');
    
    setTimeout(() => {
        window.location.href = `chapter-${chapterNumber}.html`;
    }, 600);
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Divine cursor
const cursor = document.querySelector('.divine-cursor');

document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
});

document.addEventListener('mousedown', () => {
    cursor.classList.add('click');
});

document.addEventListener('mouseup', () => {
    cursor.classList.remove('click');
});

// Particle effect (dust canvas)
const canvas = document.getElementById('dustCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const particleCount = 100;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 0.5;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * 0.5 - 0.25;
        this.opacity = Math.random() * 0.5 + 0.2;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > canvas.width) this.x = 0;
        if (this.x < 0) this.x = canvas.width;
        if (this.y > canvas.height) this.y = 0;
        if (this.y < 0) this.y = canvas.height;
    }

    draw() {
        ctx.fillStyle = `rgba(212, 175, 55, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function initParticles() {
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    requestAnimationFrame(animateParticles);
}

// Handle window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    generateChapterCards();
    initParticles();
    animateParticles();
});