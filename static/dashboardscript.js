function updateData() {
    $.get('/api/data/nondb', function(data) { //this is the AJAX request to the api/data endpoint on the server
                                        // function(data) is an anonymus function (callback function) that takes arg data. this is passed to the get function
                                        // the $.get makes a HTTP GET request to the /api/data endpoint on the server
                                        // the data param contains the response from the server


        if (data.length > 0) {
            var temperature = data[5]; 
            var humidity = data[4]; 
            var pm1p0 = data[0]; 
            var pm2p5 = data[1]; 
            var pm4p0 = data[2]; 
            var pm10p0 = data[3]
            var voc = data[6]; 
            var nox = data[7]; 

            

            // Update the DOM elements with the new data
            $('#Temperature').text(temperature);
            $('#Humidity').text(humidity);
            $('#pm1p0').text(pm1p0);
            $('#pm2p5').text(pm2p5);
            $('#pm4p0').text(pm4p0);
            $('#pm10p0').text(pm10p0);
            $('#voc').text(voc);
            $('#nox').text(nox);
        }
        
    });
}

// Update the data every 30 seconds (30000ms) how often the data is uploaded to the db
setInterval(updateData, 30000);

// Call the function immediately to load data when the page is loaded
updateData();
