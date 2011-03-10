
X$('StudentTransfer',
{
	url:				undefined,
	am_to_transfer:		[],
	
	new_lab:			{ name: "", day: "", hour: {} },
	old_lab:			{ name: "", day: "", hour: {} },
	
	init: 		function(){
					var _self = this;
					
					_self.url = _self.urlCheck();
					
					//********************************
					//Focus-Out Feature
					//********************************	
	
					var transfer = $("div.lab span.transfer.enabled", "#content");
	
					var theActive, isActive;
	
					var hideList = function(){
						if(theActive) {
							theActive.hide();
							theActive.parent().removeClass("active");
						}
					};
	
					transfer.find("ul.labs-list").each(function(){
		
						var list = $(this);
						var currentLab = $(this).parent();
		
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
	
	
					//********************************
					//Ajax-Transfer Feature
					//********************************	
	
					var Helpers			= X$('Helpers'),
						ajaxTrans 		= transfer.find("ul.labs-list li"),
						theLabs 		= $("div.lab", "#content"),
						msg 			= $("#ui-messages p", "#content");
	
					theLabs.find("table td>input").removeAttr("disabled").attr('checked', false);
	
					ajaxTrans.click(function(){
		
						var ms,
							data,
							parentDiv = $(this).parents("div.lab");
		
						_self.new_lab['name'] = $(this).find("span.name").text();
						var day = $(this).find("span.day").text();
						_self.new_lab['day'] = Helpers.explodeFullname(day);
		
						data = $(this).find("span.hour").metadata();
						_self.new_lab['hour'].start = data.start;
						_self.new_lab['hour'].end = data.end;
		
		
						_self.old_lab['name'] = parentDiv.find("h4>span.lab-name").text();
						_self.old_lab['day'] = parentDiv.find("h4>span.lab-date>span.day").text();
		
						data = parentDiv.find("h4>span.lab-date>span.hour").metadata();
						_self.old_lab['hour'].start = data.start;
						_self.old_lab['hour'].end = data.end;
		
		
						var i = 0,
							students = theActive.parents("div.lab").find("table tr:not(.disabled) td>input:checked");
						
						_self.am_to_transfer = [];
						students.each(function(){
							_self.am_to_transfer[i] = { am: $(this).val() };
							i++;
						});
		
						if (_self.conditionCheck()) {
			
							var request =	{
											lnew: { newName: _self.new_lab.name, newDay: _self.new_lab.day, newHour: _self.new_lab.hour},
											lold: {oldName: _self.old_lab.name, oldDay: _self.old_lab.day, oldHour: _self.old_lab.hour},
											stud: _self.am_to_transfer
											};
			
							var ajaxUrl = '/teachers/'+Helpers.getHash()+'/submit-student-to-lab/';
							$.ajax({
								url: ajaxUrl,
								type: 'POST',
								contentType: 'application/json; charset=utf-8',
								data: $.toJSON(request),
								dataType: 'json',
								timeout: 10000,
								success: function(data) {
								   	try {
								   	    if (data[0].status == 1){
									   		students.parents("tr").addClass("disabled", 80).find("input").attr("disabled", "disabled");
											setTimeout( function() {
												msg.fadeOut(100).removeClass().addClass("ok")
												.text(data[0].msg).append("<a href='#' onClick='window.location.reload()'>ανανέωση</a>")
												.fadeIn(200);
											},300);
										}
										else if ( data[0].status == 2 ) {
											setTimeout( function() {
												msg.fadeOut(100).removeClass().addClass("error").text(data[0].msg).fadeIn(200);
											},300);					
										}
										else {
											setTimeout( function() {
												msg.fadeOut(100).removeClass().addClass("warning").text(data[0].msg).fadeIn(200);
											},300);
										}
									}
									catch(e) { this.error(); }
								},
								error: function(xhr, err){
									ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε αργότερα";
									/*
									if(xhr.status==500){
										ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
									}
									if(xhr.status==404){
										ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
									}
									*/
									msg.fadeOut(100).removeClass().addClass("error").text(ms).fadeIn(200);
								},
								complete: function() {
									if(theActive) {
										theActive.hide();
										theActive.parent().removeClass("active");
									}
									$.scrollTo({top: 0}, 350, {axis:"y"});
								}
							});
						} else {
							if(theActive) {
								theActive.hide();
								theActive.parent().removeClass("active");
							}
							
							ms = "Δεν έχετε επιλέξει κάποιον σπουδαστή";
							if (_self.url === "home" && _self.am_to_transfer[0]){
								ms = "Χρησιμοποιείτε το ίδιο εργαστήριο";
							}
							
							setTimeout( function() {
								msg.fadeOut(100).removeClass().addClass("warning").text(ms).fadeIn(200);
							},300);
							$.scrollTo({top: 0}, 500, {axis:"y"});
						}
						return false;
					});
				
				return this;
				},
		
	conditionCheck: 	function(){
							var _self = this,
								condition;
							
							if(_self.url === "home"){
								condition = Boolean(	_self.new_lab.name !== _self.old_lab.name || 
														_self.new_lab.day !== _self.old_lab.day || 
														_self.new_lab.hour.start !== _self.old_lab.hour.start || 
														_self.new_lab.hour.end !== _self.old_lab.hour.end
													);
							}
							else if (_self.url === "pending"){
								condition = Boolean(_self.am_to_transfer[0]);
							}
							
							return condition;
						},
	
	urlCheck:			function(){
							var result = {},
								url = window.location.href;
							
							if( url.match(/pending-students/) ){
								result = "pending";
							}
							else {
								result = "home";
							}
							//console.log(result);
							return result;
						}
	
});

