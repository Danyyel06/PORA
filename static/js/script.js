document.addEventListener('DOMContentLoaded', () => {
    const speakerItems = document.querySelectorAll('.speaker-item');
    const speakerPhotos = document.querySelectorAll('.speaker-photo');
    const defaultPhoto = document.getElementById('default-speaker-photo');

    // Function to show a specific photo and hide others
    function showPhoto(photoId) {
        speakerPhotos.forEach(photo => {
            photo.classList.remove('active-photo'); // Hide all photos
        });
        const targetPhoto = document.getElementById(photoId);
        if (targetPhoto) {
            targetPhoto.classList.add('active-photo'); // Show the target photo
        }
    }

    // Add event listeners to each speaker name
    speakerItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const speakerId = item.dataset.speakerId; // Get the ID from data-speaker-id
            showPhoto(`${speakerId}-photo`); // Construct the ID of the image to show
        });

        item.addEventListener('mouseleave', () => {
            // When mouse leaves, revert to default photo
            showPhoto('default-speaker-photo');
        });
    });

    // Ensure default photo is shown on initial load
    showPhoto('default-speaker-photo');
});
