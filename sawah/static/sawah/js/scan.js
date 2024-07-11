document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Access the user's camera
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            video.srcObject = stream;
            video.play();
        });
    }

    // Function to capture an image and send it to the server
    function captureImage() {
        context.drawImage(video, 0, 0, 640, 480);
        canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append('image', blob, 'capture.png');

            // Send the captured image to the server
            fetch(scanFaceUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Fetch Response:', data);  // Log the response data
                if (data.status === 'success') {
                    console.log('Redirecting to:', data.redirect_url);  // Log the redirect URL
                    const redirectUrl = `/sawah/scan_result/?video_url=${encodeURIComponent(data.redirect_url)}`;
                    window.location.href = redirectUrl;  // Redirect to the result view
                } else {
                    console.error('Error:', data.message);
                }
            })
            .catch((error) => {
                console.error('Fetch Error:', error);  // Log any fetch errors
            });
        }, 'image/png');
    }

    // Set an interval to continuously capture images
    setInterval(captureImage, 5000); // Capture image every 5 seconds
});
