$(document).ready(function() {
    var score = $('#scoreHolder').data('score');
    var topic = $('#topicHolder').data('topic');
    var time = $('#timeHolder').data('time');
    var typeSelector = $('#typeSelector');
    var resultsGrid = $('#resultsGrid');
    

    // Example categories, replace or dynamically fetch these as needed
    var categories = ['all', 'Workshop', 'E-Learning', 'Guide'];
    $.each(categories, function(index, category) {
        typeSelector.append($('<option>', {
            value: category,
            text: category
        }));
    });
    getResults(score, topic, time, resultsGrid);
    //initial check based on quiz
    

//checking the fot type
    typeSelector.change(function() {
        var selectedType = $(this).val();
        console.log('Selected type:', selectedType);


    });
    // slider for time
    $('#timeSlider').on('mouseup', function() {
        $('#timeValue').text($(this).val());
        // Call a function to update the e-learning display based on the new slider value
        //console.log("final value: " + $(this).val());
        time = $(this).val();
        $('#timeHolder').attr('data-time', time);
        getResults(score, topic, time, resultsGrid);
        //console.log($(this).val());
    });
    // Checkbox for topics
    $('input[type="checkbox"]').on('change', function() {
        let selectedTopics = getSelectedTopics();
        console.log('Selected topics:', selectedTopics);
        $('#topicHolder').attr('data-topic', selectedTopics.join(','));

        // Assuming score and time variables are defined elsewhere in your code
        getResults(score, selectedTopics, time, resultsGrid);
    });
});
function generateStars(niveau) {
    var stars = '';
    for(var i = 0; i < niveau; i++) {
        stars += '★'; // Unicode character for a black star
    }
    return stars.length > 0 ? stars : 'No rating'; // Return stars or a default message
}
// Function to get all selected topics
function getSelectedTopics() {
    let selectedTopics = [];
    $('input[type="checkbox"]:checked').each(function() {
        selectedTopics.push($(this).val());
    });
    return selectedTopics;
}
function getResults(score, topic, time, resultsGrid) {
    topic = getSelectedTopics();
    console.log('Getting results...');
    $.ajax({
        url: `/data?score=${score}&topic=${topic}&time=${time}`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            resultsGrid.empty(); // Clear previous results
            //showing status msg
            if (data.status && data.status !== '') {
                $('#alert-message').text(data.status).show();  // Update text and show the alert message div
            } else {
                $('#alert-message').hide();  // Hide the alert if no status message
            }
            //showing results
            $.each(data.data, function(index, item) {
                if (index <6){
                    var stars = generateStars(item.Niveau);
                    var colDiv = $('<div class="col-md-4 mb-4">').html(
                        `<div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${item.Titel} - ${stars}</h5>
                                <p class="card-text">
                                    <button class="btn btn-sm btn-outline-secondary" disabled>${item.Onderwerp}</button>
                                    <button class="btn btn-sm btn-outline-primary" disabled>${item.Type}</button>
                                </p>
                                <p class="card-text"><strong>Tijdsinvestering:</strong> ${item.Tijdsinvestering}</p>
                                <p class="card-text"><strong>Taal:</strong> ${item.Taal}</p>
                                <p class="card-text"><strong>Aanbieder:</strong> ${item.Organisatie}</p>
                                <p class="card-text"><strong>Beschrijving:</strong>${item.Beschrijving}</p>
                                <a href="${item.Link}" target="_blank" class="btn btn-primary">Bekijk cursus</a>
                            </div>
                        </div>`
                    );
                    resultsGrid.append(colDiv);
                }
                else {
                    return false;  // Stop the loop after six iterations
                }
            });
        },
        error: function(xhr, status, error) {
            console.error('Error fetching data:', error);
        }
    });
}
