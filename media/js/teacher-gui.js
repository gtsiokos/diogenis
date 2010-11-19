$(function(){

	//********************************
	//Find Login Hash
	//********************************	
	
	var hashValue = $("input[type='hidden']", "#login").val();
	
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
	//Global Ajax Behaviour
	//********************************		
	
	var theBody = $("body:first");
	
	theBody.ajaxStart(function(){
		theBody.addClass("wait");
	});
	theBody.ajaxComplete(function(){
		theBody.removeClass("wait");
	});
	
	var splitOldDate = function(oldLabDate) {
		var date = oldLabDate.split(" ");
		var day = date[0];
		var hour = parseInt(date[1], 10);
		var AmPm = date[2];
		if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
			hour = hour;
		} else { hour = hour+12; }
		
		return {day:day, hour:hour};
	}
	
	//********************************
	//Ajax-Transfer Feature
	//********************************	
	
	
	var ajaxTrans 		= transfer.find("ul.labs-list li");
	var msg 			= $("#ui-messages p", "#content");
	var theLabs 		= $("div.lab", "#content");
	var pdfLink 		= theLabs.find("div.extras:first a.export-pdf");
	theLabs.find("table td>input").removeAttr("disabled").attr('checked', false);
	
	pdfLink.click(function() {
		var parentDiv = $(this).parents("div.lab");
		var labName = parentDiv.find("h4>span.lab-name").text();
		var labDate = parentDiv.find("h4>span.lab-date").text();
		
		var splittedDate = splitOldDate(labDate);
		var labDay = splittedDate.day;
		var labHour = splittedDate.hour;
		
		//console.log(labName+"-||-"+labDay+"-||-"+labHour);
		
		var request = {	pdfRequest: [{ labName: labName, labDay: labDay, labHour: labHour}] };
			
		ajaxUrl = '/teachers/'+hashValue+'/export-pdf/';
		$.ajax({
			url: ajaxUrl,
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			data: $.toJSON(request),
			dataType: 'json',
			success: function(data) {
				if ( data[0].status == 2 ) {
					setTimeout( function() {
						msg.fadeOut(100).removeClass().addClass("error").text(data[0].msg).fadeIn(200);
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
		
		return false;
	});
	
	ajaxTrans.click(function(){
		
		var ms;
		var parentDiv = $(this).parents("div.lab");
		
		
		var newLabName, newLabDate, newLabDay, newLabHour
		
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
		
		
		var oldLabName, oldLabDate, oldLabDay, oldLabHour
		
		oldLabName = parentDiv.find("h4>span.lab-name").text();
		oldLabDate = parentDiv.find("h4>span.lab-date").text();
		
		var splittedDate = splitOldDate(oldLabDate);
		var oldLabDay = splittedDate.day;
		var oldLabHour = splittedDate.hour;
		
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
				},
				error: function(xhr, err){
					ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
    				if(xhr.status==500){
    					msg.fadeOut(100).removeClass().addClass("error").text(ms).fadeIn(200);
    				}
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
	
	



	//********************************
	//Ajax-Register-Lab Feature
	//********************************
	
	
	var labList 		= $("#lab-registration");
	var lessonName 		= $("#select-lesson select[name='lesson-name']");
	var lessonDay 		= $("#select-lab select[name='lesson-day']");
	var lessonHour 		= $("#select-lab select[name='lesson-hour']");
	var lessonClass 	= $("#select-class select[name='lesson-class']");
	var maxSlider 		= $("#slider-max-students");
	var maxStudents 	= $("#max-students")
	var modalMsg 		= $("#modal-messages");
	var submitLab 		= $("#submit-lab");
	
	lessonDay.attr("disabled", "disabled").parent("li").addClass("disabled");
	lessonHour.attr("disabled", "disabled");
	lessonClass.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
	modalMsg.find("#modal-loader").hide().siblings("p").hide();
	maxSlider.slider({ 	range: "min", min: 5, max: 40, value: 20,
						slide: function( event, ui ) {
							maxStudents.val(ui.value);
						}
					});
	maxStudents.val( maxSlider.slider("value") );
	submitLab.hide();
	
	
	labList.find("li>h3").click(function() {
		if ( $(this).parent("li").hasClass("isset") && !$(this).parent("li").hasClass("disabled") ){
			labList.find("li.focused").removeClass("focused");
			$(this).parent("li").addClass("focused").find("select").first().focus();
		}
		return false;
	});
	
	
	var lessonToSend, dayToSend, hourToSend, classToSend;
	var theRequest = function(dayToSend, hourToSend, lessonToSend, classToSend) {
		
		var maxToSend = maxSlider.slider("value");
		
		if (classToSend) { var request = { newLesson: [{ action: "submitLab", newName: lessonToSend, newDay: dayToSend, newHour: hourToSend, newClass: classToSend, maxStudents: maxToSend}] }; }
		else { var request = { newLesson: [{ action: "getClass", newDay: dayToSend, newHour: hourToSend}] }; }
		ajaxUrl = '/teachers/'+hashValue+'/add-new-lab/';
		
		$.ajax({
			url: ajaxUrl,
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			data: $.toJSON(request),
			dataType: 'json',
			success: function(data) {
				if (data[0].status == 1){

					if (data[0].action == "getClass") {
						lessonClass.children().not(":first-child").remove();
						var len = data[0].classes.length;
						for(var i=0; i<len; i++){
							var str = "<option value='"+data[0].classes[i].name+"'>"+data[0].classes[i].name+"</option>";
							lessonClass.append(str);
						}
						var parentClass = lessonClass.parent("li")
						var parentMeridiam = lessonDay.parent("li")
					
						parentClass.removeClass("disabled");
						lessonClass.removeAttr("disabled");
						
						if ( !parentClass.hasClass("isset") ) {
							parentClass.addClass("focused").addClass("isset");
							parentMeridiam.removeClass("focused");
							
							var boxHeight = parentClass.height();
							parentClass.children().hide();
							parentClass.height(30).fadeIn(350,
												function(){
													$(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
												});
							submitLab.fadeIn(350);
							
							setTimeout( function() {
								lessonClass.focus();
							},900);	
						} else { lessonClass.focus(); }
					}
					else if (data[0].action == "submitLab") {
						modalMsg.find("#modal-loader").fadeOut(150, function(){
																modalMsg.find("p")
																.addClass("ok")
																.text(data[0].msg).append("<a href='#' onClick='window.location.reload()'>ανανέωση</a>")
																.fadeIn(200);
															}
														);
					}
				}
				else if (data[0].status == 2){
				
					if (data[0].action == "getClass") {
						modalMsg.find("p").addClass("error").text(data[0].msg).fadeIn(200);
					}
					else if (data[0].action == "submitLab") {
						modalMsg.find("#modal-loader").fadeOut(150, function(){
																modalMsg.find("p")
																.addClass("error")
																.text(data[0].msg)
																.fadeIn(200);
															}
														);
					}
				}
			},
			error: function(xhr, err){
				ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
				if(xhr.status==500){
					modalMsg.find("#modal-loader").fadeOut(150);
					setTimeout( function() {
						modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
					},400);
				}
			}
		});
		
	};
	
	var cleanMessages = function() {
		modalMsg.find("p").fadeOut(100).delay(100).removeClass();
	}
	
	lessonName.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
		
			hisParent.removeClass("focused");
			lessonToSend = $(this).val();
			
			lessonDay.parent("li").removeClass("disabled").addClass("focused").addClass("isset");
			lessonDay.removeAttr("disabled").focus();
			lessonHour.removeAttr("disabled");
			
			hisParent.addClass("isset");	
		} else {
			lessonToSend = $(this).val();
		}
		cleanMessages();
	});
	
	lessonDay.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
		
			dayToSend = $(this).val();
			
			if( !hisParent.hasClass("isset" ) ) {
				hisParent.addClass("isset");
			}
			
		} else {
			dayToSend = $(this).val();
		}
		if( dayToSend && hourToSend ){
			classToSend = null;
			theRequest(dayToSend, hourToSend);
		}
		cleanMessages();
	});
	
	lessonHour.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
		
			hourToSend = $(this).attr("value");
			
			if( !hisParent.hasClass("isset" ) ) {
				hisParent.addClass("isset");
			}
			
		} else {
			hourToSend = $(this).attr("value");
		}
		if( dayToSend && hourToSend ){
			classToSend = null;
			theRequest(dayToSend, hourToSend);
		}
		cleanMessages();
	});

	lessonClass.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
		
			classToSend = $(this).val();
			hisParent.addClass("isset");
		
		} else {
			classToSend = $(this).val();
		}
		cleanMessages();
	});
	
	var submitLabRequest = function() {
		if ( lessonToSend && dayToSend && hourToSend && classToSend ) {
			submitLab.unbind("click");
			modalMsg.find("p").hide().removeClass().siblings("img").fadeIn(50);
			theRequest(dayToSend, hourToSend, lessonToSend, classToSend);
			setTimeout( function() {
				submitLab.bind("click", submitLabRequest);
			},1500);
		}
		else {
			ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
			cleanMessages();
			modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
		}
		return false;
	}
	submitLab.bind("click", submitLabRequest);


























});

