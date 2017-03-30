$('.marquee').hide();

get_status(
    function(possible_status) {
        $.ajax({
            url: "http://www.metrovias.com.ar",
            type: 'GET',
            success: function(data) {
                var data = $(data);
                var lines = ["A", "B", "C", "D", "E", "H"];
                var fullText = "";
                for (var i = 0; i < lines.length; ++i) {
                    var text = data.find("span#status-line-" + lines[i]).text();
                    if (text == ""){
                        // service down
                        fullText = "El servicio web de Metrovias no responde, no es posible obtener el estado del Subte. ";
                        break;
                    }
                    var selector = $("div#" + lines[i] + " > span.status");
                    if (check_status(text, possible_status['ok'])) {
                        selector.text("✓");
                        selector.addClass('ok');
                    } else if (check_status(text, possible_status['warn'])) {
                        selector.text("⚠");
                        selector.addClass('warn');
                        fullText += lines[i] + ": " + text + " ";
                    } else {
                        selector.text("✗");
                        selector.addClass('bad');
                        fullText += lines[i] + ": " + text + " ";
                    }
                }
                if (fullText != "") {
                    $('body').css({
                        'height': '200px'
                    })
                    $('.marquee').show();
                    $('.marquee').text(fullText);
                    $('.marquee').marquee({
                        duration: 3000,
                        delayBeforeStart: 0,
                        duplicated: true
                    });
                }
            }
        });
    })
