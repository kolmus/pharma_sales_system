document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname == '/trader/') {
        console.log('działa');
        
        document.querySelectorAll('button.btn').forEach(element => {
            console.log(element);
            element.style.maxWidth = "100%"
            element.style.minWidth = "100%"
            element.style.minHeight = '130px'
            element.style.fontSize = '200%'
        })
    }
});