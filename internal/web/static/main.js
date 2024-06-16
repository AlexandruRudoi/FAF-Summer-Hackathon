document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const resultDiv = document.getElementById('result');
    const backButton = document.getElementById('backButton');
    const professions = ['Musician', 'Journalist', 'Podcaster', 'Educator', 'Interviewer', 'Vlogger'];
    const professionElement = document.getElementById('profession');
    const inputField1 = document.getElementById('url1');
        let lastValue = ''; // Track the last input value

    // Function to update the profession text with animation
    function updateProfession() {
        const currentProfession = professionElement.textContent;
        
        // Create a random index for the next profession
        let nextIndex = Math.floor(Math.random() * professions.length);
        while (professions[nextIndex] === currentProfession) {
            // Ensure the next profession is different from the current one
            nextIndex = Math.floor(Math.random() * professions.length);
        }
        const nextProfession = professions[nextIndex];
        
        // Animate the profession change (move down)
        professionElement.style.animation = 'moveDown 0.5s ease';
        setTimeout(() => {
            // Update the profession text
            professionElement.textContent = nextProfession;
            // Reset animation (move back to original position)
            professionElement.style.animation = 'none';
        }, 500); // Wait for the animation to complete (0.5s)
    }

    // Initial update
    updateProfession();

    // Update the profession text every 5 seconds
    setInterval(updateProfession, 2000);
});