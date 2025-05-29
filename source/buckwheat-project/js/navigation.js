document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuOpenIcon = document.getElementById('menu-open-icon');
    const menuCloseIcon = document.getElementById('menu-close-icon');

    if (mobileMenuButton && mobileMenu && menuOpenIcon && menuCloseIcon) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            menuOpenIcon.classList.toggle('hidden');
            menuCloseIcon.classList.toggle('hidden');
        });
    }

    // Smooth scroll for all anchor links pointing to an ID, and active state management
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    const mobileNavLinks = document.querySelectorAll('#mobile-menu a[href^="#"]');
    const allNavLinks = [...navLinks, ...mobileNavLinks]; // Combine both desktop and mobile links

    allNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor behavior
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                // Calculate offset for fixed navbar
                const navbarHeight = document.querySelector('nav').offsetHeight || 64; // Fallback height
                const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                const offsetPosition = elementPosition - navbarHeight;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }

            // Close mobile menu if a link inside it is clicked
            if (mobileMenu && !mobileMenu.classList.contains('hidden') && this.closest('#mobile-menu')) {
                mobileMenu.classList.add('hidden');
                if (menuOpenIcon && menuCloseIcon) {
                    menuOpenIcon.classList.remove('hidden');
                    menuCloseIcon.classList.add('hidden');
                }
            }
            
            // Set active class (basic version, scroll listener will refine it)
            // Remove active from all nav items first
            document.querySelectorAll('nav a.nav-item, #mobile-menu a.nav-item-mobile').forEach(navLink => {
                navLink.classList.remove('active');
            });
            // Add active to the clicked link (and its counterpart if exists)
            this.classList.add('active');
            const counterpartLink = document.querySelector(`nav a.nav-item[href="${targetId}"], #mobile-menu a.nav-item-mobile[href="${targetId}"]`);
            if(counterpartLink && counterpartLink !== this) {
                counterpartLink.classList.add('active');
            }

        });
    });

    // Active state on scroll
    const sections = document.querySelectorAll('main section[id], header[id]');
    const desktopNavItems = document.querySelectorAll('nav .hidden.md\\:block a.nav-item');
    const mobileNavItems = document.querySelectorAll('#mobile-menu a.nav-item-mobile');

    function updateActiveNav() {
        if (sections.length === 0) return;
        let currentActiveId = '';
        const navbarHeight = document.querySelector('nav').offsetHeight || 64;

        sections.forEach(section => {
            const sectionTop = section.offsetTop - navbarHeight - 20; // 20px buffer
            if (window.pageYOffset >= sectionTop) {
                currentActiveId = section.getAttribute('id');
            }
        });
        
        // Special case for hero if nothing else is active and at top
        if (window.pageYOffset < (sections[0]?.offsetTop - navbarHeight - 20) && sections[0]?.id === 'hero') {
             currentActiveId = 'hero';
        } else if (!currentActiveId && window.pageYOffset < (sections[0]?.offsetTop - navbarHeight - 20)) {
            // If scrolled to the very top and hero is not the first section, or no sections found yet.
            // Default to hero if it exists.
            if (document.getElementById('hero')) currentActiveId = 'hero';
        }


        desktopNavItems.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentActiveId}`) {
                link.classList.add('active');
            }
        });
        mobileNavItems.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentActiveId}`) {
                link.classList.add('active');
            }
        });
    }

    if (sections.length > 0) {
        window.addEventListener('scroll', updateActiveNav);
        updateActiveNav(); // Initial call
    }
});