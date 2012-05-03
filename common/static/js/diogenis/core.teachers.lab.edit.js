
X$('StudentEdit',
{
    $labs:          $('div.lab', '#content'),
    $messages:      $('#ui-messages'),
    $dropdown:      $('div.lab span.edit.enabled', '#content'),
    
    url:            undefined,
    $students:      [],
    lab:            { 'new': {}, 'old': {} },
    status:         {0:'', 1:'ok', 2:'error', 3:'warning'},
    
    init: function(){
        var self = this;
        
        self.url = self.get_url();
        self.events = self.handle_events();
        self.listen_events();
        
        self.$labs.find('table').tablesorter({
                                            //sortList: [[1,0]],
                                            headers: { 0: {sorter: false}, 3: {sorter: false}, 4: {sorter: false} }
                                            });
        self.$labs.find('table td>input').removeAttr('disabled').attr('checked', false);
        
        return this;
    },
    
    show_message: function(status_id, msg, speed) {
        var self = this,
            speed = speed || 150,
            status = self.status[status_id];
            
        self.$messages.find('p').fadeOut(100, function(){
            $.scrollTo({top: 0}, 500, {axis:'y'});
            $(this).removeClass().addClass(status).html(msg).fadeIn(speed);
        });
    },
    
    handle_events: function(){
        var self = this,
            edit_options;
        
        edit_options = function(e){
            var $target = $(e.target),
                $lab = $target.parents('div.lab'),
                students = self.get_checked_students.call($lab[0], {}),
                lab = {},
                request = {},
                option =    {
                            transfer: $target.parents('ul.transfer').hasClass('transfer'),
                            'delete': $target.hasClass('delete')
                            };
                
                if(!students[0] && (option['transfer'] || option['delete'])){
                    X$('DropdownWidget').events.dropdown.hide();
                    self.show_message(3, "Δεν έχετε επιλέξει κάποιον σπουδαστή", 200);
                } else {
                    
                    if(option['transfer']){
                        lab['new'] = $target.parents('li').data() || $target.data();
                        lab['old'] = $lab.data();
                        
                        request = {lab:lab, students:students, action:'transfer'};
                        
                        if(self.url === 'pending'){
                            try {
                            _gaq.push(['_trackEvent', 'StudentEdit', 'Transferred Pending', students.length+' students']);
                            } catch(e) {}
                        } else {
                            try {
                            _gaq.push(['_trackEvent', 'StudentEdit', 'Transferred', students.length+' students']);
                            } catch(e) {}
                        }
                        
                        self.submit(request);
                    }
                    
                    if(option['delete']){
                        smoke.confirm('Θα πρέπει να ενημερωθούν οι φοιτητές για την διαγραφή τους από την ομάδα. Θέλετε να συνεχίσετε;',function(e){
                            if(e){
                                request = {students:students, action:'delete'};
                                
                                try {
                                _gaq.push(['_trackEvent', 'StudentEdit', 'Deleted', students.length+' students']);
                                } catch(e) {}
                                
                                self.submit(request);
                            } else {
                                try {
                                _gaq.push(['_trackEvent', 'StudentEdit', 'Canceled Delete', students.length+' students']);
                                } catch(e) {}
                            }
                        }, {classname:'warning', ok:'Ναι, διάγραψε τις εγγραφές', cancel:'Όχι'});
                    }
                    
                    
                }
        };
        
        return {edit_options:edit_options};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        self.$dropdown.delegate('div.edit-widget', 'click', events.edit_options);
        
        return this;
    },
    
    get_checked_students: function(){
        var self = X$('StudentEdit'),
            students_id = [],
            $students = $(this).find('table tr:not(.disabled) td>input:checked');
        
        self.$students = $students;
        for(var i=0, student; student=$students[i]; i++){
            students_id[i] = $(student).data();
        }
        return students_id;
    },
    
    submit: function(r){
        var self = this,
            url = '';
        
        if(r['action'] === 'transfer') url = '/teachers/submit-student-to-lab/';
        if(r['action'] === 'delete') url = '/teachers/delete-subscription/';
        
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(r),
            dataType: 'json',
            timeout: 10000,
            success: function(data) {
                try {
                    if (data.status == 1){
                        self.$students.parents('tr').addClass('disabled', 80).find('input').attr('disabled', 'disabled');
                        var msg = data.msg + '<a href="#" onClick="window.location.reload()">ανανέωση</a>';
                        self.show_message(1, msg, 200);
                    }
                    else if ( data.status == 2 ) {
                        self.show_message(2, data.msg, 200);
                    }
                    else {
                        self.show_message(3, data.msg, 200);
                    }
                }
                catch(e) { this.error(); }
            },
            error: function(xhr, err){
                /*
                if(xhr.status==500) msg = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
                if(xhr.status==404) msg = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
                */
                self.show_message(2, "Παρουσιάστηκε σφάλμα, δοκιμάστε αργότερα", 200);
            },
            complete: function() {
                X$('DropdownWidget').events.dropdown.hide();
                self.$students = []
                $.scrollTo({top: 0}, 350, {axis:'y'});
            }
        });
    
    },
    
    get_url: function(){
        var result = {},
            url = window.location.href;
        
        if( url.match(/pending-students/) ){
            result = 'pending';
        }
        else {
            result = 'home';
        }
        return result;
    }
    
});

X$('DropdownWidget',
{
    events:         undefined,
    
    init: function(){
        this.events = this.handle_events();
        this.listen_events();
    },
                    
    handle_events: function(){
        var self = this,
            dropdown = {};
        
        dropdown.$ = {
                     buttons:   X$('StudentEdit').$dropdown.find('div.edit-widget'),
                     active:    undefined
                     }
                         
        dropdown.hide = function(){
            var self = this,
                $this = self.$.buttons;
            
            if($this) {
                $this.hide();
                $this.parent().removeClass('active');
            }
        };
        dropdown.close = function(params){
            var self = dropdown,
                $this = self.$.active,
                target = params.event.target;
            
            if($this) {
                var $this = $this[0];
                if(!$.contains($this,target) || !$this == target) {
                    self.hide();
                }
            }
        };
        dropdown.open = function(){
            var self = this,
                $this = self.$.active;
            
            self.hide();
            $this.show();
            $this.parent().addClass('active');
        };
        
        dropdown.$.buttons.each(function(){
            var self = dropdown,
                $this = $(this),
                $parent = $this.parent();
            
            $parent.bind('click', function(e){
                if(e) e.stopPropagation();
                if(e) e.preventDefault();
                self.$.active = $this;
                self.open();
            });
        });
        
        return {dropdown:dropdown};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        $.subscribe('widgets.close.dropdown.transfer', events.dropdown.close);
        return this;
    }

});

X$('SelectAllLabStudents',
{
    $labs: $('#content').find('div.lab'),
    events: undefined,
    
    init: function(){
        this.events = this.handle_events();
        this.listen_events();
    },
                    
    handle_events: function(){
        var self = this;
        
        var checkbox = function(e){
            var $target = $(e.target),
                $parent = $target.parents('table'),
                data = $target.data(),
                option =    {
                            selected: $target.attr('checked') || false
                            };
            
            if(option.selected) {
                $parent.find('tbody input[type="checkbox"]').attr('checked',true);
                $target.attr('title', data.deselect_tooltip).attr('checked',true);
            } else {
                $parent.find('tbody input[type="checkbox"]').attr('checked',false);
                $target.attr('title', data.select_tooltip).attr('checked',false);
            }
        };
        
        return {checkbox:checkbox};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        self.$labs.delegate('input.select-all-students', 'click', events.checkbox);
        return this;
    }

});


