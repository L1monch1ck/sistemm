function addOption() {
    const optionsDiv = document.getElementById('options');
    const newOption = document.createElement('input');
    newOption.type = 'text';
    newOption.name = 'options';
    newOption.placeholder = `Вариант ${optionsDiv.children.length + 1}`;
    newOption.className = 'mb-3';
    optionsDiv.appendChild(newOption);
}

document.getElementById('voteForm')?.addEventListener('submit', (e) => {
    const selected = document.querySelector('input[name="option"]:checked');
    if (!selected) {
        e.preventDefault();
        alert('Пожалуйста, выберите вариант!');
    } else {
        setTimeout(() => {
            e.target.submit();
        }, 500);
    }
});

document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const href = link.getAttribute('href');
        setTimeout(() => {
            window.location.href = href;
        }, 500);
    });
});

