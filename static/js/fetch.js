
function fetchAPI(options = {
    url: '',
    requestInit: undefined,
    onSuccess: undefined,
    onError: undefined
}) {
    fetch(options.url,options.requestInit)
    .then(async (response) => {
        if (!response.ok) throw {
            status: response.status,
            statusText : response.statusText
        }
        
        let type = response.headers.get('content-type')
        let obj = {
            html: null,
            json: null,
            blob: null
        }
        if (type.startsWith('text/html')) {
            obj.html = await response.text()
        }
        else if (type.startsWith('application/json')){
            obj.json = await response.json()
        }
        else if (type.startsWith('image/')){
            obj.blob = await response.blob()
        }
        return obj
    })
    .then(({html, json, blob} )=> {
        if (html){
            options.onSuccess(html)
        }
        if (json){
            options.onSuccess(json)
        }
        if (blob){
            options.onSuccess(blob)
        }
    })
    .catch(options.onError)
}