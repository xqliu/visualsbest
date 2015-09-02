$(document).ready(function () {
    document.addEventListener('bicCalendarUnSelect', function (e) {
        var amount = $("#amount");
        if (amount.length) {
            amount.val('');
        }
    });
    document.addEventListener('bicCalendarSelect', function (e) {
        moment.lang('zh_CN'); // default the language to Chinese
        var dateFirst = new moment(e.detail.dateFirst);
        var dateLast = new moment(e.detail.dateLast);
        if (dateLast - dateFirst > 0) {
            $('#from_day').val(dateFirst.format('YYYY-MM-DD'));
            $('#end_day').val(dateLast.format('YYYY-MM-DD'));
        } else {
            $('#from_day').val(dateLast.format('YYYY-MM-DD'));
            $('#end_day').val(dateFirst.format('YYYY-MM-DD'));
        }

        var price = $("#price");
        var amount = $("#amount");
        if (amount.length && price.length) {
            var number = (dateLast - dateFirst) > 0 ? dateLast - dateFirst : dateFirst - dateLast;
            amount.val(Math.abs(price.val() * (1 + number / 3600 / 24 / 1000)))
        }
    });
});

$(document).ready(function () {

    var monthNames = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"];

    var dayNames = ["日", "一", "二", "三", "四", "五", "六"];

    var events = [{}];

    $('#events-calendar').bic_calendar({
        //list of events in array
        events: events,
        //enable select
        enableSelect: true,
        //enable multi-select
        multiSelect: true,
        //set day names
        dayNames: dayNames,
        //set month names
        monthNames: monthNames,
        //show dayNames
        showDays: true,
        //show month controller
        displayMonthController: true,
        //show year controller
        displayYearController: true,
        //set ajax call
        reqAjax: {
            type: 'get',
            //url: 'http://bic.cat/bic_calendar/index.php'
            url: '/date_status/json/' + $("#photographer_id").val()
        }
    });
});