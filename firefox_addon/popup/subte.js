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
            var img = document.createElement('img');
            var sp1 = document.createElement('span');
            var sp2 = document.createElement('span');
            img.src = "../icons/linea_" + lines[i] + ".png";
            sp1.appendChild(img);
            text = data.find("span#status-line-" + lines[i]).text();
            if (text == "Normal" || text.indexOf("habitual")>-1){
                sp2.textContent = "✓";
            } else if (text.indexOf("emora")>-1 || text.indexOf("obras")>-1){
                sp2.textContent = "⚠";
            } else {
                sp2.textContent = "❌";
            }

            div.appendChild(sp1);
            div.appendChild(sp2);
            document.body.appendChild(div);
        }
    }
});
