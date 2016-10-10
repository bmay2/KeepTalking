'use strict';

var constraints = {
  audio: true
};

function handleSuccess(stream) {
  console.log('getUserMedia() got stream: ', stream);
  window.stream = stream;
}

function handleError(error) {
  console.log('navigator.getUserMedia error: ', error);
}

navigator.mediaDevices.getUserMedia(constraints).
  then(handleSuccess).catch(handleError);

var listenLog;
function startListening() {
  var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  var microphone_stream = audioCtx.createMediaStreamSource(stream);

  var analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  microphone_stream.connect(analyser);
  
  var bufferLength = analyser.fftSize;
  var dataArray = new Uint8Array(bufferLength);
  analyser.getByteTimeDomainData(dataArray);

  function listen() {
    listenLog = requestAnimationFrame(listen);

    analyser.getByteTimeDomainData(dataArray);
    console.log(Math.max.apply(Math, dataArray));
    console.log(Math.min.apply(Math, dataArray));
  }
  listen();
}