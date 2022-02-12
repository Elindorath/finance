const sensors = {
  [sensorId.movingAverage]: () => {

  },
  [sensorId.RSI]: () => {
    return (H * 100) / (H + B);
  },
};

function getSensorValue(sensorId) {

}
