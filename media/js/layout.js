$(function(){

	var highestCol = Math.round($("#content").height());
	$("#sidebar").height(highestCol+10);

	
	var theNavigation = $("#navigation");
	
	if (theNavigation.length > 0) {
		
		var theWindow = $(window);
		var theSidebar = $("#sidebar");
		var setNavigation = function() {
		
			var a = theSidebar.offset();
			var bLeft = Math.round(a.left);
			theNavigation.css({ top: 170, left: bLeft });
		
		};
		theWindow.resize(setNavigation);
		setNavigation();
	}
});
