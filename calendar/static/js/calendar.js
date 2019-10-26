$(document).ready(() => {
    // hard coded calendar for October
    var $table_body = $('tbody');
    var row_html = '';

    start_pos = 1;
    end_pos = 32;
    
    for (var i = 1; i <= 35; i++) {
        
        if (i <= start_pos || i > end_pos) {
            row_html += '<td>' + '' + '</td>';
        } else {
            row_html += '<td><p>' + (i - start_pos) + '</p></td>';
        }
        if (i % 7  == 0) {
            $table_body.append('<tr>' + row_html + '</tr>');
            row_html = '';
        }
    }
});