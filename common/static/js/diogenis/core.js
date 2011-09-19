
(function($, window, document, undefined) {
    
    var App = function(module_name, properties){
        return new App.core.init(module_name, properties);
    };
    
    var App = (function(){
    
        App.core = App.prototype = {
            
            init: function(n, p){
                var self = this;
                //console.log("called module [", n,"]");
                if (p){
                    $(function(){
                        self.modules[n] = p;
                        // In case it needs initialization
                        try{
                            self.modules[n].init();
                        }
                        catch(e){ }
                    });
                }
                else if(n && !p) {
                    return self.get(n);
                }
                return self; 
            },
            get: function(n){
                return App.core.modules[n];
            },
            modules: {}
        };

        App.core.init.prototype = App.core;
        App.get = App.core.get;
        
        return window.X$ = App;
    })();
    
})(jQuery, this, this.document);

