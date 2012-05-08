---- $toy_language wafflings:

previous abortive attempts: egan (parsers), haklog (intepreter), 
    cornelius (i), nezha (i), knut (spec).

originally, I tried extending prolog. then I tried extending python.
then I started more prolog esque and cut down my dreams one by one
until I ended up with something python-esque. 

as a warning and an apology:
	this is pretty vague in places
	and some of the bits are underdescribed.

---- language overview:

	python with braces, with flat prototypes over classes,
	processes/pipes/message passing over threads, and
	heavier use of function compositon and anonymous
	functions.
	

	I am stealing so much from python, and trying to 
	be mindful in doing so.
	

---- why this is better:
	no threads: (+erlang ~js -python -ruby)
		processes, communicating over signals (erlang style),
		or pipes (unix style), with supervision.
		
		better fault isolation, better robustness, 
		simpler code.
		
			
	orphan prototype model with traits and mutlimethods-ish 
		simpler object model without inheritance or metaclasses

		objects are ultimately wrapped dicts with sugar
		uses the python descriptor protocol to implement methods

		objects built through composition of objects/traits
		no concrete types, only behaviours can be checked
		
		delegation syntax to forward traits to particular attributes
		(no more wrapping every method call to safely extend an object)
		
		for a collection of objects you can call a multimethod,
		where the objects are tried in turn 
		
		no polymorphism, in a dynamic language but function guards.
		
		
	dialects are part of the language
		can extend existing grammar by adding new operators or literals 
		(with restrictions)

		this allows separation of library code
		and sugar, and using a dialect is explicit and per-file

	managing the code is part of the language:
		decorators and syntax for exporting versions of 
		functions/modules and importing restrictions
		
		debugging/logging builtins
		
		docstrings, and tests and logging

	nearly everything is an expression
		unlike python, can use ifs/whiles/function defs within expressions
		can define anonymous functions and objects or traits
	
	and some sugar on top:
		utf-8 strings by default
		braces when you need them
		process-local variables for context (i.e logging/stdin/stdout)
		better module naming/implicit handling
		braces if you're into that sort of thing:3
		less ambiguous ducks - builtins don't behave like a scalar and a list
			
---- why I can't have my cake and eat it

	classes, threads and non unicode strings are baked in
	to existing languages.
	
	using prototypes and processes is a fundamental shift 
	in how larger applications are written
	
	
	perl5 has too much baggage from perl 4 and earlier,
	although I could write in Moose and DEAL WITH IT


---- name contenders
	knut, nezha, kotekan, imbal
	
---- ersatz zen:

	from python import zen, data_structures, data_model
	from perl import braces, regex, virtues
	from ruby import a little magic 
	from erlang import supervision, processes, otp, inboxes
	from unix import philosophy, pipes, signals

	these are some of my influences, but they aren't responsible
	for my mistakes in copying them, or my foolish combination below

---- design constraints:

	should be understandable by a perl, ruby or python programmer
	within a handful of minutes.
	
	avoid special syntax and re-use existing datatypes/grammar
	where possible, including literals.

	the standard library isn't a special case, any language
	magic it uses must be accessible to the programmer.
	
	just a little magic is good. more than python much less than ruby.
	some special cases happen often enough to bend the rules a little.
	
	a little redundancy in the language can add to readability, so
	language features should be classed by intent, not by 
	implementation -- different things should look different
	
	function composition is useful, let's do more of that. 
	erlang/otp is a good idea - process supervision is essential
	for robust programs.
	
	languages need to grow, language extensions should be
	first class, and distinct from libraries. 
	
	programs are not just code, they are documentation 
	specification and tests. these need to be part of the language

	whitespace is nice, but braces are easier some times.

	things should be first class, and by extension, anonymous
	
	try to avoid false simplicity, a primitive feature is
	only useful if it doesn't have to be wrapped into shape.
	false simplicity leads to design patterns.


	

	
---- core language:

	everything is a object, i.e has attribues obj.a obj.b etc
	call by object reference

	when in doubt, it should work like python
		
