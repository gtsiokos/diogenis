    
//********************************
//
//********************************

X$('SchoolsLessons').extends('SchoolsEntries',
{
    $buttons:           {
	                    new_lesson: $('#new-lesson')
	                    },
	
	init: function() {
        var self = this;
        
        self.events = self.handle_events();
        self.rendering = self.handle_rendering();
        
        self.submit({type:'GET', action:'get'});
        self.listen_events();
        return this;
    },
    
    handle_events: function(){
        var self = this;
        
        var options = function(e){
            var $target = $(e.target),
                $parent = $target.parents('li.entry'),
                request = {},
                option =    {
                            edit: $target.hasClass('edit'),
                            save: $target.hasClass('save'),
                            'delete': $target.hasClass('delete')
                            };
            
            $parent.siblings().addClass('disabled').find('ul.ui-options').fadeOut(150);
            
            var classrooms = self.data.entries,
                classroom = $parent.data(),
                classroom_details = X$('JSON').get(classrooms, ':has(:root>.id:val("'+classroom.id+'"))');
                
            if(option['edit']) {
                self.rendering.edit.apply($parent, classroom_details)
            }
            if(option['save']) {
                var valid_entries;
                
                request =   {
                            'type':'POST',
                            'action':'post',
                            'id':classroom.id,
                            'name':$parent.find('span>input').val()
                            };
                
                valid_entries = check_valid_entries(request);
                if(valid_entries) self.submit(request);
            }
            if(option['delete']) {
                smoke.confirm('Θα διαγραφούν όλα τα εργαστήρια αυτού του μαθήματος. Θέλετε να συνεχίσετε;',function(e){
                    if(e){
                        request =   {
                                'type':'POST',
                                'params':[classroom.id],
                                'action':'delete',
                                'id':classroom.id
                                };
                        self.submit(request);
                    } else {
                        self.submit({type:'GET', action:'get'});
                        self.show_message(0, "Κονσόλα Μηνυμάτων", 200);
                    }
                }, {classname:'warning', ok:'Ναι, διάγραψε και τα εργαστήρια', cancel:'Όχι'});
            }
            
            return false;
        };
        
        var check_valid_entries = function(request){
            var msg = '';
            
            if(!request['name']) msg = "Συμπληρώστε το όνομα του μαθήματος";
            
            if(msg){
                self.show_message(3, msg, 200);
                return false;
            } else { return true; }
        };
        
        var new_lesson = function(){
            var $this = $this,
                msg = "Προσθέστε ένα μάθημα στο τμήμα σας";
            
            var context =   {   
                            entries: [ {id:false, 'name':"Όνομα Μαθήματος"} ]
                            };
            self.rendering.list(context);
            
            var $new_lesson = self.$entries.find('li:first');
            self.rendering.edit.apply($new_lesson, context.entries);
            self.show_message(0, msg, 200);
            
        };
        
        return {options:options, new_lesson:new_lesson};
    },
    
    handle_rendering: function(){
    	var self = this,
    	    render = X$('Helpers').render,
    	    templates = self.templates;
    	
    	var list = function(data){
    	    self.$entries.empty().append( render(templates.entries.list, data) );
    	};
    	
    	var edit = function(data){
    	    var $this = this;
    	    $this.addClass('active').empty().append( render(templates.entries.edit, data) ).show();
    	    X$('Sidebar').init();
    	};
    	
    	return {list:list, edit:edit};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        self.$entries.delegate('li ul.ui-options', 'click', events.options);
        self.$buttons.new_lesson.bind('click', events.new_lesson);
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
        
        var ajax_url = '/schools/'+self.user.username+'/lessons/';
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
                            //console.log(JSON.stringify(data.teachers));
                            self.rendering.list(data);
                            X$('Sidebar').init();
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
                //    console.log(i+': '+r[i]);
                //}
                //if(xhr.status==500)
                var msg = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
                self.show_message(2, msg, 200);
            }
        });
        
    }

});

