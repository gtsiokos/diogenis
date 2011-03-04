
X$('Helpers',
{
	hash: undefined,
	
	init:				function(){
							this.setGlobalAjax();
							return this;
						},
	
	getHash: 			function(){
							var h = this.hash || $("input[type='hidden']", "#login").val();
							this.hash = h;
							return this.hash;
						},
	
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
							var theBody = $("body:first");
	
							theBody.ajaxStart(function(){
								theBody.addClass("wait");
							});
							theBody.ajaxComplete(function(){
								theBody.removeClass("wait");
							});
						}
});

