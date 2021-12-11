//Script makes button to import adress from http://kodpocztowy.intami.pl
//Available on '/branch/add/' and on '/branch/edit/<id>/'

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed!");
    document.querySelector('#user').style.color = "black"

    const reg = /\/branch\/edit\/\d+\//;

    if (Boolean(window.location.pathname.match(reg))) {
        const form = document.querySelector('fieldset')
        const zip_code = form.querySelector('#id_zip_code')

        const buttons_div = document.createElement('div')
        buttons_div.id = 'select'
        buttons_div.style.display = 'none';
        form.insertBefore(buttons_div, zip_code)
    
        let import_button = document.createElement('button')
        import_button.innerText = 'Pobierz adres'
        import_button.setAttribute('type', 'button')
        import_button.style.display = 'none'
        form.insertBefore(import_button, zip_code.nextElementSibling)
        const legend = document.createElement('legend')
        buttons_div.appendChild(legend)

        // this change backround on input tags on chages
        document.querySelectorAll('input').forEach(element => {
            element.addEventListener('keyup', function(event) {
                event.target.style.background = 'white'
            })
        });

        // import data by zipcode
        import_button.addEventListener('click', function(event) {
            const adress = "http://kodpocztowy.intami.pl/api/" + zip_code.value
            fetch(adress).then( resp => {
                return resp.json();
            }).then( obj => {
                console.log(obj)


                document.querySelector('#id_building_number').value = ''
                document.querySelector('#id_building_number').style.background = 'red'
                document.querySelector('#id_apartment_number').value = ''
                document.querySelector('#id_apartment_number').style.background = 'red'
                
                if(obj.length > 1){
                    // this block is for miltiple objects

                    document.querySelector('#id_province').value = obj[0]['wojewodztwo']
                    let city = document.querySelector('#id_city')
                    let street = document.querySelector('#id_street')
                    buttons_div.style.display = 'flex'
                    
                    city.value = ""
                    city.style.background = 'red'
                    street.value = ""
                    street.style.background = 'red'
                    
                    
                    if (obj.length < 10) {
                        // this block is for small listst => less than 10
                        let divOff = document.createElement('div')
                        buttons_div.appendChild(divOff)
                        for (i = 0; i < obj.length; i++) {
                            element = obj[i]
                            
                            legend.innerText = "Wybierz odpowiednią ulicę: =>"

                            let new_street = document.createElement('button')
                            new_street.type = 'button'
                            new_street.innerText = element['ulica']
                            new_street.dataset.city_name = element['miejscowosc']
                            divOff.appendChild(new_street)
                            
                            new_street.addEventListener('click', function(event) {
                                street.value = event.target.innerText
                                street.style.background = 'green'
                                city.value = event.target.dataset.city_name
                                city.style.background = 'green'
                                buttons_div.style.display = 'none'
                                
                                divOff.remove()
                            })
                        };
                    } else {
                        //more than 10 objects
                        legend.innerText = 'Zbyt wiele ulic do wyboru. Wpisz ulicę ręcznie'
                    }
                } else if (obj.length == 1) {
                    // exacly 1 object

                    let result = obj[0]
                    document.querySelector('#id_city').value = result['miejscowosc']
                    document.querySelector('#id_city').style.background = 'green'
                    document.querySelector('#id_street').value = result['ulica']
                    document.querySelector('#id_street').style.background = 'green'
                    document.querySelector('#id_province').value = result['wojewodztwo']
                    document.querySelector('#id_province').style.backgroun = 'green'

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

        //show button if zip-code is valid
        zip_code.addEventListener('keyup', function(event) {
            let reg2 = /\d{2}-\d{3}/g
            if (zip_code.value.match(reg2)) {
                import_button.style.display = 'block'
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