document.getElementById('mic').addEventListener('click', async function() {
    const mic = document.getElementById('mic');
    const shadow = document.getElementById("mic-shadow");

    // Toggle the 'animate' class on click
    mic.classList.toggle('animate');

    // Apply or remove the shadow class accordingly
    if (mic.classList.contains('animate')) {
        shadow.classList.add("mic-shadow");

        // Start recording
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            let audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                const formData = new FormData();
                formData.append('audio', audioBlob, 'recording.webm');

                try {
                    await fetch('/api/speech-to-text', {
                        method: 'POST',
                        body: formData,
                    });
                } catch (error) {
                    console.error('Error:', error);
                }
                // Clear the chunks after processing
                audioChunks = [];
            };

            mediaRecorder.start();
            // Stop recording after a fixed time or when the mic is clicked again
            mic.addEventListener('click', function stopRecording() {
                if (mediaRecorder.state !== "inactive") {
                    mediaRecorder.stop();
                    mic.removeEventListener('click', stopRecording);
                }
                shadow.classList.remove("mic-shadow");
            });
        } else {
            console.error('Your browser does not support audio recording.');
        }
    } else {
        // Stop recording if the mic is clicked again
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
        }
    }
});
