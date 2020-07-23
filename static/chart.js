
// Load the Visualization API and the piechart package.
google.charts.load('current', { 'packages': ['corechart'] });

// Set a callback to run when the Google Visualization API is loaded.
// google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table, 
// instantiates the pie chart, passes in the data and
// draws it.

//Function that collectes the gramrels coming back from api to update buttons
function collectGramrels(gramrels) {
    $('#gramrels').empty()
    const collected_gramrels = []
    for (let gramrel of gramrels.data) {
        collected_gramrels.push({ name: gramrel.name, count: gramrel.count })
    }
    console.log(collected_gramrels)

    //the first item in the list is 'usage pattern', which we don't want, and therefore we start the loop at i=1
    for (let i = 1; i < 6 && i < collected_gramrels.length; i++) {
        $(`<button type="button" id=${i} class="btn btn-info">${collected_gramrels[i].name}</button>`).appendTo($('#gramrels'))
        $(`#${i}`).on('click', function () {
            createCorpusDataView(globalGramrels, this.id)
        })
    }
    return collected_gramrels
}

//function to draw chart
async function createCorpusDataView(gramrels, gramrelIdx = 1) {
    const data = await prepareData(gramrels, gramrelIdx)

    const options = configOptions()

    const chart = new google.visualization.ColumnChart(document.getElementById('corpus-data'));
    chart.draw(data, options);
}

async function prepareData(gramrels, gramrelIdx) {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Word')
    data.addColumn('number', 'Count')

    const words = gramrels.data[gramrelIdx].Words.slice(1, 6)
    sortWords(words)

    //sort the results by absolute frequency
    for (let word of words) {
        data.addRow([word.word, word.count])
        if (data.fg.length > 4) {
            break
        }
    }

    // the default order is based on logDice, useful for learning collocation
    // for (let word of gramrels.data[gramrelIdx].Words) {
    //     data.addRow([word.word, word.count])
    //     if (data.hg.length > 4) {
    //         break
    //     }
    // }
    return data
}

function configOptions() {
    const options = {
        title: 'Collocations',
        width: 500,
        height: 500,
        animation: {
            startup: true,
            duration: 1000,
            easing: 'out',
        },
        backgroundColor: '#f4f6ff',
        colors: ['#4f8a8b']
    };
    return options
}

function sortWords(words) {
    function compare(word1, word2) {
        if (word1.count > word2.count) {
            return -1
        } else if (word1.count < word2.count) {
            return 1
        } else return 0
    }
    words.sort(compare)
    return words
}