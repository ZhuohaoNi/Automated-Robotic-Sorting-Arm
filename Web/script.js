const calibrateBtn = document.getElementById('calibrate-arm');
const sortAllBtn = document.getElementById('sort-all');
const sortAllResistorsBtn = document.getElementById('sort-all-resistors');
const sortAllCapacitorsBtn = document.getElementById('sort-all-capacitors');
const sortAllLedRedBtn = document.getElementById('sort-all-led-red');

calibrateBtn.addEventListener('click', () => {
  fetch('http://127.0.0.1:5000/calibrate')
    .then(response => {
      let rand = Math.random().toString(36).substring(2);
      document.getElementById("detection-viewport").src = `http://127.0.0.1:5000/calibrate?random=${rand}`;
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
});

sortAllBtn.addEventListener('click', () => {
  fetch('http://127.0.0.1:5000/sort-all') 
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
});

sortAllResistorsBtn.addEventListener('click', () => {
  fetch('http://127.0.0.1:5000/sort-all-resistors') 
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
});

sortAllCapacitorsBtn.addEventListener('click', () => {
  fetch('http://127.0.0.1:5000/sort-all-capacitors') 
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
});

sortAllLedRedBtn.addEventListener('click', () => {
  fetch('http://127.0.0.1:5000/sort-all-led-red') 
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
});
