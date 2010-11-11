$(function(){

	//********************************
	//Find Login Hash
	//********************************	
	
	hashValue = $("input[type='hidden']", "#login").val();
	
	//********************************
	//Focus-Out Feature
	//********************************	
	
	transfer = $("div.lab span.transfer.enabled", "#content");
	
	var theActive, isActive;
	
	var hideList = function(){
		if(theActive) {
			theActive.hide();
			theActive.parent().removeClass("active");
		}
	};
	
	transfer.find("ul.labs-list").each(function(){
		
		var list = $(this);
		currentLab = $(this).parent();
		
		var showList = function(){
			hideList();
			theActive = list.show();
			list.parent().addClass("active");
			isActive = list;
		};
		
		currentLab.click(function(e){
			if(e) e.stopPropagation();
			if(e) e.preventDefault();
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
	
	ajaxTrans = transfer.find("ul.labs-list li");
	$("div.lab", "#content").find("table td>input").removeAttr("disabled").attr('checked', false);
	msg = $("#ui-messages p", "#content");
	
	ajaxTrans.click(function(){
		
		var ms;
		var parentDiv = $(this).parents("div.lab");
		
		
		newLabName = $(this).find("span.name").text();
		var day = $(this).find("span.day").text();
		var newLabDate = $(this).find("span.hour").text();
		var date = newLabDate.split(" ");
		var hour = parseInt(date[0], 10);
		var AmPm = date[1];
		if (AmPm == "π.μ.") {
			newLabHour = hour;
		} else { newLabHour = hour+12; }
		var dString = "Δευτέρα Τρίτη Τετάρτη Πέμπτη Παρασκευή";
		var sDay = day;
		var tDay = dString.split(/ +/);
		var len = tDay.length;
		for(var i=0; i<len; i++){
			if(sDay == tDay[i].substr(0,3)){
				newLabDay = tDay[i];
				//console.log(i);
				break;
			}
		}
		
		
		oldLabName = parentDiv.find("h4>span.lab-name").text();
		var oldLabDate = parentDiv.find("h4>span.lab-date").text();
		
		var date = oldLabDate.split(" ");
		var day = date[0];
		var hour = parseInt(date[1], 10);
		var AmPm = date[2];
		if (AmPm == "π.μ.") {
			oldLabHour = hour;
		} else { oldLabHour = hour+12; }
		oldLabDay = day;
		
		/*
		console.log(newLabName);
		console.log(newLabDay);
		console.log(newLabHour);
		console.log("--------------");
		console.log(oldLabName);
		console.log(oldLabDay);
		console.log(oldLabHour);
		console.log("--------------");
		console.log("--------------");
		*/
		
		errorMsg = "Προέκυψε σφάλμα στην σύνδεση";
		amToSend = [];
		students = theActive.parents("div.lab").find("table tr:not(.disabled) td>input:checked");
		var i=0;
		students.each(function(){
			amToSend[i] = { am: $(this).val() };
			i++;
		});
		
		if (newLabName != oldLabName || newLabDay != oldLabDay || newLabHour != oldLabHour) {
			
			var request = {	lnew: [ { newName: newLabName, newDay: newLabDay, newHour: newLabHour} ],
							lold: [ {oldName: oldLabName, oldDay: oldLabDay, oldHour: oldLabHour} ],
							stud: amToSend
						};
			
			ajaxUrl = '/teachers/'+hashValue+'/submit-student-to-lab/';
			$.ajax({
				url: ajaxUrl,
				type: 'POST',
				contentType: 'application/json; charset=utf-8',
				data: $.toJSON(request),
				dataType: 'json',
				success: function(data) {
				   	if (data[0].status == 1){
				   		students.parents("tr").addClass("disabled").find("input").attr("disabled", "disabled");
						setTimeout( function() {
							msg.fadeOut(100).removeClass().addClass("ok").text(data[0].msg).fadeIn(200);
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
				},
				error: function(xhr, err){
					ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
	    				if(xhr.status==500){
	    					msg.fadeOut(100).removeClass().addClass("error").text(ms).fadeIn(200);
	    				}
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
	
	msg.ajaxComplete(function(){
		if(theActive) {
			theActive.hide();
			theActive.parent().removeClass("active");
		}
		$.scrollTo({top: 0}, 350, {axis:"y"});
		
	});



	//********************************
	//Ajax-Register-Lab Feature
	//********************************

	modalDiv = $("#osx-modal-data");
	lessonName = modalDiv.find("#select-lesson select[name='lesson-name']");
	lessonDay = modalDiv.find("#select-lab select[name='lesson-day']");
	lessonHour = modalDiv.find("#select-lab select[name='lesson-hour']");
	lessonClass = modalDiv.find("#select-class select[name='lesson-class']");
	
	lessonDay.attr("disabled", "disabled").parent("li").addClass("disabled");
	lessonHour.attr("disabled", "disabled");
	lessonClass.attr("disabled", "disabled").parent("li").hide();











































});

