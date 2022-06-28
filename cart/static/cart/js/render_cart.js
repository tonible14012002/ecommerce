var updateAddBtn = (addBtns) => addBtns.forEach((btn) => {
        btn.onclick = (e) => {
            e.preventDefault()
            let formData = new FormData()
            formData.append('quantity', '1')
            formData.append('update', 'false')
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
                onSuccess: (data) => {
                    if (data.status == 'ok'){
                        toast({
                            containerSelector: '#toast',
                            title: 'Added',
                            body: 'product was added to your cart',
                            type: 'success',
                            duration: 4000
                        })
                        renderCart(cart, btn.dataset.cartUrl)
                    }
                    else {
                        toastErrors(data.errors)
                    }
                },
                onError: (error) => {
                    toast({
                        containerSelector: '#toast',
                        title: error.status || 'error',
                        body: error.statusText || error,
                        type: 'error',
                        duration: 4000
                    })
                }
            })
        }
})

var updateRemoveBtn = (removeBtns) => removeBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        e.preventDefault()
        fetchAPI({
            url:  btn.href,
            requestInit: {
                method: 'POST',
                headers: {
                    'X-CSRFtoken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                origin: 'same-origin',
            },
            onSuccess: (data) => {
                btn.closest('.cart-item').remove() 
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
    })
})

function renderCart(cart, url) {
    fetchAPI({
        url: url,
        requestInit: {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
        },
        onSuccess: (data) => {
            if (data) {
                cart.innerHTML = ""
                cart.insertAdjacentHTML("beforeend",data)
                var cartRemoveBtns = [...document.getElementsByClassName('remove-btn')]
                updateRemoveBtn(cartRemoveBtns)
            }
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
}

