// 3D渐变网格背景
class GridBackground {
    constructor() {
        this.canvas = document.getElementById('background-canvas');
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: true
        });

        this.gridSize = 20;
        this.spacing = 2;
        this.points = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.targetX = 0;
        this.targetY = 0;

        this.init();
    }

    init() {
        // 设置渲染器
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        // 设置相机位置
        this.camera.position.z = 30;

        // 创建网格
        this.createGrid();

        // 添加事件监听
        window.addEventListener('resize', this.onWindowResize.bind(this));
        document.addEventListener('mousemove', this.onMouseMove.bind(this));
        document.addEventListener('scroll', this.onScroll.bind(this));
        document.addEventListener('themeChanged', this.onThemeChange.bind(this));

        // 开始动画
        this.animate();
    }

    createGrid() {
        // 清除现有的点
        this.points.forEach(point => this.scene.remove(point));
        this.points = [];

        // 创建材质
        const material = new THREE.PointsMaterial({
            size: 0.1,
            sizeAttenuation: true,
            transparent: true,
            opacity: 0.8
        });

        // 根据主题设置颜色
        this.updateColors(document.body.classList.contains('theme-dark') ? 'dark' : 'light');

        // 创建网格点
        for (let x = -this.gridSize; x <= this.gridSize; x++) {
            for (let y = -this.gridSize; y <= this.gridSize; y++) {
                const geometry = new THREE.BufferGeometry();
                const position = new Float32Array([x * this.spacing, y * this.spacing, 0]);
                geometry.setAttribute('position', new THREE.BufferAttribute(position, 3));

                const point = new THREE.Points(geometry, material.clone());
                this.scene.add(point);
                this.points.push(point);
            }
        }
    }

    updateColors(theme) {
        const colors = theme === 'dark' 
            ? {
                primary: new THREE.Color('#1f2937'),
                secondary: new THREE.Color('#1E40AF'),
                accent: new THREE.Color('#059669')
            }
            : {
                primary: new THREE.Color('#38BDF8'),
                secondary: new THREE.Color('#818CF8'),
                accent: new THREE.Color('#34D399')
            };

        this.points.forEach((point, index) => {
            const progress = index / this.points.length;
            const color = new THREE.Color().lerpColors(
                colors.primary,
                colors.secondary,
                progress
            );
            point.material.color = color;
        });
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    onMouseMove(event) {
        this.mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    }

    onScroll() {
        const scrollProgress = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
        this.camera.position.y = -scrollProgress * 5;
    }

    onThemeChange(event) {
        this.updateColors(event.detail.theme);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));

        // 平滑相机移动
        this.targetX += (this.mouseX - this.targetX) * 0.05;
        this.targetY += (this.mouseY - this.targetY) * 0.05;

        // 网格扭曲效果
        this.points.forEach((point, index) => {
            const position = point.geometry.attributes.position;
            const originalX = Math.floor(index / (this.gridSize * 2 + 1)) * this.spacing - this.gridSize * this.spacing;
            const originalY = (index % (this.gridSize * 2 + 1)) * this.spacing - this.gridSize * this.spacing;

            position.array[2] = Math.sin(Date.now() * 0.001 + index * 0.1) * 2
                + Math.cos(this.targetX * Math.PI + originalX * 0.1) * 2
                + Math.sin(this.targetY * Math.PI + originalY * 0.1) * 2;
            
            position.needsUpdate = true;
        });

        // 渲染场景
        this.renderer.render(this.scene, this.camera);
    }
}

// 初始化背景
document.addEventListener('DOMContentLoaded', () => {
    window.gridBackground = new GridBackground();
    // 导出更新颜色方法供主题切换使用
    window.updateGridColors = (theme) => window.gridBackground.updateColors(theme);
});