document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed!");

    document.querySelectorAll('.calendar-position').forEach(calendar => {
        calendar.style.display = 'flex'
        calendar.querySelectorAll('.calendar-element').forEach(div =>{
            div.style.minWidth = '100px'
       
            calendar.querySelectorAll('textarea').forEach(element => {
                element.style.maxWidth = '100%'
                element.style.minWidth = '50%'
                element.style.maxHeight = '10%'
                element.style.minHeight = '1%'
            });
        })
    
    });
});