function updateIcon() {
    get_status(
    function(possible_status) {
    $.ajax({
        url: "http://www.metrovias.com.ar",
        type: 'GET',
        success: function(data) {
            var data = $(data);
            var lines = ["A", "B", "C", "D", "E", "H"];
            var warn = false;
            var bad = false;
            for (var i = 0; i < lines.length; ++i) {
                var text = data.find("span#status-line-" + lines[i]).text();
                if (text == ""){
                    chrome.browserAction.setBadgeBackgroundColor({ color: "#FF9933" });
                    chrome.browserAction.setBadgeText({text: '⚠'});
                    break;
                }
                if (check_status(text, possible_status['warn'])){
                    chrome.browserAction.setBadgeBackgroundColor({ color: "#FF9933" });
                    chrome.browserAction.setBadgeText({text: '⚠'});
                } else if (!check_status(text, possible_status['ok'])) {
                    chrome.browserAction.setBadgeBackgroundColor({ color: [255, 0, 0, 255] });
                    chrome.browserAction.setBadgeText({text: '✗'});
                    break;
                }
            }
        }
    });})
}

updateIcon()
chrome.alarms.create({
  periodInMinutes:(1.0)
});

chrome.alarms.onAlarm.addListener((alarm) => {
  chrome.browserAction.setBadgeText({text: ''});
  updateIcon()
});

