
var Helpers = {
	hash:null,
	
	getHash: 		function(){
						var h = this.hash || $("input[type='hidden']", "#login").val();
						this.hash = h;
						return this.hash;
					},
	
	splitDate: 		function(date)
					{
						var date = date.split(" ");
						var day = date[0];
						var hour = parseInt(date[1], 10);
						var AmPm = date[2];
						if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
							hour = hour;
						} else { hour = hour+12; }

						return {day:day, hour:hour};
					}
};

/*
var Widget = function(elem){
	
	var theActive, isActive;
	
	var hideList = function(){
		if(theActive) {
			theActive.hide();
			theActive.parent().removeClass("active");
		}
	};
	
	elem.find("ul.labs-list").each(function(){
		
		var list = $(this);
		currentLab = $(this).parent();
		
		var showList = function(){
			hideList();
			theActive = list.show();
			list.parent().addClass("active");
			isActive = list;
		};
		
		currentLab.click(function(e){
			if(e){ e.stopPropagation(); }
			if(e){ e.preventDefault(); }
			showList();
		});
	});
	
	$(document.body).bind('click',function(e) {
		if(isActive) {
			var active = isActive[0];
			if(!$.contains(active,e.target) || !active == e.target) {
				hideList();
			}
		}
	});

	return { theActive:theActive };
};
*/
