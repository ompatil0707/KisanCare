document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const langBtn = document.getElementById('language-btn');
    const langDropdown = document.getElementById('language-dropdown');
    const langOptions = langDropdown.querySelectorAll('button');

    // === Restore Theme from localStorage ===
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.remove('light-theme', 'dark-theme');
        body.classList.add(savedTheme);
    }

    // === Toggle Theme (Preserving Your Original) ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        body.classList.toggle('light-theme');
        const newTheme = body.classList.contains('dark-theme') ? 'dark-theme' : 'light-theme';
        localStorage.setItem('theme', newTheme);
    });

    const translationScript = document.getElementById('ui-translations');
    const translations = translationScript ? JSON.parse(translationScript.textContent) : {};


    function applyTranslations(lang) {
        const t = translations[lang] || translations;
        if (!t) {
            return;
        }
        const predictionCard = document.querySelector('.card h2');
        if (predictionCard) predictionCard.textContent = t.prediction;

        const labels = document.querySelectorAll('.card p strong');
        labels.forEach(label => {
            const labelText = label.textContent.trim().toLowerCase();
            if (labelText.includes('crop')) label.textContent = t.crop + ": ";
            if (labelText.includes('disease')) label.textContent = t.disease + ": ";
            if (labelText.includes('confidence')) label.textContent = t.confidence + ": ";
        });

        const treatmentTitle = document.querySelectorAll('.card h2')[1];
        if (treatmentTitle) treatmentTitle.textContent = t.treatment;

        const imageTitle = document.querySelectorAll('.card h2')[2];
        if (imageTitle) imageTitle.textContent = t.uploadedImage;

        document.querySelector('label[for="category"]').textContent = t.selectCrop;
        document.querySelector('label[for="file"]').textContent = t.uploadLeaf;
        document.querySelector('button[type="submit"]').textContent = t.predictButton;
    }

    // === Handle Language Dropdown Toggle ===
    langBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        langDropdown.style.display = langDropdown.style.display === 'flex' ? 'none' : 'flex';
    });

    // === Hide dropdown on outside click ===
    document.addEventListener('click', () => {
        langDropdown.style.display = 'none';
    });

    // === Handle Language Change Without Reload ===
    langOptions.forEach(btn => {
        btn.addEventListener('click', () => {
            const selectedLang = btn.getAttribute('data-lang');
            localStorage.setItem('language', selectedLang);
            langBtn.textContent = btn.textContent;
            applyTranslations(selectedLang);
        });
    });

    // === Apply Saved Language on Load ===
    const savedLang = localStorage.getItem('language') || 'en';
    const savedBtn = [...langOptions].find(btn => btn.getAttribute('data-lang') === savedLang);
    if (savedBtn) {
        langBtn.textContent = savedBtn.textContent;
        applyTranslations(savedLang);
    }
});