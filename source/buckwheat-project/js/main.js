document.addEventListener('DOMContentLoaded', () => {
    // Dynamic year in footer
    const currentYearSpan = document.getElementById('current-year');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    // project_demo.html uses a mailto link for contact, so no form submission JS is needed from that reference.
    // If a form were used (as in the original task.md), the following could be adapted:
    /*
    const contactForm = document.getElementById('contact-form'); // Assuming a form with this ID
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('感谢您的留言！此表单为演示用途，信息未实际发送。');
            contactForm.reset();
        });
    }
    */
});