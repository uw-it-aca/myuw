/*  University of Washington - Alert 2.0 Beta
 *  (c) 2011 Chris Heiland
 *
 *  Script should be included like such:
 * 
 *  <html>
 *  <head>
 *  <title>Page Title</title>
 *  </head>
 *  <body>
 * 
 *  <script type="text/javascript" src="//washington.edu/static/alert.js"></script>
 *  </body>
 *  </html>
 *
 *  Full docs at:
 *  uw.edu/externalaffairs/uwmarketing/toolkits/uw-alert-banner/
 *
 *--------------------------------------------------------------------------*/

var strProto = (window.location.protocol == 'https:') ? 'https://' : 'http://';

// Thanks Dane!
var test_status = window.location.hash.indexOf('alert') === -1 ? 'false' : 'true';
// Allow for local testing
var strDomain = 'www.washington.edu/static';
var strDataFeed = '/UW-Alert-Banner/alert/?c=displayAlert&test='+test_status

var strScript = document.createElement('script');
strScript.setAttribute('src', strProto + strDomain + strDataFeed);

document.getElementsByTagName('head')[0].appendChild(strScript); 

// displayAlert - grab content to display message 
function displayAlert(objAlertData)
{
    // Just in case w.com delivers us something bad
    // or We don't care if there's nothing
    if ((!objAlertData) || (objAlertData.found == 0)) {
        // For some reason the test feed has found: 0 in it.  So, dropping the return.
//        return false;
    }
    // This test instead of the one above
    if (!objAlertData.posts || !objAlertData.posts.length) {
        return false;
    }

    // Alert colors
    arrAlertTypes = {
        'red-alert-urgent' : 'uwalert-red',
        'orange-alert'     : 'uwalert-orange',
        'steel-alert-fyis' : 'uwalert-steel'
    };

    for (strCategory in objAlertData.posts[0].categories ) 
    {
        if ( window.location.hash.indexOf('uwalert') != -1 )
            var strTestAlertColor = window.location.hash.replace('#','');

        var objCategory = objAlertData.posts[0].categories[strCategory];
        // Quick way to determine color
        if ((arrAlertTypes[objCategory.slug]) || strTestAlertColor)
        {
            var strAlertTitle  = objAlertData.posts[0].title;
            var strAlertLink   = 'http://emergency.washington.edu/';
            var strAlertMessage = objAlertData.posts[0].excerpt;
            var strAlertColor = arrAlertTypes[objCategory.slug] ? arrAlertTypes[objCategory.slug] : strTestAlertColor;
        }

    }

    // Banners must have an actual color
    if (strAlertColor)
    {
        addElement(strAlertTitle,strAlertLink,strAlertColor,strAlertMessage);
    }
}

// addElement - display HTML on page right below the body page
// don't want the alert to show up randomly
function addElement(strAlertTitle,strAlertLink,strAlertColor,strAlertMessage)
{
    // Grab the tag to start the party
    var bodyTag = document.getElementsByTagName('body')[0];

  var wrapperDiv = document.createElement('div');
  wrapperDiv.setAttribute('id','uwalert-alert-message');
  wrapperDiv.setAttribute('class', strAlertColor + ' alert alert-block');

  var alertBoxTextDiv = document.createElement('div');

  var alertIcon = document.createElement('i');
  alertIcon.setAttribute('class', 'icon-warning-sign icon-large');

  var header1 = document.createElement('h1');

  var jq_h1 = $(header1);
  jq_h1.html($("<div></div>").html(strAlertTitle).text());
  header1.appendChild(alertIcon);

  var alertTextP = document.createElement('p');

  var jq_atp = $(alertTextP);

  var message_text = $("<div></div>").html(strAlertMessage).text();

  jq_atp.html(message_text.substring(0, 360) + (message_text.length >= 360 ? '... ' : ' '));

  var alertLink = document.createElement('a');
  alertLink.setAttribute('href', strAlertLink);
  alertLink.setAttribute('title', strAlertTitle);
  var alertLinkText = document.createTextNode('More Info');
  alertLink.appendChild(alertLinkText);

  // Start Building the Actual Div
  alertTextP.appendChild(alertLink);

  alertBoxTextDiv.appendChild(header1);
  alertBoxTextDiv.appendChild(alertTextP);

  wrapperDiv.appendChild(alertBoxTextDiv);

  bodyTag.insertBefore(wrapperDiv, bodyTag.firstChild);
} 

