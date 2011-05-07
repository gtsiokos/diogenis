
X$('Helpers',
{
	csrf_token: undefined,
	//hash: undefined,
	
	init:				function(){
							this.gerCsrfToken().setGlobalAjax();
							return this;
						},
	
	gerCsrfToken:		function(){
							var _self = this,
								cookie,
								cookies;
							
							if (document.cookie && document.cookie != '') {
								cookies = document.cookie.split(';');
								for (var i = 0, len = cookies.length; i<len; i++) {
									cookie = _self.getCookie(cookies[i]);
									if (cookie['name'] === 'csrftoken') {
										_self.csrf_token = cookie['value']
										break;
									}
								}
							}
							return this;
						},
	
	getCookie:			function(cookie){
							cookie = $.trim(cookie);
							cookie = cookie.split('=');
							return { name:cookie[0], value:cookie[1] }
						},
	/*
	getHash: 			function(){
							var h = this.hash || $("input[type='hidden']", "#login").val();
							this.hash = h;
							return this.hash;
						},
	*/
	splitDate: 			function(date){
							var date = date.split(" ");
							var day = date[0];
							var hour = parseInt(date[1], 10);
							var AmPm = date[2];
							if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
								hour = hour;
							} else { hour = hour+12; }

							return {day:day, hour:hour};
						},
	
	explodeFullname:	function(day){
							var daysStr 	= "Δευτέρα Τρίτη Τετάρτη Πέμπτη Παρασκευή",
								days 		= daysStr.split(/ +/),
								matchedDay	= undefined;
							
							for(var i=0, len=days.length; i<len; i++){
								if( day == days[i].substr(0,3) ){
									matchedDay = days[i];
									break;
								}
							}
							
							return matchedDay || false;
						},
	
	//********************************
	//Global Ajax Behaviour
	//********************************	
	setGlobalAjax:		function(){
							var _self = this,
								theBody = $("body:first");
	
							theBody.ajaxStart(function(){
								theBody.addClass("wait");
							});
							
							theBody.ajaxSend(function(e, xhr, settings){
								if ( !(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)) ){
									xhr.setRequestHeader("X-CSRFToken", _self.csrf_token);
								}
							});
							
							theBody.ajaxComplete(function(){
								theBody.removeClass("wait");
							});
							
							return this;
						}
});

