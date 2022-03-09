$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault()
        form = $('form')

        $.ajax({
            'url':'/ajax/newsletter',
            'type':'POST',
            // data attribute is what we are passing to the request.
            // serialize converts the form values into a JSON 
            'data':form.serialize(),
            'dataType':'json',
            'success': function() {
                alert(data['success'])
            },
        })
        $('#id_your_name').val('')
        $('#id_email').val('')
    })
})