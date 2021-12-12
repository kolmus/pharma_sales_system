document.addEventListener("DOMContentLoaded", function () {
    
    if (window.location.pathname == '/') {
        let lastWeekDiv = document.querySelector('div.last-week')
        lastWeekDiv.style.display = 'none';

        let thisWeekDiv = document.querySelector('div.this-week')
        thisWeekDiv.style.display = 'flex';

        let nextWeekDiv = document.querySelector('div.next-week')
        nextWeekDiv.style.display = 'none';
        
        document.querySelectorAll('.calendar-element').forEach(div =>{
            div.style.minWidth = '100px';
        })

        document.querySelectorAll('textarea').forEach(element => {
            element.style.maxWidth = '100%';
            element.style.minWidth = '50%';
            element.style.maxHeight = '10%';
            element.style.minHeight = '1%';
        });

        // this part colors borders on current day if shown
        let thisWeekForms= document.querySelector('div.this-week').querySelectorAll('form');
        thisWeekForms.forEach(element => {
            today = new Date().toISOString().slice(0, 10)
            if (element.parentElement.dataset.tdate.split(' ')[0] == today) {
                element.style.border = '.2rem solid white'
            }

        })


        document.querySelector('#last-week-button').addEventListener('click', function(event) {
            lastWeekDiv.style.display = 'flex';
            thisWeekDiv.style.display = 'none';
            nextWeekDiv.style.display = 'none';
        })
        
        document.querySelector('#this-week-button').addEventListener('click', function(event) {
            lastWeekDiv.style.display = 'none';
            thisWeekDiv.style.display = 'flex';
            nextWeekDiv.style.display = 'none';
        })

        document.querySelector('#next-week-button').addEventListener('click', function(event) {
            lastWeekDiv.style.display = 'none';
            thisWeekDiv.style.display = 'none';
            nextWeekDiv.style.display = 'flex';
        })
    }
});