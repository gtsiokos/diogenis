$(function(){

	var highestCol = parseInt($("#content").height(), 10);
	$("#sidebar").height(highestCol+10);

	var theWindow = $(window);
	var theSidebar = $("#sidebar");
	var theNavigation = $("#navigation");
	
	var setNavigation = function() {
		
		var a = theSidebar.offset();
		var bLeft = parseInt(a.left, 10);
		theNavigation.css({ top: 170, left: bLeft });
		
	};
	theWindow.resize(setNavigation);
	setNavigation();
});
