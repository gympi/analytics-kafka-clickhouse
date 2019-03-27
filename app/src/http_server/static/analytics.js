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
            urlVisit: window.location.href,
            timezoneClient: Intl.DateTimeFormat().resolvedOptions().timeZone,
            sessionStartClient: sessionStartClient,
            screenWidth: width,
            screenHeight: height,
            width: width,
            height: height,

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
      .then(function(response){
          if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
              response.status);
            return;
          }

          var contentType = response.headers.get("content-type");
            if(contentType && contentType.includes("application/json")) {
              return response.json();
            }
            throw new TypeError("Oops, we haven't got JSON!");
      })
      .then(function(json) {
              sessionUidClient=json.sessionUidClient
          }
      )
      .catch(function(err) {
        console.log('Fetch Error', err);
      });
}

// Init environment

var sessionUidClient = undefined;
var sessionStartClient = Math.floor(Date.now() / 1000);

var width = window.innerWidth
|| document.documentElement.clientWidth
|| document.body.clientWidth;

var height = window.innerHeight
|| document.documentElement.clientHeight
|| document.body.clientHeight;


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
    send_tick(build_params({state: 'close', sessionUidClient: sessionUidClient, sessionStopClient: Math.floor(Date.now() / 1000), sessionDurationClient: Math.floor(Date.now() / 1000) - sessionStartClient}))
};

//window.addEventListener("load", constructor);
//window.addEventListener("beforeunload", destructor, false);



// var Environments = {};
//
// Environments.URL = (function(){
//     var hashParams = {};
//     var searchParams = {};
//
//     console.log(window.location);
//
//     var _initHashParams = function(){
//         hashParams = _splitParams(window.location.hash)
//     };
//
//     var _initSearchParams = function(){
//         searchParams = _splitParams(window.location.search)
//     };
//
//     var _splitParams = function(str){
//         return str.split('&').reduce(function (result, item) {
//             var parts = item.split('=');
//             result[parts[0].replace(/[?#]/, '')] = parts[1];
//             return result;
//         }, {});
//     };
//
//     var urlParam = function (name){
//         var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
//         if (results==null){
//            return null;
//         }
//         else{
//            return decodeURI(results[1]) || 0;
//         }
//     }
//
//     _initHashParams();
//     _initSearchParams();
//     window.addEventListener("hashchange", _initHashParams);
// })();


var a = '<div class="js-analytics-mark" style="position: absolute;left: 0px;right: 0px;height: 100px; width: 200px; z-index: 9999;opacity: 0.5;background: rgb(244, 78, 78);top: 100px; pointer-events: none;"><span style="position: absolute; top: -28px; left: 16px; font-family: Arial; font-size: 15px; color: white; background: rgb(244, 78, 78); line-height: 32px; padding: 0px 16px; display: inline-block; border-radius: 3px;">Block selection</span></div>'

document.getElementsByTagName("body")[0].innerHTML += a;

