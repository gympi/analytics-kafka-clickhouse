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
        screenWidth: windowRect().width,
        screenHeight: windowRect().height,
        width: windowRect().width,
        height: windowRect().height,

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


String.prototype.endWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

function isInt(n){
    return Number(n) === n && n % 1 === 0;
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}

function windowRect() {
    var width = window.innerWidth
        || document.documentElement.clientWidth
        || document.body.clientWidth;

    var height = window.innerHeight
        || document.documentElement.clientHeight
        || document.body.clientHeight;

    return {
        width: width,
        height: height
    }
}

function viewPort(){
    var winRect = windowRect();

    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    var scrollRight = scrollLeft + winRect.width;
    var scrollBottom = scrollTop + winRect.height;

    return {
        scrollTop: scrollTop,
        scrollLeft: scrollLeft,
        scrollRight: scrollRight,
        scrollBottom: scrollBottom
    }
}

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


var AnalyticCloudFun = {};

AnalyticCloudFun.Environments = {};

AnalyticCloudFun.Environments = (function(){
    var hashParams = {};
    var searchParams = {};

    console.log(window.location);

    var initHashParams = function(){
        hashParams = _splitParams(window.location.hash);
        return hashParams
    };

    var initSearchParams = function(){
        searchParams = _splitParams(window.location.search);
    };

    var _splitParams = function(str){
        return str.split('&').reduce(function (result, item) {
            var parts = item.split('=');
            result[parts[0].replace(/[?#]/, '')] = parts[1];
            return result;
        }, {});
    };

    var urlParam = function (name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null){
            return null;
        }
        else{
            return decodeURI(results[1]) || 0;
        }
    };

    initHashParams();
    initSearchParams();
    window.addEventListener("hashchange", initHashParams);

    return {hashParams: hashParams, initHashParams: initHashParams, searchParams: searchParams}
})();

function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild;
}

AnalyticCloudFun.Develop = (function () {
    var _initDevelopEnveroment = function(){

        //Show observed blocks
        observedElements.forEach(function(observedElement) {
            if (Number.parseInt(AnalyticCloudFun.Environments.initHashParams()['dev']) > 0)
                observedElement.showMarkBlock();
            else
                observedElement.hideMarkBlock();
        });

        //Show mark blocks
        observerElements.forEach(function (observerElement) {
            if (Number.parseInt(AnalyticCloudFun.Environments.initHashParams()['dev']) > 0)
                observerElement.showMarkBlock();
            else
                observerElement.hideMarkBlock();
        });
    };

    window.addEventListener("hashchange", _initDevelopEnveroment);
})();


var selectors = ['.last_news_1', '.last_news_3', '.last_news_4'];

var observedElements = [];

class ObservedElement {

    constructor(element, selector) {
        this.element = element;
        this.selector = selector;
        this.isView = false;
        this.rect = element.getBoundingClientRect();
        this._on = false;
        this.mark = undefined;

        this.element.addEventListener("eventIsViewObservedElement", function(event) {
            console.log(event)
        }, false);
    }

    setIsView(){
        this.isView = true;

        if (this.mark !== undefined)
            this.mark.style.background = 'rgb(135,206,250)';
        console.log(this.element);
        console.log(this.isView);
        this.element.dispatchEvent(new Event("eventIsViewObservedElement"))
    }

    showMarkBlock(){
        if (!this._on){
            this._on = true;
            this.mark = this._mark(this.rect.width, this.rect.height, this.rect.top, this.rect.left, this.selector);
        }
    }

    hideMarkBlock(){
        if (this._on){
            this._on = false;
            this.mark.parentElement.removeChild(this.mark);
        }
    }

    _mark(width, height, top, left) {
        var element = createElementFromHTML(
            '<div class="js-analytics-mark" style="position: absolute; left: ' + left.toString() + 'px; right: 0px; top: ' + top.toString() + 'px; height: ' + height.toString() + 'px; width: ' + width.toString() + 'px; z-index: 9999;opacity: 0.5;background: rgb(244, 78, 78); pointer-events: none;"><span style="position: absolute; top: -28px; left: 16px; font-family: Arial; font-size: 15px; color: white; background: rgb(244, 78, 78); line-height: 32px; padding: 0px 16px; display: inline-block; border-radius: 3px;">Block selection '+ this.selector.toString() + '</span></div>'
        );
        document.getElementsByTagName("body")[0].appendChild(element);
        return element;
    }
}

var observerElements = [];

class ObserverElement {
    constructor() {
        this.buildPositionMark();

        this._on = false;
        this.mark = undefined;

        var a = this;

        document.addEventListener("scroll", function (){a.buildPositionMark()}, false);
    }

    buildPositionMark(){
        var _viewPort = viewPort();
        var _windowRect = windowRect();
        this.top = _viewPort.scrollTop + _windowRect.height / 100 * 70;
    }

    buildScrolPositionMark(){
        document.getElementById('markView').style.top = this.top + 'px';
    }

    showMarkBlock(){
        if (!this._on){
            this._on = true;
            this.mark = this._mark(this.top);
            var a = this;
            window.addEventListener("scroll", function (){a.buildScrolPositionMark()}, false);
        }
    }

    hideMarkBlock(){
        if (this._on){
            this._on = false;
            this.mark.parentElement.removeChild(this.mark);
        }
    }

    _mark(top) {
        var rect = windowRect();
        var width = rect.width / 100 * 95;
        var element = createElementFromHTML(
            '<div class="js-analytics-mark" id="markView" style="position: absolute; margin-left: auto; margin-right: auto; top: ' + top.toString() + 'px; height: 3px; width: ' + width.toString() + 'px; z-index: 9999;opacity: 0.5; background: rgb(135,206,250); pointer-events: none;"><div style="position: absolute; width: 3px; height: 23px; top: -10px; background: rgb(135,206,250); pointer-events: none;"></div><div style="position: absolute; width: 3px; height: 23px; top: -10px; left: ' + width.toString() + 'px; background: rgb(135,206,250); pointer-events: none;"></div><span style="position: absolute; top: -28px; left: 16px; font-family: Arial; font-size: 15px; color: white; background: rgb(135,206,250); line-height: 32px; padding: 0px 16px; display: inline-block; border-radius: 3px;">View mark</span></div>'
        );
        document.getElementsByTagName("body")[0].appendChild(element);
        return element;
    }
}

(function () {
    if (!Array.prototype.forEach) {
        Array.prototype.forEach = function forEach (callback, thisArg) {
            if (typeof callback !== 'function') {
                throw new TypeError(callback + ' is not a function');
            }
            var array = this;
            thisArg = thisArg || this;
            for (var i = 0, l = array.length; i !== l; ++i) {
                callback.call(thisArg, array[i], i, array);
            }
        };
    }
})();

//Init marks
observerElements.push(new ObserverElement());

//Init observed elements
selectors.forEach(function(selector) {
    var elements = document.querySelectorAll(selector);

    elements.forEach(function(element) {
        observedElements.push(new ObservedElement(element, selector));
    });
});


window.addEventListener("scroll", function(event) {
    observerElements.forEach(function (observerElement) {
        observedElements.filter(elementItem => elementItem.isView === false).forEach(function (elementItem) {
            var elementRect = elementItem.rect;

            //if(elementRect.bottom < viewPort.scrollBottom && elementRect.top > viewPort.scrollTop){
            if(elementRect.top < observerElement.top){
                elementItem.setIsView();
            }
        });
    });
}, false);


// window.addEventListener("eventIsViewObservedElement", function(event) {
//     console.log(event)
// }, false);
