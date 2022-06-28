var cartBtn = [...document.getElementsByClassName('cart-btn')]
var cartRemoveBtn = [...document.getElementsByClassName('remove-btn')]
updateRemoveBtn(cartRemoveBtn)

cartBtn.forEach((btn) => {
    btn.onclick = (e) => {
        e.preventDefault()
        var form = btn.closest('form')
        form.classList.toggle('form-disabled')

        var inputElement = form.querySelector('input')
    
        var formData = new FormData()
        if (btn.dataset.action == "add"){
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
                    if (inputElement.value <= 0)
                        btn.closest('.cart-item').remove()
                    else
                        btn.parentNode.querySelector('input[type=number]')[step]()
                        let priceElement = btn.closest('.cart-item').querySelector('.price')
                        priceElement.innerText = `$ ${(Number(priceElement.dataset.price) * Number(inputElement.value)).toFixed(3)}`
                }
                else if (inputElement.value == '1'){
                    toast({
                        containerSelector: '#toast',
                        title: 'Add failed',
                        body: 'item quantity must be above 1',
                        type: 'alert',
                        duration: 4000
                    })
                }
                else if (inputElement.value == '21'){
                    toast({
                        containerSelector: '#toast',
                        title: 'Add failed',
                        body: 'item quantity must be below 21',
                        type: 'alert',
                        duration: 4000
                    })
                }
                form.classList.toggle('form-disabled')
            }
        })
    }
})
