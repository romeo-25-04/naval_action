$(document).ready(function () {
    $('.port').on('click', function(){
        lon = $(this).find('td.lon').text();
        lat = $(this).find('td.lat').text();
        $('#dest_a').val(lon);
        $('#dest_b').val(lat);
    })
});

