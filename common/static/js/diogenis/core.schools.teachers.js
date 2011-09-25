    
//********************************
//
//********************************
    
X$('SchoolsTeachers',
{
    user:               $('#content').data(),
    
    $teachers:			$('#teachers'),
	$messages:          $('#ui-messages'),
	$buttons:           {
	                    new_teacher: $('#new-teacher')
	                    },
	templates:          {
                        teachers:   {
                                    list:$('#list-tpl').html(),
                                    details:$('#details-tpl').html()
                                    }
                        },
    status:             {0:'', 1:'ok', 2:'error', 3:'warning'},
    
    init: function() {
        var self = this;
        
        self.events = self.handle_events();
        self.rendering = self.handle_rendering();
        
        self.submit({type:'GET', action:'get'});
        self.listen_events();
        return this;
    },
    
    show_message: function(status_id, msg, speed) {
        var self = this,
            speed = speed || 150,
            status = self.status[status_id];
            
        self.$messages.find('p').fadeOut(100, function(){
            $.scrollTo({top: 0}, 500, {axis:'y'});
            $(this).removeClass().addClass(status).text(msg).fadeIn(speed);
        });
    },
    
    handle_events: function(){
        var self = this;
        
        var options = function(e){
            var $target = $(e.target),
                $parent = $target.parents('li.teacher'),
                request = {},
                option =    {
                            edit: $target.hasClass('edit'),
                            'delete': $target.hasClass('delete'),
                            save: $target.hasClass('save')
                            };
            
            var teachers = self.data.teachers,
                teacher = $parent.data(),
                teacher_details = X$('JSON').get(teachers, ':has(:root>.id:val("'+teacher.id+'"))');
            
            if(option['edit']) { // Hardcoded Solution
                var $options = $parent.find('ul.ui-options li'),
                    $details = $parent.find('div.details'),
                    $password = {
                                label: $details.find('div.entry.input-password label'),
                                input: $details.find('div.entry.input-password input')
                                };
                
                $parent.siblings().addClass('disabled').find('ul.ui-options').fadeOut(150);
                $options.not(':first').remove();
                $options.find('a').removeClass('edit').addClass('save').text('Αποθήκευση');
                
                $password.label.addClass('as-link').text("Αλλαγή Κωδικού");
                $password.input.hide();
                
                $password.label.click(function(){
                    $password.label.text("Νέος Κωδικός").removeClass('as-link');
                    $password.input.show();
                });
                
                $details.find('#courses').chosen().change( function(){ X$('Sidebar').init(); } );
                
                $parent.addClass('active');
                $details.show();
                X$('Sidebar').init();
            }
            if(option['save']) {
                var courses = [],
                    valid_entries,
                    $courses = $parent.find('#courses option');
                
                for(var i=0, course, $course; course=$courses[i]; i++){
                    $course = $(course);
                    if( $course.is(':selected') ){
                        courses.push( {id:$course.data('id'), selected:true} );
                    } else {
                        courses.push( {id:$course.data('id')} );
                    }
                }
                request =   {
                            'type':'POST',
                            'action':'post',
                            'id':$parent.data('id'),
                            'username':$parent.find('#teacher-username').val(),
                            'password':$parent.find('#teacher-password').val(),
                            'firstname':$parent.find('#teacher-firstname').val(),
                            'lastname':$parent.find('#teacher-lastname').val(),
                            'courses':courses
                            };
                
                valid_entries = check_valid_entries(request);
                if(valid_entries) self.submit(request);
            }
            if(option['delete']) {
                smoke.confirm('Θα διαγραφούν όλα τα εργαστήρια του καθηγητή. Θέλετε να συνεχίσετε;',function(e){
                    if(e){
                        request = {
                                'type':'POST',
                                'params':[teacher.id],
                                'action':'delete',
                                'id':teacher.id
                                };
                        self.submit(request);
                    } //else { self.show_message(0, "Κονσόλα Μηνυμάτων", 200); }
                }, {classname:'warning', ok:'Ναι, διάγραψε και τα εργαστήρια', cancel:'Όχι'});
            }
            
            return false;
        };
        
        var check_valid_entries = function(request){
            var msg = '';
            
            X$('JSON').get( request.courses,
                            ':has(:root>.selected)',
                            function(){
                                if(!this[0]) msg = "Επιλέξτε τα μαθήματα του καθηγητή";                                   
                            });
            if(!request.lastname) msg = "Συμπληρώστε το Επώνυμο";
            if(!request.firstname) msg = "Συμπληρώστε το Όνομα";
            if(!request.id && !request.password) msg = "Συμπληρώστε τον Κωδικό";
            if(!request.username) msg = "Συμπληρώστε το Username";
            
            if(msg){
                self.show_message(3, msg, 200);
                return false;
            } else { return true; }
        };
        
        var focus_entry = function(e){
            var $target = $(e.target),
                $details = $target.parents('div.details');
            
            $details.find('div.entry').removeClass('active');
            $target.parents('div.entry').addClass('active');
        }
        
        var new_teacher = function(){
            var $this = $this,
                msg = "Επιλέξτε τα μαθήματα για τα οποία έχει εργαστήρια ο καθηγητής";
            
            var context =   {   
                            teachers: [ {id:false, courses:self.data.courses} ]
                            };
            self.rendering.list(context);
            self.$teachers.find('li:first').addClass('active').find('div.details').show().find('#courses').chosen().change( function(){ X$('Sidebar').init(); } );
            //var $new_teacher = self.$teachers.find('li:first');
            //self.rendering.details.apply($new_teacher, context.teachers);
            self.show_message(0, msg, 200);
            
        };
        
        return {options:options, new_teacher:new_teacher, focus_entry:focus_entry};
    },
    
    handle_rendering: function(){
    	var self = this,
    	    render = X$('Helpers').render,
    	    templates = self.templates;
    	
    	var list = function(data){
    	    var teachers_list_created = self.$teachers.empty().append( render(templates.teachers.list, data) );
    	    
    	    var interval = setInterval(function(){
    	        if(teachers_list_created){
    	            X$('Sidebar').init();
    	            clearInterval(interval);
    	        }
    	    }, 5);
    	};
    	
    	return {list:list};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        self.$teachers.delegate('li ul.ui-options', 'click', events.options);
        self.$buttons.new_teacher.bind('click', events.new_teacher);
        self.$teachers.delegate('label', 'click', events.focus_entry);
        self.$teachers.delegate('input', 'click', events.focus_entry);
    },
    
    
	submit: function(r) {
        var self = this,
            request,
            type;
        
        if (r['type'] === 'GET'){
            type = r.type;
            request = {action:r.action};
        } else {
            type = r.type;
            request = JSON.stringify(r);
        }
        
        var ajax_url = '/schools/'+self.user.username+'/teachers/';
        if(r.params) ajax_url += r.params.join('/')+'/';
        
        $.ajax({
            url: ajax_url,
            type: type,
            contentType: 'application/json; charset=utf-8',
            data: request,
            dataType: 'json',
            timeout: 10000,
            beforeSend: function() {
                var a =2;
            },
            success: function(data) {
                try {
                    if (data.status == 1){

                        if (data.action === 'get') {
                            self.data = data;
                            self.rendering.list(data);
                        } else {
                            self.submit({type:'GET', action:'get'});
                            self.show_message(data.status, data.msg, 200);
                        }
                    }
                    else if (data.status == 2){
                        self.submit({type:'GET', action:'get'});
                        self.show_message(data.status, data.msg, 200);
                    }
                }
                catch(e) { this.error(); }
            },
            error: function(xhr, err){
                //for(i in r){
                //   console.log(i+': '+r[i]);
                //}
                //if(xhr.status==500)
                var msg = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
                self.show_message(2, msg, 200);
            }
        });
        
    }

});

