$(function(){

	//********************************
	//Global Ajax Behaviour
	//********************************		
	
	var theBody = $("body:first");
	
	theBody.ajaxStart(function(){
		theBody.addClass("wait");
	});
	theBody.ajaxComplete(function(){
		theBody.removeClass("wait");
	});
	
	//********************************
	//Ajax-Register-Lab Feature
	//********************************
	
	StudentRegister.init();


});

