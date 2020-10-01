// Some Chart Colors.

window.chartColors = {
    // Colors I added, for better contrast.
    sienna: 'rgb(160,82,45)',
    darkslategray: 'rgb(47, 79, 79)',
    seagreen: 'rgb(46, 139, 87)',
    darkred: 'rgb(139, 0, 0)',
    olive: 'rgb(128, 128, 0)',
    purple: 'rgb(127, 0, 127)',
    orangered: 'rgb(255, 69, 0)',
    orange: 'rgb(255, 165, 0)',
    yellow: 'rgb(255, 255, 0)',
    chartreuse: 'rgb(127, 255, 0)',
    mediumspringgreen: 'rgb(0, 250, 154)',
    royalblue: 'rgb(65, 105, 225)',
    aqua: 'rgb(0, 255, 255)',
    deepskyblue: 'rgb(0, 191, 255)',
    blue: 'rgb(0, 0, 255)',
    fuchsia: 'rgb(255, 0, 255)',
    khaki: 'rgb(240, 230, 140)',
    salmon: 'rgb(250, 128, 114)',
    plum: 'rgb(221, 160, 221)',
    deeppink: 'rgb(255, 20, 147)',
    // Preset Colors.
    red: 'hex(#ffa500)',
    orange2: 'rgb(255, 159, 64)',
    yellow2: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue2: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)',
    aqua2: 'rgb(0,255,255)',
    beige: 'rgb(245,245,220)',
    black: 'rgb(0,0,0)',
    lime: 'rgb((0,255,0)',
    golden: 'rgb(218,165,32)',
    orange_red: 'rgb(255,69,0)',
    navy: 'rgb(0,0,128)',
    thistle: 'rgb(216,191,216)',
    slate_grap: 'rgb(112,128,144)'
};

// Some Chart Colors --End

var colorNames = Object.keys(window.chartColors);
var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var config = {
    type: 'line',
    data: {
        labels: ['0','1','2','3','4','5','6','7','8','9','10'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: window.chartColors['deeppink'],
            borderColor: window.chartColors['deeppink'],
            data: [
            25,30,35,40
            ],
            fill: false,
        }, {
            label: 'My Second dataset',
            fill: false,
            backgroundColor: window.chartColors['green'],
            borderColor: window.chartColors['green'],
            data: [
            50,
            30,
            25,
            15,
            60
            ],
        }]
    },
    options: {
        legend: {
            display: true
        },
        responsive: true,
        title: {
            display: true,
            text: 'TrueSkill Info Line Chart'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Battles'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'TrueSkill Rating'
                }
            }]
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById('Trueskill').getContext('2d');
    window.myLine = new Chart(ctx, config);
};


var colorNames = Object.keys(window.chartColors);

document.getElementById('addData').addEventListener('click', function() {
    if (config.data.datasets.length > 0) {
        var month = MONTHS[config.data.labels.length % MONTHS.length];
        config.data.labels.push(month);

        config.data.datasets.forEach(function(dataset) {
            dataset.data.push(randomScalingFactor());
        });

        window.myLine.update();
    }
});

document.getElementById('removeData').addEventListener('click', function() {
            config.data.labels.splice(-1, 1); // remove the label first

            config.data.datasets.forEach(function(dataset) {
                dataset.data.pop();
            });

            window.myLine.update();
        });