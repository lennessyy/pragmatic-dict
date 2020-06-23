function parseString(str) {
    const regex = /\{.*\}/g
    return str.replace(regex, '').trim()
}