X$('StudentSignup',
{
    $user:              $('#user'),
    $messages:          $('#ui-messages'),
    $span:              undefined,
    $button:            undefined,
    
    data:               undefined,
    
    events:             undefined,
    render:             undefined,
    
    templates:          {
                        authenticate:   $('#authenticate-tpl').html(),
                        signup:         $('#signup-tpl').html(),
                        messages:       $('#messages-tpl').html()
                        },
    msg:                {1:'ok', 2:'error', 3:'warning'},
    
    init:           function(){
                        var self = this,
                            templates = self.templates;
                        
                        self.render = X$('Helpers').render;
                        self.$user.empty().append( self.render( templates.authenticate,{}) );
                        
                        self.get_selectors();
                        self.events = self.handle_events();
                        self.listen_events();
                        
                    },
                    
    get_data:       function(){ return this.$span.data(); },
    
    get_selectors:  function(){
                        var self = this;
                        
                        self.$span = self.$user.find('span:first');
                        self.$button = self.$user.find('button');
                        
                        return this;    
                    },
    
    handle_events:  function(){
                        var self = this,
                        	focus = {},
                        	toggle_layout;
                        
                        var submit = function(){
                            self.$button.unbind('click');
                            self.data = self.get_data();
                            self.submit(self.data);
                            setTimeout( function() {
                                self.$button.bind('click', submit);
                            },1100);
                            return false;
                        };
                        
                        focus['in'] = function(){
                        	var $this = $(this),
                        		$parent = $this.parent('div.entry');
                        	
                        	focus.out();
                        	if($parent) $parent.addClass('active');
                        };
                        
                        focus['out'] = function(){
                        	self.$user.find('div.entry').removeClass('active');
                        };
                        
                        toggle_layout = function(){
                            self.$user.empty().append( self.render( self.templates.authenticate,{'old_layout':true}) );
                            self.listen_events();
                        }
                        
                        return {submit:submit, focus:focus, toggle_layout:toggle_layout};
                    },
    
    listen_events:  function(){
                        var self = this,
                            events = self.events;
                        
                        self.$span = self.$user.find('span:first');
                        self.$button = self.$user.find('button');
                        $toggle = $('#toggle-layout');
                        
                        self.$button.bind('click', events.submit);
                        self.$user.find('input').bind('focus', events.focus['in'] )
                       							.bind('blur', events.focus['out'] );
                       	
                       	$toggle.bind('click', events.toggle_layout);
                       	$('#school').chosen();
                    },
    
    submit:         function(r){
                        var self = this,
                            templates = self.templates,
                            request = {},
                            action = r['action'],
                            incomplete = false;
                        
                        if(action==='authenticate'){
                            var inputs = $('#user div.entry input');
                            
                            request = {action:action};
                            for(var i=0, input; input = inputs[i]; i++){
                                input = $(input);
                                request[input.data('type')] = input.val();
                            }
                        }
                        if(action==='signup'){
                            var school = $('#school'),
                                agree_terms = $('#agree-terms').is(':checked'),
                                school_id = (school.val()) ? school.find(':selected').data('id') : '';
                            
                            request['action'] = action;
                            request['student'] = r;
                            request['school_id'] = school_id;
                            request['agree_terms'] = agree_terms || '';
                        }
                        
                        for(var item in request){
                            if(request[item]==='') incomplete = true;
                            //console.log(item+': '+request[item]);
                        }
                        
                        if(incomplete === true){
                            var context =   {
                                            status:self.msg[2],
                                            msg:"Παρακαλώ συμπληρώστε τα στοιχεία"
                                            }
                            self.$messages.empty().show().append( self.render(templates.messages, context) );
                        }else{
                            self.$messages.empty().hide();
                            
                            $.ajax({
                                url: '/signup/',
                                type: 'POST',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify(request),
                                dataType: 'json',
                                timeout: 10000,
                                beforeSend: function() {
                                    //emfanise loader
                                },
                                success: function(data) {
                                    if(data.action==='authenticate' && data.status===1){
                                        self.$user.empty().append( self.render(self.templates.signup, data) );
                                        self.listen_events();
                                    }
                                    
                                    if(data.msg){
                                        var context =   {
                                                        status:self.msg[data.status],
                                                        msg:data.msg
                                                        };
                                        self.$messages.empty().show().append( self.render(templates.messages, context) );
                                    }
                                },
                                error: function(xhr, err){
                                    var context =   {
                                                    status:self.msg[2],
                                                    msg:"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
                                                    };
                                    self.$messages.empty().show().append( self.render(templates.messages, context) );
                                }
                            });
                        }
                        
                        
                    }
});

