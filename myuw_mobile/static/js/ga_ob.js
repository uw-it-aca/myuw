var myuwUaId="";

if (location.hostname=='myuw.washington.edu') {
  myuwUaId='UA-22539974-7'; 
} else if (location.hostname=='myuwtest.u.washington.edu') { 
  myuwUaId='UA-22539974-8'; 
} else { myuwUaId='UA-22539974-6'; }

// begin standard google analytics code
var _gaq = _gaq || [];
_gaq.push(['_setAccount', myuwUaId]);
_gaq.push(['_gat._anonymizeIp']); 
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); 
  ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == window.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; 
  s.parentNode.insertBefore(ga, s);
 })();
// end

