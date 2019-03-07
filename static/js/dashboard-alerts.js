getAlertsInfo();
setInterval(getAlertsInfo, 1000); //3000 MS == 3 seconds

var alertBody = document.getElementById('alert-body');

function getAlertsInfo() {
    $.ajax({
        type: 'GET',
        url: 'http://rafid/api-alerts-info',
        success: function(alerts) {
            alertBody.innerHTML = '';
            $.each(alerts, function (i, alert) {
                var link = '/resolve-alert/' + alert.id;
                //console.log(link);
                if (alert.severity === 'alert'){
                    alertBody.innerHTML += '<div class="alert alert-info" role="alert"><strong>Device: ' +
                                            '</strong>'+ alert.device_name +
                                            ' || <strong>Message: </strong>' + alert.error_details +
                                            ' || <strong>Occured: </strong>' + alert.date_time + '    ' +
                                            '<a href=" '+ link +'"class="btn btn-outline-secondary btn-sm float-right"' +
                                            ' role="button">Resolve</a>' +
                                            '</div>';
                } else if (alert.severity === 'warning'){
                    alertBody.innerHTML += '<div class="alert alert-warning" role="alert"><strong>Device: ' +
                                            '</strong>'+ alert.device_name +
                                            ' || <strong>Message: </strong>' + alert.error_details +
                                            ' || <strong>Occured: </strong>' + alert.date_time + '    ' +
                                            '<a href=" '+ link +'"class="btn btn-outline-secondary btn-sm float-right"' +
                                            ' role="button">Resolve</a>' +
                                            '</div>';

                } else if(alert.severity === 'danger'){
                    alertBody.innerHTML += '<div class="alert alert-danger" role="alert"><strong>Device: ' +
                                            '</strong>'+ alert.device_name +
                                            ' || <strong>Message: </strong>' + alert.error_details +
                                            ' || <strong>Occured: </strong>' + alert.date_time + '    ' +
                                            '<a href=" '+ link +'"class="btn btn-outline-secondary btn-sm float-right"' +
                                            ' role="button">Resolve</a>' +
                                            '</div>';
                }else {
                    console.log('severity type error');
                }
            });
        }
    });
}