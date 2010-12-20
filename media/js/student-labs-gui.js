$(function(){

	//********************************
	//Find Login Hash
	//********************************	
	
	var hashValue = $("input[type='hidden']", "#login").val();
	
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
	//Ajax-Register-Lab Feature
	//********************************
	
	var labList 		= $("#lab-registration");
	var lessonName 		= $("#select-lesson select[name='lesson-name']");
	var lessonTeacher	= $("#select-teacher select[name='lesson-teacher']");
	var lessonClass 	= $("#select-class select[name='lesson-class']");
	var modalMsg 		= $("#modal-messages");
	var submitLab 		= $("#submit-lab");
	
	lessonTeacher.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
	lessonClass.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
	modalMsg.find("#modal-loader").hide().siblings("p").hide();
	submitLab.hide();
	
	labList.find("li>h3").click(function() {
		if ( $(this).parent("li").hasClass("isset") && !$(this).parent("li").hasClass("disabled") ){
			labList.find("li.focused").removeClass("focused");
			$(this).parent("li").addClass("focused").find("select").first().focus();
		}
		return false;
	});
	
	var lessonToSend, teacherToSend, classToSend;
	var theRequest = function(lessonToSend, teacherToSend, classToSend) {
		
		if (lessonToSend && teacherToSend && classToSend){
		
		}
		else if (lessonToSend && teacherToSend){
		
		}
		else if (lessonToSend){
			var request = { action: "getTeachers", lesson: lessonToSend };
		}
		
		ajaxUrl = '/students/'+hashValue+'/add-new-lab/';
		
		$.ajax({
			url: ajaxUrl,
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			data: $.toJSON(request),
			dataType: 'json',
			success: function(data) {
				if (data[0].status == 1){

					if (data[0].action == "getTeachers") {
						lessonTeacher.children().not(":first-child").remove();
						var len = data[0].teachers.length;
						for(var i=0; i<len; i++){
							var str = "<option value='"+data[0].teachers[i].name+"'>"+data[0].teachers[i].name+"</option>";
							lessonTeacher.append(str);
						}
						var parentClass = lessonTeacher.parent("li")
						
						parentClass.removeClass("disabled");
						
						if ( !parentClass.hasClass("isset") ) {
							parentClass.addClass("focused").addClass("isset");
							
							var boxHeight = parentClass.height();
							parentClass.children().hide();
							parentClass.height(30).fadeIn(350,
												function(){
													$(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
												});
							submitLab.fadeIn(350);
							
							setTimeout( function() {
								lessonTeacher.focus();
							},900);	
						} else { lessonTeacher.focus(); }
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
			
			lessonTeacher.parent("li").removeClass("disabled").addClass("focused").addClass("isset").show();
			lessonTeacher.removeAttr("disabled").focus();
			
			hisParent.addClass("isset");	
		} else {
			lessonToSend = $(this).val();
		}
		theRequest(lessonToSend);
		
		cleanMessages();
	});
	
	/*
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
			},1900);
		}
		else {
			ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
			cleanMessages();
			modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
		}
		return false;
	}
	submitLab.bind("click", submitLabRequest);
	*/

























});

