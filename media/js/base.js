$(function(){
	
	//********************************
	//Focus-Out Feauture for Options Panel
	//********************************	
	
	oPanel = $("#login");
	oPanel.find('div.panel').hide();
	
	var theActive, isActive;
	
	var hidePanel = function(){
		if(theActive) {
			theActive.hide();
			theActive.parent().removeClass("active");
		}
	};
	
	oPanel.find("div.panel").each(function(){
		
		var options = $(this);
		loginDiv = $(this).parent();
		
		var showPanel = function(){
			hidePanel();
			theActive = options.show();
			loginDiv.addClass("active");
			isActive = options;
		};
		
		loginDiv.children("a.options-panel").click(function(e){
			if ( loginDiv.hasClass("active") ){
				hidePanel();
			} else {
				showPanel();
			}
			if(e){ e.stopPropagation(); }
			if(e){ e.preventDefault(); }
		});
	});
	
	$(document.body).bind('click',function(e) {
		if(isActive) {
			var active = isActive[0];
			if(!$.contains(active,e.target) || !active == e.target) {
				hidePanel();
			}
		}
	});
	
});
