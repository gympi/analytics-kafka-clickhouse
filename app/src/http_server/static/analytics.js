/*

Inserted script

<script type="text/javascript" charset="utf-8">
    (function() {
        var sm = document.createElement("script");
        sm.type = "text/javascript";
        sm.async = true;
        sm.defer = true;
        sm.src = "/analytics/static/analytics.js";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(sm, s);
    })();
</script>

*/

// Libs
function buildUrl(url, parameters) {
    let qs = "";
    for (const key in parameters) {
        if (parameters.hasOwnProperty(key)) {
            const value = parameters[key];
            qs +=
                encodeURIComponent(key) + "=" + encodeURIComponent(value) + "&";
        }
    }
    if (qs.length > 0) {
        qs = qs.substring(0, qs.length - 1); //chop off last "&"
        url = url + "?" + qs;
    }

    return url;
}

function build_params(added_params){
    return Object.assign({}, {
            url_visit: window.location.href,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            timestamp: Math.floor(Date.now() / 1000),

        }, added_params);
}

function send_tick(parameters){
    fetch(buildUrl("//analytics.ru/tick/", parameters), {
        method: 'get',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        },
        credentials: 'include',
        cache: 'no-cache',
        mode: 'cors'})
      .then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
              response.status);
            return;
          }
          response.json().then(function(data) {
            console.log('With analytics everything is fine!');
          });
        }
      )
      .catch(function(err) {
        console.log('Fetch Error', err);
      });
}

// Init environment

var ua = navigator.userAgent.toLowerCase();
if (ua.indexOf('safari') !== -1 && ua.indexOf('chrome') === -1) {
    var el = createAnalyticIframe();
} else {
    var el = createAnalyticImage();
}

function createAnalyticIframe(){
    var iframe = document.createElement('iframe');
    iframe.name = 'atvz';
    iframe.title = 'atvz';
    iframe.frameborder = 0;
    iframe.style.cssText = 'opacity: 0; width: 0px; height: 0px; position: absolute; left: 100%; bottom: 100%; border: 0px !important;';
    iframe.src = 'https://services.tvzvezda.ru/analytics/atvz_pixel.png';
    var s = document.getElementsByTagName("body")[0];
    s.append(iframe);
    return iframe
}

function createAnalyticImage(){
    var img = document.createElement('img');
    img.src = 'http://analytics.ru/static/p.png';
    img.style.cssText = 'display: none';
    var s = document.getElementsByTagName("body")[0];
    s.append(img);
    return img
}

// Load Pge
function afterLoad() {
  console.log('Send tick');
  send_tick(build_params({state: 'open'}));
}

el.onload = el.onerror = function() {
  if (!this.executed) { // executed only once
    this.executed = true;
    afterLoad();
  }
};

el.onreadystatechange = function() {
  var self = this;
  if (this.readyState === "complete" || this.readyState === "loaded") {
    setTimeout(function() {
      self.onload()
    }, 0); // Save "this" for onload
  }
};

// Close page
window.onbeforeunload = function () {
    send_tick(build_params({state: 'close'}))
};


