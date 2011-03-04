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
	
	var ajaxTrans 		= transfer.find("ul.labs-list li");
	var msg 			= $("#ui-messages p", "#content");
	var theLabs 		= $("div.lab", "#content");
	theLabs.find("table td>input").removeAttr("disabled").attr('checked', false);
		
	ajaxTrans.click(function(){
		
		var ms;
		var parentDiv = $(this).parents("div.lab");
		
		var newLabName, newLabDate, newLabDay, newLabHour;
		
		newLabName = $(this).find("span.name").text();
		var day = $(this).find("span.day").text();
		newLabDate = $(this).find("span.hour").text();
		var date = newLabDate.split(" ");
		var hour = parseInt(date[0], 10);
		var AmPm = date[1];
		if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
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
		
		
		var oldLabName, oldLabDate, oldLabDay, oldLabHour;
		
		oldLabName = parentDiv.find("h4>span.lab-name").text();
		oldLabDate = parentDiv.find("h4>span.lab-date").text();
		
		var splittedDate = X$('Helpers').splitDate(oldLabDate);
		oldLabDay = splittedDate.day;
		oldLabHour = splittedDate.hour;
		
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
		
		var errorMsg = "Προέκυψε σφάλμα στην σύνδεση";
		var amToSend = [];
		var students = theActive.parents("div.lab").find("table tr:not(.disabled) td>input:checked");
		var i=0;
		students.each(function(){
			amToSend[i] = { am: $(this).val() };
			i++;
		});
		
		if (amToSend[0]) {
			
			var request =	{
							lnew: [ { newName: newLabName, newDay: newLabDay, newHour: newLabHour} ],
							lold: [ {oldName: oldLabName, oldDay: oldLabDay, oldHour: oldLabHour} ],
							stud: amToSend
							};
			
			var ajaxUrl = '/teachers/'+X$('Helpers').getHash()+'/submit-student-to-lab/';
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
					catch (e) { this.error(); }
				},
				error: function(xhr, err){
					ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
    				//if(xhr.status==500)
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
			setTimeout( function() {
				msg.fadeOut(100).removeClass().addClass("warning").text(ms).fadeIn(200);
			},300);
			$.scrollTo({top: 0}, 500, {axis:"y"});
		}
		return false;
	});


});

