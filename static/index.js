let globalGramrels = {}
$('#s-button').on({
    click: function () {
        handleClick();
        $('#note').val('Notes to make on the search')
    }
})

$('#search-word').on('keyup', function (evt) {
    if (evt.key !== 'Enter') {
        return
    }
    handleClick()
    $('#note').val('Notes to make on the search')
})

$('#note-btn').on('click', function (evt) {
    evt.preventDefault()
    axios.post(`/${this.dataset.uid}/notes`, {
        word: $('#search-word').val(),
        pos: $("input[name='pos']:checked").val(),
        user_id: Number(this.dataset.uid),
        note: $('#note').val()
    }).then(response => {
        console.log(response)
        alert(response.data)
    })
})

function hideAll() {
    $('h3').empty()
    $('#definitions').empty()
}

async function handleClick() {
    hideAll()
    const word = $('input').val().toLowerCase()
    const pos = $("input[name='pos']:checked").val();
    createDefinitionView(word)
    let gramrels;
    try { gramrels = await axios.post(`/api/sketchengine/${word}/${pos}`) }
    catch (e) {
        console.log(e)
        $('#corpus-data').empty()
        $('<img style="margin-top: 3em;" src="/static/error_img.png">').appendTo('#corpus-data')
    } finally {
        await widget.fetch(word, 'English')
        $('#show-word').text(word)
        $('#note-form').show()
        $('#dict-view').slideDown()
        $('#player').slideDown()
    }
    if (!gramrels) {
        return
    }
    createCorpusDataView(gramrels)
    collectGramrels(gramrels)
    globalGramrels = gramrels
}

async function createDefinitionView(word) {
    let resp = {};
    $('#searched-word').text(word)
    try { resp = await axios.post(`/api/dictionary/${word}`) }
    catch (e) {
        $('<p>We did not find this word in the wild this time</p>').appendTo($('#definitions'))
        console.log(e)
        return
    }

    for (let def of resp.data) {
        $(`<li>
        ${parseString(def)}
        </li>   
        `).appendTo($('#definitions'))
    }
}

//fetch data from python session if there is 
document.addEventListener('DOMContentLoaded', function () {
    if (wordToSearch) {
        $('#search-word').val(wordToSearch)
        $(`input[name='pos'][value=${pos}]`).prop("checked", true);
        handleClick()
    }
})