--- built in types:	

	string "woooo I am utf-8" 'woo'
         (immutable, not list like, and string interpolation "$foo ${bar}")
         there are also different types of string, noted by a prefix foo"...."
         
         to iterate over a string you must split it, for example by .chars()
         or .lines() or by whitespace  
	
	characters c'x'  c"\0" etc, (wide/unicode chars)
	
    number 0123_456, 344.54885
          can have underscores (like perl they are ignored, 1_000 = 1000)
          can have leading 0s, ie 010=10,
          types of number are prefixed with 0name
          octal is 0o10..., hex is 0xFF... binary is 0b11010...

    list [1,2,3]  (mutable container type)
    tuple 1,2,3 or  (1,2,3)   (immutable container type)
    	last , is optional in []'s
	    ()'s optional, except for empty tuple ()
	    last , is optional in tuples with more than one item
	    	
	    i.e ()   2, or (2,)  3,4 or 3,4, (3,4) or (3,4,) 

    ordered dict [a=1; b=2;"c":3] ,  empty dict is [;] ?
        (note foo=bar is "foo":bar), and it is ordered by insertion.
        dicts also have implicit ; in newlines
        [ 
          a=1
          b=2
        ]
        
        note we use []'s for dicts so we can use {}'s for blocks
        we can't use , as the seperator as that is ambiguous
    
    built in types:
    true, false, nil.

	also, steal bytestrings and buffer/memoryviews from python3.
		
		
		
