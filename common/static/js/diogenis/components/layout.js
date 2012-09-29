
X$('Sidebar',
{
    $window:$(window),
    $sidebar:$('#sidebar'),
    $navigation:$('#navigation'),
    
    init:               function(){
                            if(this.$sidebar[0]){
                                //this.set_sidebar_height();
                                if(this.$navigation[0]) this.handle_events().position_navigation();
                            }
                        },
    
    handle_events:      function(){
                            var self = this;
                            self.$window.resize(self.position_navigation);
                            return this;
                        },
    
    position_navigation:function(){
                            var self = X$('Sidebar'),
                                a = self.$sidebar.offset(),
                                b_left = Math.round(a.left);
                            
                            self.$navigation.css({ top: 170, left: b_left });
                            return this;
                        },
                        
    set_sidebar_height: function(){
                            var self = this,
                                content_height = Math.round($("#content").outerHeight());
                            
                            self.$sidebar.height(content_height-41);
                        }
});

X$('GlobalEvents',
{
    $body:              $('body'),
    init:               function(){
                            this.handle_events();
                        },
    
    handle_events:      function(){
                            var self = this;
                            
                            self.$body.click(function(e){
                                var params = {event:e};
                                $.publish('widgets.close', params);
                            });
                        }


});

X$('AccountDropdownWidget',
{
    $login:         undefined,
    $panel:         undefined,
    
    events:         undefined,
    
    init:           function(){
                        this.$login = $('#login');
                        this.$panel = this.$login.find("div.panel").hide();
                        
                        this.events = this.handle_events();
                        this.listen_events();
                    },
                    
    handle_events:  function(){
                        var self = this,
                            dropdown = {};
                        
                        dropdown.$ = {
                                     panel:     self.$panel,
                                     button:    self.$login.find('a.options-panel'),
                                     active:    undefined
                                     }
                                         
                        dropdown.hide = function(){
                            var self = this,
                                $this = self.$.active;
                            
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
                        
                        dropdown.$.panel.each(function(){
                            var self = dropdown,
                                $this = $(this),
                                $parent = $this.parent();
                            
                            self.$.button.bind('click', function(e){
                                if(e) e.stopPropagation();
                                if(e) e.preventDefault();
                                if ( $parent.hasClass("active") ){
                                    self.hide();
                                } else {
                                    self.$.active = $this;
                                    self.open();
                                    try{
                                        $this.find("input")[0].focus();
                                    } catch(error){ }
                                }
                            });
                        });
                        
                        return {dropdown:dropdown};
                    },
    
    listen_events:  function(){
                        var self = this,
                            events = self.events;
                        
                        $.subscribe('widgets.close.dropdown.user_panel', events.dropdown.close);
                        return this;
                    }

});

