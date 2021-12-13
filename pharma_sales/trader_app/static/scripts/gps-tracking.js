document.addEventListener("DOMContentLoaded", function () {
    const adress = "http://google.pl";

    // function apiUpdateLocation (args) {
    //     fetch(adress).then( resp => {
    //         return resp.json();
    //     }).then( obj => {
    //         //obj jest obiektem lub
    //     }).catch(function (error) {
    //         console.log('ERROR:', error)
    //     });
    // }


    if (window.location.pathname == '/trader/start_day/') {

        console.log('działa w gpstracking');
        navigator.geolocation.getCurrentPosition(data => {
            document.cookie = "lat=" + data.coords.latitude
            document.cookie = "long=" + data.coords.longitude
            console.log(data.coords.longitude)
        }, (error) => console.log(error)
        );
    }
    if (window.location.pathname.match(/\/trader\/visit\//)) {

        console.log('działa w gpstracking');
        navigator.geolocation.getCurrentPosition(data => {
            document.cookie = "lat=" + data.coords.latitude
            document.cookie = "long=" + data.coords.longitude
            console.log(data.coords.longitude)
        }, (error) => console.log(error)
        );
    }
    
});