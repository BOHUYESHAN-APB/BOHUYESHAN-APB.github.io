// 主题切换功能
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // 从本地存储获取主题设置
    const getCurrentTheme = () => {
        let theme = localStorage.getItem('theme');
        if (!theme) {
            theme = prefersDarkScheme.matches ? 'dark' : 'light';
        }
        return theme;
    };

    // 应用主题
    const applyTheme = (theme) => {
        document.body.className = `theme-${theme}`;
        localStorage.setItem('theme', theme);
        
        // 更新网格背景颜色
        if (window.updateGridColors) {
            window.updateGridColors(theme);
        }

        // 触发自定义事件
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    };

    // 初始化主题
    applyTheme(getCurrentTheme());

    // 主题切换按钮点击事件
    themeToggle.addEventListener('click', () => {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // 添加过渡动画类
        document.body.classList.add('theme-transition');
        
        // 应用新主题
        applyTheme(newTheme);
        
        // 动画结束后移除过渡类
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 300);
    });

    // 监听系统主题变化
    prefersDarkScheme.addEventListener('change', (e) => {
        const theme = e.matches ? 'dark' : 'light';
        applyTheme(theme);
    });
});