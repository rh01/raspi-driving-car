$('#searching').hide()
$('#results-table').hide()
$('#error').hide()

var  data = []

$(function() {
  $('.img').click(function() {
    $(this).addClass('active')

    $('#results').empty()
    $('#results-table').hide()
    $('#error').hide()

    $('.img').removeClass('active')
    $(this).addClass('active')

    var image = $(this).attr('src').split('/').pop()

    $('#searching').show()

    $.ajax({
      type: 'POST',
      url: '/search',
      data: {img: image},
      success: function(d) {
        $('#searching').hide()
        var data = d.results
        $('#results-table').show()
        for (i = 0; i < data.length; i++) {
          $("#results").append('<tr><th><img class="img-results" src="../static/images/' + data[i]["image"] + '"></th><th>' + data[i]['score'] + '</th></tr>')
        }
      },
      error: function(error) {
        $('#searching').hide()
        $('#error').append()
      }
    })
  })
})