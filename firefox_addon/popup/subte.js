$.ajax({
    url: "http://www.metrovias.com.ar",
    type: 'GET',
    success: function(data){
        var data = $(data);
        var lines = ["A", "B", "C", "D", "E", "H"];
        for (var i = 0; i < lines.length; ++i) {
            var text = data.find("span#status-line-" + lines[i]).text();
            var selector = $("div#" + lines[i] + " > span.status");
            if (text == "Normal" || text.indexOf("habitual")>-1){
                selector.text("✓");
                selector.addClass('ok');
            } else if (text.indexOf("emora")>-1 || text.indexOf("obras")>-1){
                selector.text("⚠");
                selector.addClass('warn');

            } else {
                selector.text("❌");
                selector.addClass('bad');
            }
        }
    }
});
