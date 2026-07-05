// 页面动画效果管理
class AnimationManager {
    constructor() {
        // 初始化动画元素
        this.glitchText = document.querySelector('.glitch-text');
        this.neumorphicCards = document.querySelectorAll('[data-tilt]');
        this.fadeElements = document.querySelectorAll('.fade-in');
        this.slideLeftElements = document.querySelectorAll('.slide-in-left');
        this.slideRightElements = document.querySelectorAll('.slide-in-right');

        this.init();
    }

    init() {
        // 初始化故障文字动画
        this.initGlitchAnimation();
        
        // 初始化新拟态卡片倾斜效果
        this.initTiltAnimation();
        
        // 初始化滚动触发动画
        this.initScrollAnimations();
        
        // 监听主题变化
        document.addEventListener('themeChanged', this.onThemeChange.bind(this));
    }

    initGlitchAnimation() {
        if (!this.glitchText) return;

        // 使用 anime.js 创建故障动画
        const glitchAnimation = anime.timeline({
            loop: true,
            direction: 'alternate'
        });

        glitchAnimation
            .add({
                targets: this.glitchText,
                textShadow: [
                    { value: '2px 2px var(--accent), -2px -2px var(--primary)' },
                    { value: '-2px -2px var(--accent), 2px 2px var(--primary)' },
                    { value: '2px -2px var(--primary), -2px 2px var(--accent)' },
                    { value: '2px 2px var(--accent), -2px -2px var(--primary)' }
                ],
                duration: 100,
                easing: 'steps(1)',
                delay: anime.random(0, 2000)
            })
            .add({
                targets: this.glitchText,
                duration: 50,
                skew: [10, -10],
                easing: 'steps(1)'
            })
            .add({
                targets: this.glitchText,
                duration: 50,
                skew: 0,
                easing: 'steps(1)'
            });
    }

    initTiltAnimation() {
        if (!this.neumorphicCards.length) return;

        // 使用 vanilla-tilt.js 初始化倾斜效果
        this.neumorphicCards.forEach(card => {
            VanillaTilt.init(card, {
                max: 5,
                speed: 400,
                glare: true,
                'max-glare': 0.2,
                scale: 1.02
            });
        });
    }

    initScrollAnimations() {
        // 创建 Intersection Observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // 只触发一次
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // 观察所有需要动画的元素
        [...this.fadeElements, ...this.slideLeftElements, ...this.slideRightElements]
            .forEach(element => observer.observe(element));
    }

    onThemeChange() {
        // 主题变化时重新初始化故障动画
        this.initGlitchAnimation();

        // 更新卡片阴影效果
        this.neumorphicCards.forEach(card => {
            if (card.vanillaTilt) {
                card.vanillaTilt.destroy();
            }
        });
        this.initTiltAnimation();
    }

    // 创建滚动指示器动画
    createScrollIndicator() {
        const indicator = document.querySelector('.scroll-indicator');
        if (!indicator) return;

        anime({
            targets: '.mouse::before',
            translateY: [0, 20],
            opacity: [1, 0],
            easing: 'easeInOutQuad',
            duration: 1000,
            loop: true
        });
    }

    // 添加页面切换动画
    addPageTransition() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', e => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    anime({
                        targets: targetElement,
                        opacity: [0, 1],
                        translateY: [20, 0],
                        duration: 800,
                        easing: 'easeOutExpo',
                        begin: () => {
                            targetElement.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }
                    });
                }
            });
        });
    }
}

// 初始化动画管理器
document.addEventListener('DOMContentLoaded', () => {
    window.animationManager = new AnimationManager();
    window.animationManager.createScrollIndicator();
    window.animationManager.addPageTransition();
});