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