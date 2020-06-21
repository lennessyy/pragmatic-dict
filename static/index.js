$('button').on('click', handleClick)

function hideAll() {
    $('h3').empty()
    $('#definitions').empty()
}

async function handleClick() {
    hideAll()
    const word = $('input').val()
    createDefinitionView(word)
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