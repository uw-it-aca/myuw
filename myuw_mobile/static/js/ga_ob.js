var myuwUaId="";

if (location.hostname=='myuw.washington.edu') {
  myuwUaId='UA-22539974-7'; 
} else if (location.hostname=='my-test.s.uw.edu') { 
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
  ga.src = '//www.google-analytics.com/analytics.js';
  var s = document.getElementsByTagName('script')[0]; 
  s.parentNode.insertBefore(ga, s);
 })();
// end