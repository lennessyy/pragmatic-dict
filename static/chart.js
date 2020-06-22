
// Load the Visualization API and the piechart package.
google.charts.load('current', { 'packages': ['corechart'] });

// Set a callback to run when the Google Visualization API is loaded.
// google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table, 
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Slices');
    data.addRows([
        ['Mushrooms', 3],
        ['Onions', 1],
        ['Olives', 1],
        ['Zucchini', 1],
        ['Pepperoni', 2]
    ]);

    // Set chart options
    var options = {
        'title': 'How Much Pizza I Ate Last Night',
        'width': 500,
        'height': 500,
        animation: {
            "startup": true,
            duration: 1000,
            easing: 'out',
        },
    };

    // Instantiate and draw our chart, passing in some options.
    const chart = new google.visualization.ColumnChart(document.getElementById('corpus-data'));
    chart.draw(data, options);
}

function collectGramrels(gramrels) {
    $('#gramrels').empty()
    const collected_gramrels = []
    for (let gramrel of gramrels.data) {
        if (gramrel.name == 'usage patterns' || gramrel.count == 0) {
            continue
        }
        collected_gramrels.push({ name: gramrel.name, count: gramrel.count })
    }
    console.log(collected_gramrels)
    let i = 0
    for (let gramrel of collected_gramrels) {
        $(`<button type="button" id=${i} class="btn btn-secondary">${gramrel.name}</button>`).appendTo($('#gramrels'))
        $(`#${i}`).on('click', function () {
            createCorpusDataView(globalGramrels, this.id)
        })
        i++;
        if (i > 4) {
            break
        }
    }
    return collected_gramrels
}

async function createCorpusDataView(gramrels, gramrelIdx = 1) {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Word')
    data.addColumn('number', 'Count')

    for (let word of gramrels.data[gramrelIdx].Words) {
        data.addRow([word.word, word.count])
        if (data.hg.length > 4) {
            break
        }
    }

    const options = {
        'title': 'Gramrels and counts',
        'width': 500,
        'height': 500,
        animation: {
            "startup": true,
            duration: 1000,
            easing: 'out',
        },
    };

    const chart = new google.visualization.ColumnChart(document.getElementById('corpus-data'));
    chart.draw(data, options);
}