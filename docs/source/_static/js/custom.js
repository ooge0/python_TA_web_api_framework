document.addEventListener('DOMContentLoaded', function () {
    const toggles = document.querySelectorAll('.admonition.toggle');

    toggles.forEach(function (toggle) {
        const title = toggle.querySelector('.admonition-title');
        const content = toggle.querySelector('.literal-block-wrapper');

        // Initially collapse the content
        content.style.display = 'none';

        // Toggle content display when the title is clicked
        title.addEventListener('click', function () {
            if (content.style.display === 'none') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
    });
});
