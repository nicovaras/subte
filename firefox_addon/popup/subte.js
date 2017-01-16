var div = document.createElement('div');
div.textContent = "Cargando...";
document.body.appendChild(div);
$.ajax({
    url: "http://www.metrovias.com.ar",
    type: 'GET',
    success: function(data){
        $("div").empty();
        var data = $(data);
        var lines = ["A", "B", "C", "D", "E", "H"];
        for (var i = 0; i < lines.length; ++i) {
            var div = document.createElement('div');
            text = data.find("span#status-line-" + lines[i]).text();
            if (text == "Normal" || text.indexOf("habitual")>-1){
                div.textContent = "✓";
            } else if (text.indexOf("emora")>-1 || text.indexOf("obras")>-1){
                div.textContent = "⚠";
            } else {
                div.textContent = "❌";
            }
            div.textContent = lines[i] + ": " + div.textContent
            document.body.appendChild(div);
        }
    }
});
