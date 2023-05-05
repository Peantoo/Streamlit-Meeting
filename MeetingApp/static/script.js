let audioContext = new AudioContext();
let analyser = audioContext.createAnalyser();
let microphoneStream;

function visualize(stream) {
    microphoneStream = audioContext.createMediaStreamSource(stream);
    microphoneStream.connect(analyser);
    visualizeVolume();
}

function visualizeVolume() {
    let volumeBar = document.getElementById('volume-bar');
    analyser.fftSize = 256;
    let bufferLength = analyser.frequencyBinCount;
    let dataArray = new Uint8Array(bufferLength);

    function draw() {
        requestAnimationFrame(draw);
        analyser.getByteFrequencyData(dataArray);

        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
            sum += dataArray[i];
        }

        let averageVolume = sum / bufferLength;
        volumeBar.style.height = averageVolume + 'px';
    }

    draw();
}
