$(function() {
    $.material.init();
    $("#jobform").validate({focusCleanup: true});
    $("#joburl").change(function () {
        var url = $(this).val();
        var pat = /^((http|https|ftp):\/\/)?(\w(\:\w)?@)?([0-9a-z_-]+\.)*?([a-z0-9-]+\.[a-z]{2,6}(\.[a-z]{2})?(\:[0-9]{2,6})?)((\/[^?#<>\/\\*":]*)+(\?[^#]*)?(#.*)?)?$/i;
        var ret = pat.exec(url);
        if (ret != null && ret.length > 10 && ret[10] != undefined && ret[10].length > 1) {
            $("#filename").val(ret[10].substring(1));
        }
    });
    $(".pop-tooltip").tooltip();
});
