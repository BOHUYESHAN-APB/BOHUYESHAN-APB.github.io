document.addEventListener('DOMContentLoaded', () => {
    // AI Simulation: Seed Filtering (using IDs from task.md and new index.html)
    const seedFilterButton = document.getElementById('seed-filter-button');
    const seedFilterResult = document.getElementById('seed-filter-result');

    if (seedFilterButton && seedFilterResult) {
        seedFilterButton.addEventListener('click', () => {
            seedFilterButton.textContent = '正在筛选...';
            seedFilterButton.disabled = true;
            seedFilterButton.classList.add('opacity-50', 'cursor-not-allowed'); // Tailwind classes for disabled state

            setTimeout(() => {
                seedFilterResult.classList.remove('hidden');
                seedFilterButton.textContent = '筛选完成';
                // Keep button disabled after one run as per original task.md logic
                // If re-run is desired, uncomment below:
                // seedFilterButton.disabled = false;
                // seedFilterButton.classList.remove('opacity-50', 'cursor-not-allowed');
            }, 1500);
        });
    }

    // AI Simulation: Sprout Evaluation/QC (using IDs from task.md and new index.html)
    const sproutEvalButton = document.getElementById('sprout-eval-button'); // ID from task.md
    const sproutEvalResult = document.getElementById('sprout-eval-result'); // ID from task.md

    if (sproutEvalButton && sproutEvalResult) {
        sproutEvalButton.addEventListener('click', () => {
            sproutEvalButton.textContent = '正在计数...'; // Text from task.md
            sproutEvalButton.disabled = true;
            sproutEvalButton.classList.add('opacity-50', 'cursor-not-allowed');

            setTimeout(() => {
                sproutEvalResult.classList.remove('hidden');
                sproutEvalButton.textContent = '计数完成'; // Text from task.md
                // Keep button disabled
            }, 1500);
        });
    }
});