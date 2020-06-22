let globalGramrels = {}
$('button').on('click', handleClick)

function hideAll() {
    $('h3').empty()
    $('#definitions').empty()
}

async function handleClick() {
    hideAll()
    const word = $('input').val()
    const pos = $("input[name='pos']:checked").val();
    createDefinitionView(word)
    const gramrels = await axios.post(`api/sketchengine/${word}/${pos}`)
    createCorpusDataView(gramrels)
    collectGramrels(gramrels)
    globalGramrels = gramrels
}

async function createDefinitionView(word) {
    const resp = await axios.post(`/api/dictionary/${word}`)
    $(`<h3>${word}</h3>`).insertBefore($('#definitions'))
    for (let def of resp.data) {
        $(`<li>
        ${def}
        </li>   
        `).appendTo($('#definitions'))
    }
}