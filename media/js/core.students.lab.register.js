	
//********************************
//Ajax-Register-Lab Feature
//********************************

X$('StudentRegister',
{
	labList 		: undefined,
	lessonName 		: undefined,
	lessonTeacher	: undefined,
	lessonClass 	: undefined,
	modalMsg 		: undefined,
	submitLab 		: undefined,


	init: function() {
		var _self = this;
		
		_self.labList 			= $("#lab-registration");
		_self.lessonName 		= $("#select-lesson select[name='lesson-name']");
		_self.lessonTeacher		= $("#select-teacher select[name='lesson-teacher']");
		_self.lessonClass 		= $("#select-class select[name='lesson-class']");
		_self.modalMsg 			= $("#modal-messages");
		_self.submitLab 		= $("#submit-lab");
		
		_self.stepify().setEvents();
		
		return this;
	},
	
	
	removeFocus: function(){
		var _self = this;
		_self.labList.find("li.focused").removeClass("focused");
	},
	
	
	stepify: function(){
		var _self = this;
		
		_self.lessonTeacher.attr("disabled", "disabled").parent("li").addClass("disabled");
		_self.lessonClass.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
		_self.modalMsg.find("#modal-loader").hide().siblings("p").hide();
		_self.submitLab.hide();

		_self.labList.find("li>h3").click(function() {
			if ( $(this).parent("li").hasClass("isset") && !$(this).parent("li").hasClass("disabled") ){
				_self.removeFocus();
				$(this).parent("li").addClass("focused").find("select").first().focus();
			}
			return false;
		});
		
		return this;
	},
	
	
	cleanMessages: function() {
		var _self = this;
		_self.modalMsg.find("p").fadeOut(100).delay(100).removeClass();
	},
	
	
	setEvents: function(){
		var _self = this;
		var lessonToSend, teacherToSend, classToSend, submitRequest;
		
		_self.lessonName.change(function() {
			var hisParent = $(this).parent("li");
			if ( !hisParent.hasClass("isset") ){
				lessonToSend = $(this).val();
				hisParent.addClass("isset");	
			} else {
				lessonToSend = $(this).val();
			}
			if( lessonToSend ){
				_self.submit(lessonToSend);
			}
		
			_self.submitLab.hide();
			_self.cleanMessages();
		});
	
		_self.lessonTeacher.change(function() {
			var hisParent = $(this).parent("li");
			if ( !hisParent.hasClass("isset") ){
				teacherToSend = $(this).val();
				hisParent.addClass("isset");	
			} else {
				teacherToSend = $(this).val();
			}
			if( lessonToSend && teacherToSend ){
				classToSend = null;
				_self.submit(lessonToSend, teacherToSend);
			}
			_self.cleanMessages();
		});
	
		_self.lessonClass.change(function() {
			var hisParent = $(this).parent("li");
			if ( !hisParent.hasClass("isset") ){
				classToSend = $(this).val();
				hisParent.addClass("isset");
			} else {
				classToSend = $(this).val();
			}
			if( lessonToSend && teacherToSend && classToSend ){
				_self.submit(lessonToSend, teacherToSend, classToSend, 0);
			}
			_self.cleanMessages();
		});
	
		var submitLabRequest = function() {
			if ( lessonToSend && teacherToSend && classToSend ) {
				_self.submitLab.unbind("click");
				_self.modalMsg.find("p").hide().removeClass().siblings("img").fadeIn(50);
				_self.submit(lessonToSend, teacherToSend, classToSend, 1);
				setTimeout( function() {
					_self.submitLab.bind("click", submitLabRequest);
				},1900);
			}
			else {
				var ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
				_self.cleanMessages();
				_self.modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
			}
			return false;
		};
		_self.submitLab.bind("click", submitLabRequest);
		
		return this;
	},


	submit: function(lessonToSend, teacherToSend, classToSend, submitRequest) {
		var _self = this,
			request;
		
		if (lessonToSend && teacherToSend && classToSend){
			var classInfo 	= classToSend.split(" ");
			var classDate 	= X$('Helpers').splitDate(classToSend);
			var className 	= classInfo[3];
			var classDay 	= classDate.day;
			var classHour 	= classDate.hour;
			if ( submitRequest===0 ) {
				request = { action:"checkAvailability", lesson:lessonToSend, teacher:teacherToSend, cname:className, cday:classDay, chour:classHour };
			}
			else { request = { action:"submitLab", lesson:lessonToSend, teacher:teacherToSend, cname:className, cday:classDay, chour:classHour }; }
		}
		else if (lessonToSend && teacherToSend){
			request = { action:"getClasses", lesson:lessonToSend, teacher:teacherToSend };
		}
		else if (lessonToSend){
			request = { action:"getTeachers", lesson:lessonToSend };
		}
		
		var ajaxUrl = '/students/'+X$('Helpers').getHash()+'/add-new-lab/';
		$.ajax({
			url: ajaxUrl,
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			data: $.toJSON(request),
			dataType: 'json',
			beforeSend: function() {
				if (request.action == "submitLab") { _self.modalMsg.find("#modal-loader").show(); }
			},
			success: function(data) {
				if (data[0].status == 1){
					var strHtml;
					
					if (data[0].action == "getTeachers") {
						_self.lessonTeacher.children().not(":first-child").remove();
						_self.lessonClass.attr("disabled", "disabled").parent("li")
																	.removeClass("isset").hide().end()
																	.children().not(":first-child").remove();
						var len = data[0].teachers.length;
						for(var i=0; i<len; i++){
							strHtml += "<option value='"+data[0].teachers[i].name+"'>"+data[0].teachers[i].name+"</option>";
						}
						_self.lessonTeacher.append(strHtml);
						
						var parentClass = _self.lessonTeacher.parent("li");
						parentClass.removeClass("disabled");
						
						_self.removeFocus();
						if ( !parentClass.hasClass("isset") ) {
							parentClass.addClass("focused").addClass("isset");
							_self.lessonTeacher.removeAttr("disabled");
							
							setTimeout( function() {
								_self.lessonTeacher.focus();
							},900);	
						} else { parentClass.addClass("focused"); _self.lessonTeacher.focus(); }
					}
					else if (data[0].action == "getClasses") {
						_self.lessonClass.children().not(":first-child").remove();
						var len = data[0].classes.length;
						for(var i=0; i<len; i++){
							var str 	= data[0].classes[i].day+" - "+data[0].classes[i].hour+" - "+data[0].classes[i].name;
							var strVal 	= data[0].classes[i].day+" "+data[0].classes[i].hour+" "+data[0].classes[i].name;
							strHtml += "<option value='"+strVal+"'>"+str+"</option>";
						}
						_self.lessonClass.append(strHtml);
						
						var parentClass = _self.lessonClass.parent("li");
						parentClass.removeClass("disabled");
						
						_self.removeFocus();
						if ( !parentClass.hasClass("isset") ) {
							parentClass.addClass("focused").addClass("isset");
							_self.lessonClass.removeAttr("disabled");
							
							var boxHeight = parentClass.height();
							parentClass.children().hide();
							parentClass.height(30).fadeIn(350,
												function(){
													$(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
												});
							
							setTimeout( function() {
								_self.lessonClass.focus();
							},900);
						} else { parentClass.addClass("focused"); _self.lessonClass.focus(); }
					}
					else if (data[0].action == "checkAvailability") {
						_self.submitLab.text("Υποβολή").fadeIn(350);
					}
					else if (data[0].action == "submitLab") {
						_self.modalMsg.find("#modal-loader").fadeOut(150, function(){
																_self.modalMsg.find("p")
																.addClass("ok")
																.text(data[0].msg).append("<a href='#' onClick='window.location.reload()'>ανανέωση</a>")
																.fadeIn(200);
															}
														);
					}
				}
				else if (data[0].status == 3){
					if (data[0].action == "checkAvailability") {
						_self.modalMsg.find("p").addClass("warning").text(data[0].msg).fadeIn(200);
						_self.submitLab.text("Υποβολή Αιτήματος").fadeIn(350);
					}
				}
				else if (data[0].status == 2){
				
					if (data[0].action == "getTeachers") {
						_self.modalMsg.find("p").addClass("error").text(data[0].msg).fadeIn(200);
					}
					else if (data[0].action == "getClasses") {
						_self.lessonClass.attr("disabled", "disabled").children().not(":first-child").remove();
						_self.submitLab.hide();
						_self.lessonClass.parent("li").hide().removeClass("isset").removeClass("focused").addClass("disabled");
						_self.modalMsg.find("p").addClass("error").text(data[0].msg).fadeIn(200);
					}
					else if (data[0].action == "submitLab") {
						_self.modalMsg.find("#modal-loader").fadeOut(150, function(){
																_self.modalMsg.find("p")
																.addClass("error")
																.text(data[0].msg)
																.fadeIn(200);
															}
														);
					}
				}
			},
			error: function(xhr, err){
				var ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
				if(xhr.status==500){
					_self.modalMsg.find("#modal-loader").fadeOut(150);
					setTimeout( function() {
						_self.modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
					},400);
				}
			}
		});
		
	}

});
