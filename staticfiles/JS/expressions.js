// Get references to the avatar image and camera button elements
const avatarImage = document.getElementById('avatar-image');
const cameraButton = document.querySelector('.camera-button');
const imageInput = document.getElementById('file-input');
const imageDataInput = document.querySelector('#image-data');

// Add a click event listener to the camera button
cameraButton.addEventListener('click', async () => {
  // Create the overlay webcam element
  const webcamOverlay = document.createElement('div');
  webcamOverlay.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.8); z-index: 9999;';

  // Create the webcam video element
  const video = document.createElement('video');
  video.style = 'position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);border-radius: 5px;'
  video.autoplay = true;

  // Access the user's camera and stream the video to the video element
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;

  // Create the button to take a picture
  const takePictureButton = document.createElement('button');
  takePictureButton.style = 'position: absolute; bottom: 5rem; left: 50%; transform: translateX(-50%); padding: 1rem 4rem; background-color: orange; color: #fff; border: none; border-radius: 0; font-size: 1rem;font-weight:900; cursor: pointer;border-radius: 50px;';
  takePictureButton.textContent = 'Take Picture';

  // Create the close button for the webcam overlay
  const closeButton = document.createElement('button');
  closeButton.style = 'position: absolute; top: 10px; right: 10px; background-color: transparent; color: #fff; border: none; font-size: 2.5rem; cursor: pointer;';
  closeButton.innerHTML = '&times;'; // Use an "X" symbol as the close button

  // Add a click event listener to the close button
  closeButton.addEventListener('click', () => {
    // Stop the video stream and remove the webcam overlay and elements
    stream.getTracks().forEach(track => track.stop());
    webcamOverlay.remove();
    video.remove();
    takePictureButton.remove();
    closeButton.remove();
  });

  // Add the close button to the webcam overlay
  webcamOverlay.appendChild(closeButton);


  // Add a click event listener to the take picture button
  takePictureButton.addEventListener('click', () => {
    // Create a canvas element to capture the picture
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 800;
   
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Stop the video stream and remove the webcam overlay and elements
    stream.getTracks().forEach(track => track.stop());
    webcamOverlay.remove();
    video.remove();
    takePictureButton.remove();

    // Set the avatar image source to the captured picture
    avatarImage.src = canvas.toDataURL('image/png');

    // Set the image input value to the captured picture path
    const imageSrc = canvas.toDataURL('image/png');
    imageDataInput.value = imageSrc;
  });


  // Add the video and button elements to the webcam overlay
  webcamOverlay.appendChild(video);
  webcamOverlay.appendChild(takePictureButton);

  // Add the webcam overlay to the page
  document.body.appendChild(webcamOverlay);
});

// Add a change event listener to the file input element
imageInput.addEventListener('change', () => {
  // Set the avatar image source to the selected file
  avatarImage.src = URL.createObjectURL(imageInput.files[0]);
});

// Add drag and drop functionality to the avatar wrapper element
const avatarWrapper = document.getElementById('avatar-wrapper');
avatarWrapper.addEventListener('dragover', e => {
  e.preventDefault();
  avatarWrapper.classList.add('dragover');
});
avatarWrapper.addEventListener('dragleave', () => {
  avatarWrapper.classList.remove('dragover');
});
avatarWrapper.addEventListener('drop', e => {
  e.preventDefault();
  avatarWrapper.classList.remove('dragover');

  // Set the avatar image source to the dropped file
  avatarImage.src = URL.createObjectURL(e.dataTransfer.files[0]);

  // Set the image input value to the dropped file path
  imageInput.value = avatarImage.src;
});
