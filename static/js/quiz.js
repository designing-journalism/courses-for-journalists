$(document).ready(function() {
    let currentQuestion = 0;
    let totalScore = 0; // Keeps track of the total score
    let selectedTopic = ''; // To store the selected topic

    function loadQuestion() {
        $.getJSON(`/quiz/question/${currentQuestion}`, function(question) {
            // Check if the question is not found or we've reached the end of the quiz
            if (question.error || !question.question) {
                // Submit the quiz if there are no more questions
                submitQuiz();
                return;
            }

            // Display the question and answers
            $('#quiz-container').empty().append(`<div><h4>${question.question}</h4></div>`);
            const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; // For labeling answers
            question.answers.forEach((answer, index) => {
                let answerLabel = alphabet[index];
                let btn;
                if (answer.score !== undefined) {
                    btn = $(`<div class="mb-2">
                    <button class="btn btn-primary mb-2 answer-btn" data-score="${answer.score}">${answerLabel}</button>
                    <span class="ml-2">${answer.text}</span>
                    </div>`);
                } else if (answer.topic !== undefined) {
                    btn = $(`<div class="mb-2">
                    <button class="btn btn-primary mb-2 answer-btn" data-topic="${answer.topic}">${answerLabel}</button>
                    <span class="ml-2">${answer.text}</span>
                    </div>`);
                }
                $('#quiz-container').append(btn);
            });
        }).fail(function() {
            // If the request fails (e.g., no more questions can be loaded), submit the quiz
            submitQuiz();
        });
    }

    function submitQuiz() {
        console.log("Total Score:", totalScore, "Selected Topic:", selectedTopic);
        // Here, replace the console.log with your actual submit logic, such as:
        // $.post('/submit-quiz', {score: totalScore, topic: selectedTopic}, function(response) {
        //     // Handle response, e.g., display a message or redirect
        // });
        window.location.href = `/elearning?score=${totalScore}&topic=${selectedTopic}`;
    }

    $(document).on('click', '.answer-btn', function() {    
        if ($(this).data('score') !== undefined) {
            totalScore += parseInt($(this).data('score'));
        } else if ($(this).data('topic') !== undefined) {
            selectedTopic = $(this).data('topic');
        }
        currentQuestion++;
        //console.log("Total Score:", totalScore, "Selected Topic:", selectedTopic);
        loadQuestion(); // Load the next question or submit if at the end
    });

    loadQuestion(); // Load the first question
});