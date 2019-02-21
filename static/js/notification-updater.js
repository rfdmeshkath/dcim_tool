getTotalAlerts();
setInterval(getTotalAlerts, 30000); //3000 MS == 3 seconds

    function getTotalAlerts() {
        $.ajax({
            type: 'GET',
            url: 'http://rafid/total-dashboard-alerts',
            success: function(data) {
                console.log('success', data);
                document.getElementById("alert_notification").innerHTML=data;
            }
        });
    }