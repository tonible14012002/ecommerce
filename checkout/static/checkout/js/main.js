var cartBtn = [...document.getElementsByClassName('cart-btn')]
var cartRemoveBtn = [...document.getElementsByClassName('remove-btn')]
updateRemoveBtn(cartRemoveBtn)

cartBtn.forEach((btn) => {
    btn.onclick = (e) => {
        e.preventDefault()
        // disable btn while fetch api
        var item = btn.closest('.cart-item')
        item.classList.add('disabled')

        var inputElement = item.querySelector('input')
    
        var formData = new FormData()
        var action = btn.dataset.action

        if (action == "add"){
            var step = "stepUp"
            formData.append('quantity', String(Number(inputElement.value)+1))
        }
        else {
            var step = "stepDown" 
            formData.append('quantity', String(Number(inputElement.value)-1))
        }
        formData.append('update', 'true')

        fetchAPI({
            url:  btn.href,
            requestInit: {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFtoken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                origin: 'same-origin',
            },
            onSuccess: (data)=>{
                if(data.status == 'ok'){
                    inputElement = btn.parentNode.querySelector('input[type=number]')
            
                    btn.parentNode.querySelector('input[type=number]')[step]()
                    if (inputElement.value == 0)
                        item.remove()
                    else {
                        let priceElement = btn.closest('.cart-item').querySelector('.price')
                        priceElement.innerText = `$ ${(Number(priceElement.dataset.price) * Number(inputElement.value)).toFixed(3)}`                        
                    }
                }
                else {
                    toastErrors(data.errors)
                }
                item.classList.remove('disabled')
            },
            onError: (error) => {
                toast({
                    containerSelector: '#toast',
                    title: error.status || 'error',
                    body: error.statusText || error,
                    type: 'error',
                    duration: 5000
                })
            }
        })
        // enable btn
    }
})

