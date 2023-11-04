$(document).ready(function() {
    $('#send-btn').on('click', function() {
        var userInput = $('#user-input').val();
        if (userInput !== '') {
            $('#chat-log').append('<p><strong>You:</strong> ' + userInput + '</p>');
            $('#user-input').val('');

            $.ajax({
                url: '/get_response',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ input: userInput }),
                success: function(response) {
                    $('#chat-log').append('<p><strong>Chatbot:</strong> ' + response + '</p>');
                }
            });
        }
    });
});
