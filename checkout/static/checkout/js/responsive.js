var pageContainer = document.getElementById('order-container')
var form = pageContainer.querySelector('.form')

if (window.innerWidth <= 900){
    form.classList.add('response')
    pageContainer.classList.add('response')
}
else {
    form.classList.remove('response')
    pageContainer.classList.remove('response')
}

window.onresize = (e)=>{
    if (e.target.innerWidth <= 900){
        form.classList.add('response')
        pageContainer.classList.add('response')
    }
    else {
        form.classList.remove('response')
        pageContainer.classList.remove('response')
    }
}