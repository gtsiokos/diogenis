    
//********************************
//Ajax-Register-Lab Feature
//********************************
    
X$('TeacherRegister',
{
    $lab_registration       : undefined,
    $select                 :   {
                                  lesson:undefined,
                                  day:undefined,
                                  hour:{
                                         start:undefined,
                                         end:undefined
                                       },
                                  classroom:undefined,
                                  max_students:{
                                                 slider:undefined,
                                                 value:undefined
                                               }
                                },
    $modal_messages         : undefined,
    $submit_lab             : undefined,
    $loader                 : undefined,
    msg                     : {1:'ok', 2:'error', 3:'warning'},


    init: function() {
        var self = this;
        
        self.$lab_registration              = $('#lab-registration');
        self.$select.lesson                 = $('#select-lesson select[name="lesson-name"]');
        self.$select.day                    = $('#select-lab select[name="lesson-day"]');
        self.$select.hour.start             = $('#select-lab select[name="lesson-hour-start"]');
        self.$select.hour.end               = $('#select-lab select[name="lesson-hour-end"]');
        self.$select.classroom              = $('#select-class select[name="lesson-class"]');
        self.$select.max_students.slider    = $('#slider-max-students');
        self.$select.max_students.value     = $('#max-students');
        self.$modal_messages                = $('#modal-messages');
        self.$loader                        = $('#modal-loader');
        self.$submit_lab                    = $('#submit-lab');
        
        var spinner = X$('Helpers').get_spinner();
        self.$loader.spin(spinner.options);
        
        self.stepify().handle_events();
        
        return this;
    },
    
    
    remove_focus: function(){
        var self = this;
        self.$lab_registration.find('li.focused').removeClass('focused');
    },
    
    
    stepify: function(){
        var self = this;
        
        self.$select['day'].attr('disabled', 'disabled').parent('li').addClass('disabled');
        self.$select.hour['start'].attr('disabled', 'disabled');
        self.$select.hour['end'].attr('disabled', 'disabled');
        self.$select['classroom'].attr('disabled', 'disabled').parent('li').addClass('disabled').hide();
        self.$modal_messages.find('p').hide();
        self.$loader.hide();
        self.$select.max_students['slider'].slider({ range: 'min', min: 5, max: 40, value: 20,
                                slide: function( event, ui ) {
                                    self.$select.max_students['value'].val(ui.value);
                                }
                            });
        self.$select.max_students['value'].val( self.$select.max_students['slider'].slider('value') );
        self.$submit_lab.hide();
        
        self.$lab_registration.find('li>h3').click(function() {
            if ( $(this).parent('li').hasClass('isset') && !$(this).parent('li').hasClass('disabled') ){
                self.remove_focus();
                $(this).parent('li').addClass('focused').find('select').first().focus();
            }
            return false;
        });
        
        return this;
    },
    
    
    clean_messages: function() {
        var self = this;
        self.$modal_messages.find('p').fadeOut(100).delay(100).removeClass();
        
        return this;
    },
    
    show_message: function(status, new_msg, new_speed) {
        var self = this;
        var speed = new_speed || 150;
        
        self.clean_messages().$modal_messages.find('p').addClass(self.msg[status]).text(new_msg).fadeIn(speed);
    },
    
    handle_events: function(){
        var self = this,
            lesson,
            day,
            hour = {start: 0, end: 0},
            classroom;
        
        self.$select['lesson'].change(function() {
            var $this = $(this).find(':selected'),
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            lesson = ($this.val()) ? $this.data() : '';
            
            if ( step_is_not_set && lesson ){
                parent.removeClass('focused').addClass('isset');
                
                self.$select['day'].parent('li').removeClass('disabled').addClass('focused').addClass('isset');
                self.$select['day'].removeAttr('disabled').focus();
                self.$select.hour['start'].removeAttr('disabled');
                self.$select.hour['end'].removeAttr('disabled');
            }
            
            self.clean_messages();
        });
    
        self.$select['day'].change(function() {
            var parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');
            day = $(this).val();
            
            if( lesson && day && hour.start && hour.end ){
                self.submit({lesson:lesson, day:day, hour:hour});
            }
            self.clean_messages();
        });
    
        self.$select.hour['start'].change(function() {
            var start,
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');            
            start = $(this).attr('value') || 0;
            hour.start = parseInt(start, 10);
            
            if( lesson && day && hour.start && hour.end ){
                self.submit({lesson:lesson, day:day, hour:hour});
            }
            self.clean_messages();
        });
        
        self.$select.hour['end'].change(function() {
            var end,
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');
            end = $(this).attr('value') || 0;
            hour.end = parseInt(end, 10);
            
            if( lesson && day && hour.start && hour.end ){
                self.submit({lesson:lesson, day:day, hour:hour});
            }
            self.clean_messages();
        });

        this.$select['classroom'].change(function() {
            var $this = $(this).find(':selected'),
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');
            classroom = ($this.val()) ? $this.data() : '';
            
            self.clean_messages();
        });
    
        var submit_lab_request = function() {
            if ( lesson && day && hour.start && hour.end && classroom ) {
                self.$submit_lab.unbind('click');
                self.$modal_messages.find('p').hide().removeClass().siblings('img').fadeIn(50);
                self.submit({day:day, hour:hour, lesson:lesson, classroom:classroom});
                setTimeout( function() {
                    self.$submit_lab.bind('click', submit_lab_request);
                },1900);
            }
            else {
                var ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
                self.show_message(2, ms, 200);
            }
            return false;
        };
        self.$submit_lab.bind('click', submit_lab_request);
        
        return this;
    },


    submit: function(r) {
        var self = this,
            request,
            max_students = self.$select.max_students['slider'].slider('value');
        
        if (r['classroom']) { request = { action:'submit', course_id:r['lesson'].id, day:r['day'], hour:r['hour'], classroom_id:r['classroom'].id, max_students:max_students }; }
        else                { request = { action:'classes', course_id:r['lesson'].id, day:r['day'], hour:r['hour'] }; }
        
        var ajax_url = '/teachers/add-new-lab/';
        $.ajax({
            url: ajax_url,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(request),
            dataType: 'json',
            timeout: 10000,
            beforeSend: function() {
                if (request.action == 'submit') { self.$loader.show(); }
            },
            success: function(data) {
                try {
                    if (data.status == 1){

                        if (data.action == 'classes') {
                            self.$select['classroom'].children().not(':first-child').remove();
                            
                            var list_html = '';
                            for(var i=0, classroom; classroom=data.classes[i]; i++){
                                list_html += '<option data-id="'+classroom.id+'" value="'+classroom.name+'">'+classroom.name+'</option>';
                            }
                            self.$select['classroom'].append(list_html);
                            
                            var parentClass = self.$select['classroom'].parent('li');
                            var parentMeridiam = self.$select['day'].parent('li');
                    
                            parentClass.removeClass('disabled');
                            self.$select['classroom'].removeAttr('disabled');
                        
                            if ( !parentClass.hasClass('isset') ) {
                                parentClass.addClass('focused').addClass('isset');
                                parentMeridiam.removeClass('focused');
                            
                                var boxHeight = parentClass.height();
                                parentClass.children().hide();
                                parentClass.height(30).fadeIn(350,
                                                    function(){
                                                        $(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
                                                    });
                                self.$submit_lab.fadeIn(350);
                            
                                setTimeout( function() {
                                    self.$select['classroom'].focus();
                                },900);    
                            } else { self.$select['classroom'].focus(); }
                        }
                        else if (data.action == 'submit') {
                            self.$loader.hide();
                            self.$modal_messages.find('p').addClass('ok').text(data.msg)
                                                .append('<a href="#" onClick="window.location.reload()">ανανέωση</a>')
                                                .fadeIn(200);
                        }
                    }
                    else if (data.status == 2){
                
                        if (data.action == 'classes') {
                            self.show_message(data.status, data.msg, 200);
                        }
                        else if (data.action == 'submit') {
                            self.$loader.hide();
                            self.show_message(data.status, data.msg, 200);
                        }
                    }
                }
                catch(e) { this.error(); }
            },
            error: function(xhr, err){
                var ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
                //if(xhr.status==500)
                self.$loader.hide();
                self.show_message(2, ms, 200);
            }
        });
        
    }

});

