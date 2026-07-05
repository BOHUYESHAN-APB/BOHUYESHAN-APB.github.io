// 主程序入口
class App {
    constructor() {
        this.mobileMenuButton = document.querySelector('.mobile-menu-btn');
        this.mobileNav = null; // 将在初始化时创建
        this.isMenuOpen = false;

        this.init();
    }

    init() {
        // 创建移动导航
        this.createMobileNav();
        
        // 初始化事件监听
        this.initEventListeners();
        
        // 设置页面加载动画
        this.setupPageLoadAnimation();
        
        // 初始化性能优化
        this.setupPerformanceOptimizations();
    }

    createMobileNav() {
        // 创建移动导航元素
        this.mobileNav = document.createElement('nav');
        this.mobileNav.className = 'mobile-nav';
        this.mobileNav.innerHTML = document.querySelector('.nav-links').innerHTML;
        document.body.appendChild(this.mobileNav);
    }

    initEventListeners() {
        // 移动菜单切换
        if (this.mobileMenuButton) {
            this.mobileMenuButton.addEventListener('click', () => this.toggleMobileMenu());
        }

        // 页面滚动处理
        let lastScrollTop = 0;
        const navbar = document.querySelector('.main-nav');
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // 导航栏显示/隐藏逻辑
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop;
        }, { passive: true });

        // 监听所有链接点击
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => this.handleLinkClick(e));
        });

        // 监听窗口大小变化
        window.addEventListener('resize', this.handleResize.bind(this));

        // 监听页面可见性变化
        document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
    }

    toggleMobileMenu() {
        this.isMenuOpen = !this.isMenuOpen;
        this.mobileMenuButton.classList.toggle('mobile-menu-open');
        this.mobileNav.classList.toggle('open');
        
        // 禁用/启用页面滚动
        document.body.style.overflow = this.isMenuOpen ? 'hidden' : '';
    }

    handleLinkClick(e) {
        const targetId = e.currentTarget.getAttribute('href');
        if (targetId === '#') return;

        e.preventDefault();
        
        // 如果菜单是打开的，关闭它
        if (this.isMenuOpen) {
            this.toggleMobileMenu();
        }

        // 平滑滚动到目标位置
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const navHeight = document.querySelector('.main-nav').offsetHeight;
            const targetPosition = targetElement.offsetTop - navHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    handleResize() {
        // 重置移动菜单状态
        if (window.innerWidth > 768 && this.isMenuOpen) {
            this.toggleMobileMenu();
        }

        // 更新背景canvas大小
        if (window.gridBackground) {
            window.gridBackground.onWindowResize();
        }
    }

    handleVisibilityChange() {
        // 页面不可见时暂停动画
        if (document.hidden) {
            if (window.gridBackground) {
                window.gridBackground.renderer.setAnimationLoop(null);
            }
        } else {
            if (window.gridBackground) {
                window.gridBackground.renderer.setAnimationLoop(window.gridBackground.animate.bind(window.gridBackground));
            }
        }
    }

    setupPageLoadAnimation() {
        // 页面加载完成后的动画
        window.addEventListener('load', () => {
            document.body.classList.add('loaded');
            
            // 触发首屏元素动画
            const heroElements = document.querySelectorAll('.hero-section *');
            heroElements.forEach((element, index) => {
                element.style.animationDelay = `${index * 0.1}s`;
                element.classList.add('fade-in', 'visible');
            });
        });
    }

    setupPerformanceOptimizations() {
        // 使用 requestIdleCallback 延迟加载非关键资源
        if ('requestIdleCallback' in window) {
            requestIdleCallback(this.loadNonCriticalResources);
        } else {
            setTimeout(this.loadNonCriticalResources, 1000);
        }

        // 使用 IntersectionObserver 优化图片加载
        this.setupLazyLoading();
    }

    loadNonCriticalResources() {
        // 加载额外的字体
        const fontLink = document.createElement('link');
        fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@800;900&display=swap';
        fontLink.rel = 'stylesheet';
        document.head.appendChild(fontLink);
    }

    setupLazyLoading() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});