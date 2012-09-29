
(function($, window, document, undefined) {
    
    var App = function(mod_name, props){
        return new App.core.init(mod_name, props);
    };
    
    var App = (function(){
    
        App.core = App.prototype = {
            
            init: function(n, p){
                var self = this,
                    p = self._copy(p);
                
                if(!self.modules[n]){
                    self.modules[n] = self._copy(self.api);
                    self.modules[n]._meta = {'name': n};
                }
                //console.log("called module [", n,"]");
                if (p){
                    self.modules[n] = self._extend(self.modules[n], p);
                    self.modules[n]._meta = self._extend(self.modules[n]._meta, p._meta);
                    
                    $(function(){
                        // In case it needs initialization
                        try{
                            self.modules[n].init();
                        }
                        catch(e){ }
                    });
                }
                else if(n && !p) {
                    return self._get(n);
                }
                
                return self; 
            },
            api:{
                extends: function(n, p){
                    var self = this,
                        core = App.core,
                        modules = core.modules,
                        meta = self._meta,
                        mname = meta['name'],
                        parent = core._copy(modules[n]);
                    
                    p = core._extend(parent, p);
                    
                    p._meta = meta;
                    if (n !== mname){
                        p._meta.extends = [n];
                    }
                    
                    self = modules[mname] = core._copy(p);
                    
                    if(self.init){
                        self.init();
                    }
                    return self;
                },
                mixin: function(mixins){
                    var self = this,
                        props = {},
                        core = App.core,
                        modules = core.modules,
                        meta = self._meta,
                        mname = meta['name'],
                        minit = self.init || undefined,
                        self = modules[mname];
                    
                    for (var i=0, mixin; mixin = modules[mixins[i]]; i++){
				        props = core._extend(props, mixin);
				    }
			        props._meta = meta;
			        
			        self = modules[mname] = core._copy(props);
			        if(minit){
			            self.init = minit;
			        }
			        if(self.init) {
			            self.init();
                    }
                    return self;
                },
                'delete': function(){
                    var self = this,
                        mname = self._meta['name'];
                    
                    delete App.core.modules[mname];
                    return self;
                }
            },
            _get: function(n){
                return App.core.modules[n] || undefined;
            },
            _extend: function(o1, o2){
                return owl.copy( $.extend(o1,o2) );
            },
            _copy: function(o){
                return owl.copy(o);
            },
            modules: {}
        };

        App.core.init.prototype = App.core;
        App.get = App.core._get;
        
        return window.X$ = App;
    })();
    
})(jQuery, this, this.document);

