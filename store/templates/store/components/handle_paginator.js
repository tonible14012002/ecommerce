var json = "{{page_info|escapejs}}"
var pageInfo = JSON.parse(json)


var btn = document.getElementById('more-products-btn')

if (!pageInfo.has_other_pages) {
    btn.remove()
}
console.log(pageInfo.q)

btn.onclick = () => {
    "{% if category_slug %}"
        var url = `{% url 'store:more_products_by_category' category_slug %}?q=${pageInfo.q}&page=${pageInfo.current_page + 1}`
    "{% else %}"
        var url = `{% url 'store:more_products' %}?q=${pageInfo.q}&page=${pageInfo.current_page + 1}`
    "{% endif %}"
    var productList = document.getElementById('products-list')
    productsSection.classList.add('disabled')

    fetchAPI({
        url: url,
        requestInit: {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        },
        onSuccess: (data) => {
            if (data.html == ''){
                toast({
                    containerSelector: '#toast',
                    title: 'Error',
                    body: 'Load products error, try request again',
                    type: 'error',
                    duration: 5000     
                })
            }
            else {
                productList.insertAdjacentHTML("beforeend", data.html) 
                var addBtns = [...document.getElementsByClassName('add-product-btn')]
                updateAddBtn(addBtns)
                var script = document.createElement('script')
                script.innerHTML = data.script
                document.body.appendChild(script)

                pageInfo = data.page_info
                console.log(pageInfo)
                if (!pageInfo.has_next)
                    btn.remove()
            }
            productsSection.classList.remove('disabled')
        },
        onError: (error) => {
            toast({
                containerSelector: '#toast',
                title: error.status || 'error',
                body: error.statusText || error,
                type: 'error',
                duration: 5000
            })
            productsSection.classList.remove('disabled')
        }
    })
}