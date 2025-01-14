function updateData() {
    $.get('/api/data', function(data) { //this is the AJAX request to the api/data endpoint on the server
                                        // function(data) is an anonymus function (callback function) that takes arg data. this is passed to the get function
                                        // the $.get makes a HTTP GET request to the /api/data endpoint on the server
                                        // the data param contains the response from the server

        //console.log(data)
        // Clear existing table rows
        $('#sensor-data tbody').empty(); // clears all the rows from <tbody> of the table with ID sensor-dataS

        // Populate the table with new data
        data.forEach(function(row) {
            $('#sensor-data tbody').append(`
                <tr>
                    <td>${row[9]}</td>
                    <td>${row[1]}</td>
                    <td>${row[2]}</td>
                    <td>${row[3]}</td>
                    <td>${row[4]}</td>
                    <td>${row[5]}</td>
                    <td>${row[6]}</td>
                    <td>${row[7]}</td>
                    <td>${row[8]}</td>
                </tr>
            `);
        });
    });
}

// Update the data every 30 seconds (30000ms) how often the data is uploaded to the db
setInterval(updateData, 30000);

// Call the function immediately to load data when the page is loaded
updateData();
