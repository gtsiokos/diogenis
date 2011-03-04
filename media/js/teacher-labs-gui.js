$(function(){

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
	
	var Helpers			= X$('Helpers');
		ajaxTrans 		= transfer.find("ul.labs-list li"),
		theLabs 		= $("div.lab", "#content"),
		msg 			= $("#ui-messages p", "#content");
	
	theLabs.find("table td>input").removeAttr("disabled").attr('checked', false);
	
	ajaxTrans.click(function(){
		
		var ms,
			data,
			parentDiv = $(this).parents("div.lab");
		
		
		var newLabName,
			newLabDay,
			newLabHour = {};
		
		newLabName = $(this).find("span.name").text();
		var day = $(this).find("span.day").text();
		newLabDay = Helpers.explodeFullname(day);
		
		data = $(this).find("span.hour").metadata();
		newLabHour.start = data.start;
		newLabHour.end = data.end;
		
		
		var oldLabName,
			oldLabDay,
			oldLabHour = {};
		
		oldLabName = parentDiv.find("h4>span.lab-name").text();
		oldLabDay = parentDiv.find("h4>span.lab-date>span.day").text();
		
		data = parentDiv.find("h4>span.lab-date>span.hour").metadata();
		oldLabHour.start = data.start;
		oldLabHour.end = data.end;
		
		
		console.log(newLabName);
		console.log(newLabDay);
		console.log(newLabStartHour);
		console.log(newLabEndHour);
		console.log("--------------");
		console.log(oldLabName);
		console.log(oldLabDay);
		console.log(oldLabStartHour);
		console.log(oldLabEndHour);
		console.log("--------------");
		console.log("--------------");
		
		
		var i=0,
			amToSend = [],
			students = theActive.parents("div.lab").find("table tr:not(.disabled) td>input:checked");
		
		students.each(function(){
			amToSend[i] = { am: $(this).val() };
			i++;
		});
		
		if (newLabName != oldLabName || newLabDay != oldLabDay || newLabHour.start !== oldLabHour.start || newLabHour.end !== oldLabHour.end) {
			
			var request =	{
							lnew: [ { newName: newLabName, newDay: newLabDay, newHour: newLabHour} ],
							lold: [ {oldName: oldLabName, oldDay: oldLabDay, oldHour: oldLabHour} ],
							stud: amToSend
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
			if (amToSend[0]) { ms = "Χρησιμοποιείτε το ίδιο εργαστήριο"; }
			setTimeout( function() {
				msg.fadeOut(100).removeClass().addClass("warning").text(ms).fadeIn(200);
			},300);
			$.scrollTo({top: 0}, 500, {axis:"y"});
		}
		return false;
	});

});

