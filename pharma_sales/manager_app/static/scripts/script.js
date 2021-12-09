//Script makes button to import adress from http://kodpocztowy.intami.pl
//Available on '/branch/add/' and on '/branch/edit/<id>/'

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed!");
    const select_div = document.querySelector('#select')
    select_div.style.display = 'none'
    const reg = /\/branch\/edit\/\d+\//;

    if (Boolean(window.location.pathname.match(reg))) {
        const form = document.querySelector('fieldset')
        const zip_code = form.querySelector('#id_zip_code')

        let import_button = document.createElement('button')
        import_button.innerText = 'Pobierz adres'
        import_button.setAttribute('type', 'button')
        import_button.style.display = 'block'
        zip_code.parentElement.insertBefore(import_button, zip_code.nextElementSibling)

        zip_code.addEventListener('keyup', function(event) {
            let reg2 = /\d{2}-\d{3}/g
            if (zip_code.value.match(reg2)) {
                import_button.addEventListener('click', function(event) {
                    const adress = "http://kodpocztowy.intami.pl/api/" + zip_code.value
                    fetch(adress).then( resp => {
                        return resp.json();
                    }).then( obj => {
                        if(obj.length > 1){
                            // this block is for miltiple objects

                            document.querySelector('#id_province').value = obj[0]['wojewodztwo']
                            let city = document.querySelector('#id_city')
                            let street = document.querySelector('#id_street')
                            select_div.style.display = 'block'
                            let legend = select_div.querySelector('legend')
                            city.value = obj[0]['miejscowosc']
                            
                            
                            if (obj.length < 10) {
                                // this block is for small listst
                                obj.foreach(element => {                   // <= problem
                                    if (element['miejscowosc'] != obj[0]['miejscowosc]']) {
                                        // if difrent cities

                                        city.value = ""
                                        legend.innerText = "Wybierz poprawną miejscowość:"

                                        let divOff = document.createElement('div')
                                        select_div.appendChild(divOff)

                                        let new_city = document.createElement('button')
                                        new_city.type = 'button'
                                        new_city.innerText = element['miejscowosc']
                                        
                                        divOff.appendChild(new_city)
                                        new_city.addEventListener('click', function(event) {
                                            city.value = event.target.innerText
                                            divOff.remove()
                                        })

                                    }
                                    if (element['miejscowosc'] == city.value) {
                                        // if less than 10 objects

                                        let divOff = document.createElement('div')
                                        select_div.appendChild(divOff)
                                            
                                        street.value = ""
                                        legend.innertext = "Wybierz odpowiednią ulicę"

                                        let new_street = document.createElement('button')
                                        new_street.type = 'button'
                                        new_street.innerText = element['ulica']
                                        divOff.appendChild(new_street)
                                        
                                        new_street.addEventListener('click', function(event) {
                                            city.value = event.target.innerText
                                            select_div.style.display = 'none'
                                            divOff.remove()
                                        })
                                        
                                    }
                                });
                            } else {
                                //more than 10 objects
                                legend.innerText = 'Zbyt wiele ulic do wyboru. Wpisz ulicę ręcznie'
                            }
                        } else if (obj.length == 1) {
                            // exacly 1 object

                            let result = obj[0]
                            document.querySelector('#id_city').value = result['miejscowosc']
                            document.querySelector('#id_street').value = result['ulica']
                            document.querySelector('#id_province').value = result['wojewodztwo']

                        } else {
                            // No objects

                            zip_code.style.background = 'red'
                        }
                    }).catch(function (error) {
                        // error 
                        zip_code.style.background = 'red'
                        console.log('ERROR:', error)
                    });
                })
            }
        })
    }



});


// Example response:
// 
// 
// [
//     {
//         "kod": "01-111",
//         "nazwa": "Zakład XYZ",
//         "miejscowosc": "Warszawa",
//         "ulica": "Jana Olbrachta",
//         "gmina": "Warszawa",
//         "powiat": "Warszawa",
//         "wojewodztwo": "mazowieckie",
//         "dzielnica": "Wola",
//         "numeracja": [
//         {
//             "od": "1",
//             "do": "9b",
//             "parzystosc": "NIEPARZYSTE"
//         }
//         ]
//     }
// ]