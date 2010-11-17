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
		
		
		oldLabName = parentDiv.find("h4>span.lab-name").text();
		var oldLabDate = parentDiv.find("h4>span.lab-date").text();
		
		var date = oldLabDate.split(" ");
		var day = date[0];
		var hour = parseInt(date[1], 10);
		var AmPm = date[2];
		if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
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
				   		students.parents("tr").addClass("disabled", 80).find("input").attr("disabled", "disabled");
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
	
	
	var labList 		= $("#lab-registration");
	var lessonName 		= $("#select-lesson select[name='lesson-name']");
	var lessonDay 		= $("#select-lab select[name='lesson-day']");
	var lessonHour 		= $("#select-lab select[name='lesson-hour']");
	var lessonClass 	= $("#select-class select[name='lesson-class']");
	var maxSlider 		= $("#slider-max-students");
	var modalMsg 		= $("#modal-messages");
	var submitLab 		= $("#submit-lab");
	
	lessonDay.attr("disabled", "disabled").parent("li").addClass("disabled");
	lessonHour.attr("disabled", "disabled");
	lessonClass.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
	modalMsg.find("#modal-loader").hide().siblings("p").hide();
	maxSlider.slider({ 	range: "min", min: 5, max: 40, value: 20,
						slide: function( event, ui ) {
							$("#max-students").val(ui.value);
						}
					});
	$("#max-students").val( maxSlider.slider("value") );
	
	submitLab.hide();
	
	
	labList.find("li>h3").click(function() {
		if ( $(this).parent("li").hasClass("isset") && !$(this).parent("li").hasClass("disabled") ){
			labList.find("li.focused").removeClass("focused");
			$(this).parent("li").addClass("focused").find("select").first().focus();
		}
		return false;
	});
	
	
	var lessonToSend, dayToSend, hourToSend, classToSend;
	var theRequest = function(lessonToSend, dayToSend, hourToSend, classToSend){
		
		if (classToSend) { var request = { newLesson: [{ action: "submitLab", newName: lessonToSend, newDay: dayToSend, newHour: hourToSend, newClass: classToSend}] }; }
		else { var request = { newLesson: [{ action: "getClass", newName: lessonToSend, newDay: dayToSend, newHour: hourToSend}] }; }
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
							$("body").addClass("wait");
						
							var boxHeight = parentClass.height();
							parentClass.children().hide();
							parentClass.height(30).fadeIn(350,
												function(){
													$(this).animate({height: boxHeight}, 350);
												});
							submitLab.fadeIn(350);
							setTimeout( function() {
								parentClass.children().fadeIn(350);
							},710);
						} else {
							$("body").addClass("wait");
							modalMsg.find("p").fadeOut(100);
						}
						
						setTimeout( function() {
							lessonClass.focus();
							$("body").removeClass("wait");
							modalMsg.find("p").removeClass();
						},720);
					}
					else if (data[0].action == "submitLab") {
						modalMsg.find("#modal-loader").fadeOut(150, function(){
																modalMsg.find("p")
																.removeClass().addClass("ok")
																.text(data[0].msg).append("<a href='#' onClick='window.location.reload()'>Ανανέωση</a>")
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
																.removeClass().addClass("error")
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
						modalMsg.find("p").fadeOut(100).removeClass().addClass("error").text(ms).fadeIn(200);
					},400);
				}
			}
		});
		
	};
	
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
		if( lessonToSend && dayToSend && hourToSend ){
			theRequest(lessonToSend, dayToSend, hourToSend);
		}
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
		if( lessonToSend && dayToSend && hourToSend ){
			theRequest(lessonToSend, dayToSend, hourToSend);
		}
	});

	lessonClass.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
		
			classToSend = $(this).val();
			hisParent.addClass("isset");
		
		} else {
			classToSend = $(this).val();
		}
		
	});

	submitLab.click(function() {
		if ( lessonToSend && dayToSend && hourToSend && classToSend ) {
			modalMsg.find("p").hide().siblings("img").fadeIn(50);
			theRequest(lessonToSend, dayToSend, hourToSend, classToSend);
		} else { alert("Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου"); }
	
	
		return false;
	});


























});