--- expressions and statements:

	basic syntax rules:
	
        python with braces, newline is terminator.
    
        i.e ONE TRUE BRACE STYLE
	          x = 
	        	{ 
	        	}  is a syntax error.
	    
	    comments: // /* */ and # 
        
        like in python:
	        statements are top level bits of syntax, 
	        like module statements, or imports
	        or if/for/while, and are often marked by whitespace
	        indentation
        
	        expressions are bits that are whitespace ignorant,
    	    i.e 1 + 2, 3 < 4, and cannot contain statements
      	
	        assignment is a statement, and cannot be embedded
	        in an expression: x=(y=1)+1 is invalid

      	however, unlike in python:
      		most statements that take an indented block
      		have an expression form that uses braces
      		
      		
      	so a statement if looks like:
      		if x:
      			..... 
		and an expression if looks like
			if x {....}      

		this is so you can do
			x = if y {.....} 
	
		reminder: you can't use indented blocks
		anywhere other than directly inside indented blocks
		as soon as you use {}'s, indentation is ignored
		like in ()'s or []'s
		
		
  basic flow control:
        normal boolean operators and values:

        if statements:
            if foo { } else { },

			or 
			if foo:
				   indented block
			else if bar:
			       indented block
			else:
			   	indented block
            (like python this calls __bool__() on foo)
            
            accept e(l|ls|lse|else )if

        and an infix version:
            {...} if foo else {...}

        while loops:
            while bar { ... }
            
   		for loops: (the iterator protocol is defined later)
            for x in source { ....}
   

    variables:
        store references to objects
        implied lexical scope, implicit declaration ala python.
        explicit lexical scope with let, or where. (below)
        
        	
		x = 1 defines a mutable variable x 
		x = 2 changes it
		
		def x 1 defines x as 1
		x = 2 is an error 
		
		things with def cannot be re-assigned, or re-defined
		
		

    functions
        like python: functions are call by object reference

        def foo(a,b,c=1):  
            implicit return, default values evaluated at call time
        
        def foo(a,b) {
        	....
        }
        
        can't reassign a def.
     
        
        functions can be called using named args;
        a = foo(a=3, b=4)

        varargs definitions foo(*listargs, **kvargs)

        'return' and 'return from' to mark tail recursive return.

        anonymous function syntax:
            {|x,y| .... non empty contents ....} 
            

        there is also a syntax for obtaining infix operators
            (+) (*) (.) -   (+) is to A + B as foo is to foo(A,B)
			x = (+)
			print x(2,2)
			
        and partial versions of the infix operators 

            (< 7) as in  {|x| x < 7}
            (.foo(1,2,3)) as in   {|x| x.foo(1,2,3)}
            (.bar) etc 
           
		prototypes can behave like functions by providing a __call__
		method.
		
		functions also have a __call__ attribute, too.
		
		functions have signatures
		
			signature = {|x,y,z*|} 
		
		these are used later in traits.
		
	
		
		        
     decorators:
     	a useful syntax for one argument functions
     	
     	x = @foo y is x = foo(y)
     	
     	they can also be applied to definitions too
     	or assignment
     	
     	@foo
     	def x(...) ... is like x = foo({|...| ...})
     	or @foo x = {|.|..} is like x = foo({|..|..})
     	@foo is low binding, i.e @foo x + 4 is @foo (x + 4)
     	
     	useful syntax for compositional function calls
     	or simply wrapping functions
     	x.a = @method {|self,x|  ... }
     	
     	@print 1,2
     	
     	used for things like memoiziaton

    case/switch style statements:
        switch operator:
            takes a dict of values:functions.

            expr switch [
                10: x :- say("$x is 10")
                nil:  ...
            ]

            % yes, dicts are ordered.

            it can also have foo switch [..] else {..} if nothing matches.

        match operator:
            there is also a match that takes a dict of functions:functions 

            expr match [
                (.isint) : {|x| say("$x is an int")}
                (is nil):  ...
            ]
            
            there is a way to capture the output of a match function, by wrapping
            the associated function in a prototype with a __match__ method
            
            expr match [  (.split(" ")): @capture {|e,*args| ... } ]
            
            this is done through a decorator 
            
            possibly allow   *expr match [ ....]

   exceptions: 
        functions can return a value or throw a value

        try is like an if statement, but checks to see if it 
        returned a value, or threw. rather than true/false.

        try x = foo(...) {
            ... 
        } rescue {|x| 
            ... on failure/exit .... 
        }

		try x=foo(...) {
		....
		} catch {|x| ...on errors... }
		
        catching is a little bare bones at the moment.
        
   iteration:
        for loops:
            for x in source { ....}
            

        iterators have a next() method
        that either returns a one element tuple (value,)
        or None at the end of the list.

        iterators can be composed using map, filter and similar operators
        from the itertools package. these return iterators which
        execute on demand. i.e lazy operators, also left assoc ((,),)

        these can be used as infix operators
            y = range(0,100) map (*2) filter (<30) map (**2)

        like the other infix operators, there are also anonymous partial versions 

            f = (map (*2))
            l = ([1,2,3] map)
            a = (map)

        this allows more flexible composition, and means that you can write
        iteration in a more pipeline style, akin to method chaining


        f = (map (match [isInt: {|x| 0} ; any: {|x|nil}))

        x = f([1,2,3,'a']) is [0,0,0,nil]
        
    generators:
    	yield and yield from, like python
    	
    	(can this be implemented in call/cc ish manner?) 
    	are they going to have send() ?
    	
 	 let, with  syntax, 
        with {fooo=open(....)} in {
            ......
        } // * will .close() foo here

		let {a=1;b=2} in {
			// 
		} // will just delete a,b

        with implies a contextmanager, ala python
        
        or with {.....}:
         	....
        
        or
        with:
        	......
        in:
        	......
   regexes:
   		regexes are functions, and can use the literal as such
   		rx"\d+"(foo) to match foo
   		
   		also expose .match(...)
   		
	tuple assignment:
		uses * to mean unpack/pack
		like in python vararg functions
		
		a,b,c = 1,2,3
		
		a,b,*c = 1,2,3,4
		
		[x=x;y=y] = o	
		
		a,b,c = (1,*[1,2])
  
  
  
---- modules and execution:            

    modules  (are prototypes too)
        like python, files are implicitly modules.

        modules can be imported
            import foo, foo.bar
            from foo import * etc

        modules can define their name in limited ways
        rather than simply implicitly using the relative file name.

        in a foo/bar.py can have
        no module declaration 
                -- it is foo::bar to the current dir but internally it is bar

        or it can state some of it's path in the name, i.e.
            module foo.foo
                -- it is foo::bar internally and externally, so
                    inside I can import from foo:: 
        or use the directory name as the module name, ignoring the file name.
            module foo
                -- it is actually part of the directory.
                   so everything is in foo, and there is no foo.bar
		
	 files are scripts:
		when loaded the file is executed like a script.
	    like python, perl or ruby.
	    
	    if run in this way, and there is a __main__ function
	    defined, it is called with the command line arguments
	    
    files are libraries
        you can also define a __module__ function too
        that returns a module to supplant the default
        one in the file.	
        
        modules by default export all definitions
        that don't have a leading underscore
        
		@export should allow you to export things
		at a defintion level, assignment level
		
		
	versioning:
		versioning in modules and definitions through decorators
		
		something like: module foo exports 0v0.1, 0v0.2
	
		@version(introduced=0v0.2, deprecated=... removed=...)

  		
   	debugging:
   		trace/debug decorators, to follow execution
   		or to dump data strucutres
   		debug is essentially dumping to stderr	
   		
   		ie
   		@trace
   		def foo(x,y) {...}
   		
   		would print to std err every time foo is invoked
   	





---- object system	

    everything is a object.
		objects are essentially wrappers around dicts
		with a little sugar
		
		foo.a looks up a in it's own dictionary.
		this dictionary is available as a hardwired attribute
		foo.__slots__        
        
    	obj.name is the same as getattr(obj.name)
    	
    	there are number of ways to build a object:
    	
    	 	a struct, built using x = struct(a=1,b=2,c=3)
				fixed slot names, can't add or remove attributes
            	values accessed with x.a, x.b, etc.
            	
	        a new prototype from a dict. bless(foo)
	        	this creates a new object that uses 
	        	the items in foo for it's attributes.
	        	
	        nb: bless(x) is the same as struct(**x)
	        
	        an object literal x = object {......}
	        	(explained below)
	        
	        through composition, and
	        	        
	        through traits
	        	traits are like flat abstract classes
	        	that can be composed together. like bless
	        
		        you can also add delegate traits, i.e methods that are 
		        forwarded to an attribute.
	        
	        
	 	__slots__ can be get and set like other attributes, but not
	    deleted.
	    
	    attributes can override their behaviour, (explained below)
	    to allow method binding and multimethods, and delegate methods
	    
	    notably: 
	    	objects are flat, and there is no parent or base class
	    	traits are immutable
	    	if you want privacy, use a closure
			objects are anonymous
		
		the built-in objects are closed. no monkeypatching.
		i.e their .__slots__ attribute is immutable
        
 	methods:
 	
 		@method 
 		def some_method(self,a,b,c):
 			...
 			
 			
 		like python, self is explicit, and the descriptor protocol is used.
 		this means that when x.a or gettattr(x,a) is called,
 		it tries to call a.__get__(x)
 		
 		i.e, when do you x.a it is actually x.__slots__['a'].__get__(x)
 			
 		this allows us to write attributes that bind to their parent
 		on access. using this we can implement methods.
 		
 		methods can be created by calling method(fn) or @method fn
 
 		both method and self are explicit, but there is some sugar
 		
 		def self.foo(x,y) { .... } is foo = @method {|self,x,y| ...}
 		

    methods/attributes define behaviour:    	
    	most object actions are defined through method acccess
        foo.to_str() (a cast)
        
        or can be extended through methods
        i.e, getattr(x,a) calls x.__getattr__(a) if it is present.
        
       	some are attributes:
       	foo.len , foo.__str__ (this is the internal, give me a string, not
       	a cast) 
   
   
   traits, object literals:
   		objects are dicts with sugar,
   		traits are incomplete objects.
   		
   		object literal syntax:
   			can compose parts of traits or objects
   			can define attributes
   			uses decorators to define methods/multimethods
   			some sugar
   			cannot contain abstract attributes
   			
		a = object {
			has traita, traitb
			x= 1;
			@method foo(.....) {
			} with traita, traitb?
		};
		
   		traits literal syntax:
   			can compose parts of traits
   			can define attributes or requirements for attributes
   			i.e function signature or attribute name
   			
   			uses decorators to define methods/multimethods
   			some sugar
   			can contain abstract attributes


		list =  trait {
		
			abstract x 1
			abstract f(1,2,3)
			
			abstract self.foo(a,b,c)
			
			@method requires foo(x,y,z) {.....}
			 
		}
	
		abstract is like def but can take
		a function signature or a name, without an accompanying value
		
		with  some syntax for anonymous abstract requirements
		
		 x = required {|x,b,*c|}
	
		requires can take an optional defintion
		
		
	multimethods:
		methods that are dispatched over a collection of objects
		rather than an individual object. 
		
		each object's multimethod is tried in turn until one
		succeeds.
		
		
		for instance, in addition, each object exposes an __add__
		multimethod that takes two arguments
		
		to do 1 + 4, the __add__ multimethod attached to 1 is called
		and, if it throws NotImplemented, then 4's multimethod __add__
		is called.
		
		A multimethod defintion looks like a normal method,
		but expects a collection of objects in the first
		argument:
		
		@multimethod def __add__((selfa,selfb)) {....}
		@multimethod def collide(objs, arg1, arg2) {....}
		
		syntax:
		
		i.e  (a,b).*__add__()  will call __add__ in a, then in b
		with the same arguments ((a,b))
		
		if a returns: b is not tried
		if a throws: the exception is thrown
		if a raises NotImplemented exception: the next multimethod is tried
		if a multimethod cannot be found: an exception is thrown
		
		
		many of the operators are defined in terms of multimethods
		
		[[ note in python, a similar thing is achieved for operators
		   of two arguments, first a.__foo__(b) is tried, then b.__rfoo__(a) is tried
		   here instead, __foo__ is tried in a and b, and the first argument
		   'self' is bound to (a,b). this extension is a lot less clumsy]]
		   
		   
	delegates:
		objects can delegate a collection of method names
		to a specific attribute
		
		d = delegate {traits} to name
		
		produces a new trait, where the method bodies,
		attributes and requirements are transformed into
		optional functions i.e
		
		
		x= trait {
			abstract self.count()
		}
		
		d = delegate x to bar
		
		is the same as:
		
		d = trait {
			abstract bar
			abstract self.count() self.bar.count()
		}
	'
		   
---- processes, concurrency

    lightweight processes, pipes, inboxes:
    
        can spawn other processes. can communicate over pipes,
        or signals/messages to the processes.
        
        
        pipes are like unix pipes, with a fixed input and output
        writer,reader = pipe()
        writer.write(), writer.close(), writer.error()
        
        
        this is the concurrency primitive for pipe-style programming
        passing data between processes, possibly filtering.
        
        the other form of concurrency is the process inbox:
        %inbox, which is iterable.
        
        other processes can send messages (or signals) to
        the process, which normally go in the inbox.
       
       	however, some signals throw an exception
       	by default. but can be masked, which results in 
       	a message being stored in the inbox.
       	
       	so, proc.signal(.....) means deal with this right now
       	and will either be put on top the inbox, or will cause
       	the process to throw an exception
       	
       	and proc.send(....) means deal with this eventually
       	and is put on the end of the inbox
       	      
        for example:
        	process death sends a signal to the owner, which
        	if not masked, will throw an exception.
           
        pipes are for filters/pipelines, inboxes are for signals
        
        signals are used to form supervision heirarchies,
        like in erlang/otp
		
		
	process context variables, 
        these are marked with % prefix, i.e %stdin
        
        these can only be overidden, not set all the time?
        
        i.e 
        
        let {%foo={....}} in ......
        
        
        (globals by any other name... but live in a seperate 
        namespace, and no sharing)
		
    pipes:
        pipe is an infix operator like map
        if do you 
            x = [1,2,3] pipe foo(1,2,3)

        this spawns foo in a new process with the arguments 1,2,3, 
        setting %stdin to the iterator of [1,2,3]
        and a pipe mapped to stdout and the returned iterator 


	select style operator
	
		x = select [
			chan1 : {|value_read| .... }
			.....
		]
		
		
	will need some sort of process registry too,
	but i'll steal that from erlang
		
		
---- idioms:
	re-use basic data types over inventing new syntax.
		i.e switch, match, with, where all use dicts
	
	provide built in operators for common tasks that
	can delegate to methods.
	
	__mustaches__ indicate specialness, i.e a not so normal method
	like __add__ where it is normally called by a + b 
	some, like .iter() and .next() are not 
	
	many behvaiours are defined over a number of methods in
	preference order i.e 1 + 2 is 1.__add__(2) or 2.__radd__(1)
	
	for example <list> map <fun>  tries
	list.__map__(fun) first before list.iter()
	
	prototypes are defined by their behaviour through attributes,
	so if you want an object to behave differently, it should 
	have different attributes.
	
	decorators are used to wrap objects with new behaviours.
	i.e @method, @capture
	
	many builtin functions can take functions as arguments
	max(..., key=fn)  sort(..., key=fn), etc
	
	
	def method(func) {
		obj = bless([ 
			__func__=func 
			__call__= *x,**y :- func(*x,**y)
		])
		bless([__get__=obj])
	}
	
	@method 
	def f(...) {
	
			
---- language extentions
		
	prelude:
			language is defined from a core set of features and syntax:
			
				small token set and reserved words
				
				statements (if/for/def/let/try, foo[], foo(), @foo foo) and some literals (number, string, list, dict, function)
				and some built in functions (getattr, setattr, spawn, bless, etc)
				
				it defines grammar hooks for operators, or special literals
				i.e hooks for infix, postfix, distfix operators, relational infix operators (<,>,==)
				
				and the implied transformation rules
				
			this all lives in the __native__ namespace -- things that must live in the bootstrap
			
			the prelude defines core which comprises the language fully -- things that
				can be defined within the language
			
			the prelude contains:
				a lot of sugar
				some infix, prefix and postfix operators
				including the  relation operators which can do 1<2<3 etc
				attribute lookup sugar
				map, filter
				
		the prelude essentially defines the magic in the programming language
   		
	magic, or dialects
	 	we can define a new feature for the language
	 	in terms of extentions to the core grammar
	 	like adding new operators from existing types
	 	(infix, prefix, distfix, etc)
	 	
	 	new types of literals from existing types
	 		i.e new strings like  foo"...." and numbers like 0n....
	 
	 	and ast transformations/rewrite rules
	 		that return a parse tree without the new features
	 	
	 	
	 	a strawman syntax is :
		 	goo = dialect {
				reserved .... re
				right_infix re ....
				prefix re
				postfix re
				disfix re ....
				expr ... ?
				distfixliteral name re
				numberliteral name re
				stringliteral name re
				interpolatedstringliteral name re
				listliteral name re
				blockliteral name re
				
				transform x + y into { (x,y)*.__add__() }
				
				
				template if cond &block ... { ...... 
				}
			}
		
		and use goo to use that dialect
		
		use statements are per-file and must be at the top of the file
		(before any definitions or code)

	example language extentions:
	
		xml and web handling:
	
			allow string interpolation 
			xml literals xml"<foo>.....${......}" etc
			
			file"....."
			url"...."
			http"...."
		    xpath"....."	
			
			uris/urls maybe url"............." 
		
			throw in GET/POST etc or smart urls, like say url"http://....".get(.....) 
	

	
spec bugs:

	exceptions used for multimethods
		all seems to come back to 'error by default'
		
	multimethods probably not best name
		no resolution order
			should (a,b)*.foo() be the same as (b,a)*.foo()
		no exception handling? should it be pushed down the chain?
			
	no exception mechanism defined in terms of exception matching? maybe traits
		how to say 'this type of thing'
			well, exceptions defined through attributes
			ex.error
		
		
	ffi?
		how will it fit in with 'dialects', will it be like ctypes
		
		
	memoization and other niceties?
	