/*

Inserted script

<script type="text/javascript" charset="utf-8">
    (function() {
        var sm = document.createElement("script");
        sm.type = "text/javascript";
        sm.async = true;
        sm.src = "/analytics/static/analytics.js";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(sm, s);
    })();
</script>

*/

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


fetch(buildUrl("/analytics/", {
        url_visit: window.location.href
    }))
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