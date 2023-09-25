import * as Plotly from 'plotly.js';

document.getElementById("submit").addEventListener("click", process_input);

function success() {
    var data = JSON.parse(this.responseText);
    update_image(data['sentiment'])
    update_plot(data['probabilities'])
}

function error(err) {
    console.log('Request Failed', err); 
}

var xhr = new XMLHttpRequest(); 
xhr.onload = success; 
xhr.onerror = error;  


function process_input() {
    var user_input = document.getElementById('user_input').value;
    xhr.open('POST', "http://127.0.0.1:8000/predict");
    xhr.send(JSON.stringify({'text': user_input}));
}

function update_plot(predicted_data){
    var layout = {  margin: {l: 25, r: 20, b: 25, t: 25, pad: 5 },
                    title: 'Probabilities',
                    font:{ family: 'Raleway, sans-serif'},
                }

    var data = [{predicted_data,
            x: Object.keys(predicted_data),
            y: Object.values(predicted_data),
            marker:{
                color: 'rgba(158,202,225,.5)',
                line: {
                    color: 'rgb(8,48,107)',
                    width: 1.5
                }
            },
            type: 'bar'            
        }];
      Plotly.newPlot('myDiv', data, layout, {displayModeBar: false});
}

function update_image(sentiment){
    if (sentiment === "positive"){
        document.getElementById("imgClickAndChange").src = "assets/positive.png";
    }
    else if (sentiment === "neutral"){
        document.getElementById("imgClickAndChange").src = "assets/neutral.png";
    }
    else if (sentiment === "negative"){
        document.getElementById("imgClickAndChange").src = "assets/negative.png";
    }
}