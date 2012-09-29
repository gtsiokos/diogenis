describe("Core Module System", function() {
    
    describe('Ένα module', function() {
        
        beforeEach(function() {
        
            X$('Module1',{
                key_1: 12345,
                init: function(){
                    return this;
                }
            });
        
        });
        
        it('Περιέχει το όνομά του στις _meta πληροφορίες', function() {
            expect(X$('Module1')._meta['name']).toBe('Module1');
            //expect(X$('Module1')._meta['extends']).toBeDefined();
        });
        
        it('Δεν περιέχει το όνομα του module που το επεκτείνει στις _meta πληροφορίες εφόσον δεν έχει επεκταθεί', function() {
            expect(X$('Module1')._meta['extends']).toBeUndefined();
        });
    });
    
    describe('Όταν ένα module διαγράφεται', function() {
        
        beforeEach(function() {
        
            X$('Module1',{
                key_1: 12345,
                init: function(){
                    return this;
                }
            });
            
            X$('Module1').delete();
        
        });
        
        it('Αφαιρείται από τα φορτωμένα modules', function() {
            expect(X$.get('Module1')).toBeUndefined();
        });
    });
    
    describe('Όταν ένα module επεκτείνεται από ένα άλλο', function() {
        
        beforeEach(function() {
        
            X$('Module1',{
                key_1: 12345,
                init: function(){
                    return this;
                }
            });
            
            X$('Module2').extends('Module1', {
                key_2: 23456,
                init: function(){
                    return this;
                }
            });
            
        });
        
        it('Περιέχει το όνομα του module που το επεκτείνει στις _meta πληροφορίες', function() {
            expect(X$('Module2')._meta['extends'][0]).toBe('Module1');
        });
        
        it('Κληρονομεί τα properties του επεκτεινόμενου module', function() {
            expect(X$('Module2').key_1).toBeDefined();
            expect(X$('Module2').key_1).toBe(12345);
        });
        
        it('Διατηρεί τα δικά του properties', function() {
            expect(X$('Module2').key_2).toBeDefined();
            expect(X$('Module2').key_2).toBe(23456);
        });
        
        it('Το αρχικό module δεν περιέχει το όνομα του module που το επεκτείνει στις _meta πληροφορίες', function() {
            expect(X$('Module1')._meta['extends']).toBeUndefined();
        });
    });
    
    describe('Όταν ένα module επεκτείνεται χρησιμοποιώντας mixin', function() {
        
        beforeEach(function() {
        
            X$('Module1',{
                key_1: 12345,
                init: function(){
                    return this;
                }
            });
            
            X$('Mixin1',{
                mixin_func1: function(){ return true; },
                init: function(){
                    var self = this;
                    self.mixin_func1();
                    return this;
                }
            });
            
            X$('Mixin2',{
                mixin_func2: function(){ return true; },
            });
            
            X$('Module1').mixin(['Mixin1', 'Mixin2']);
        });
        
        it('Περιέχει το όνομά του στις _meta πληροφορίες', function() {
            expect(X$('Module1')._meta['name']).toBe('Module1');
            //expect(X$('Module1')._meta['extends']).toBeDefined();
        });
        
        it('Περιέχει τα properties του mixin', function() {
            expect(X$('Module1').mixin_func1).toBeDefined();
            expect(X$('Module1').mixin_func2).toBeDefined();
        });
        
        it('Το mixin διατηρεί τις _meta πληροφορίες του', function() {
            expect(X$('Mixin1')._meta['name']).toBe('Mixin1');
        });
    });
    
});
