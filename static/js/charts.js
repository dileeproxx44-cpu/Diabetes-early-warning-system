const ctx = document.getElementById('riskChart');

new Chart(ctx, {

    type: 'pie',

    data: {

        labels: [

            'High Risk',
            'Low Risk'

        ],

        datasets: [{

            data: [

                highRisk,
                lowRisk

            ],

            backgroundColor: [

                'red',
                'green'

            ],

            borderWidth: 2

        }]

    },

    options: {

        responsive: true

    }

});