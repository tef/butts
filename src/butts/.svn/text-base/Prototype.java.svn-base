/**
 * 
 */
package butts;

import java.util.List;

import butts.prototype.SlotPrototype;

public interface Prototype {
	

	/** This is a Java implementation of a prototype like data structure for a toy language
	 * 
	 * Prototypes
	 * ----------
	 * Prototypes are like anonymous structs
	 * 		they have no parents, 
	 * 		they have no classes,
	 * 		they only have attributes.
	 * 
	 * 
	 * The basic prototype in Java is SlotPrototype, one method it has is 
	 * getattr: 
	 *  	 foo.getattr(name) - get a value with the associated name
	 *
	 * Prototypes can be functions, strings, numbers and a number of other things.
	 * These are implemented as subclasses of SlotPrototype:
	 *   		 FunctionPrototype, NumberPrototype, StringPrototype  below
	 * 
	 * All of the classes have a number of methods for manipulating them
	 * 
	 * Examples in java:
	 *     	foo.call(args) - if foo is a function, execute it. other prototypes throw an error
	 *    	and foo.bool() - get a java boolean value 
	 *    	foo.getattr(..) , foo.hasattr(..)
	 *    
	 * So, instead of relying on the class of a prototype, we rely on the behaviour
	 * of its methods. A function is a prototype with a call method that returns a 
	 * value. Ones that don't behave that way throw an exception.
	 * 
	 *    
	 * Overriding behaviour
	 * --------------------
	 * We want to allow any prototype to behave like a function, not just ones with
	 * special call() methods.   
	 * 
	 * So we say that any prototype with a "__call__" attribute is a function.
	 * 
	 * To implement this, we change the .call method to behave as follows
	 * In the FunctionPrototype, we leave it unchanged, .call just does what we expect
	 * 
	 * For a SlotPrototype, the behaviour in java is to delegate to the slot __call__
	 *  	getattr('__call__').call(args)
	 * 
	 * So, ultimately, calling a prototype involves delegating to another prototype
	 * until you get to a java builtin.
	 * 
	 * If any prototype with a "__call__" attribute is a function, then the builtin
	 * functions must also have a __call__ attribute, which is itself.
	 *  
	 * This means that  p.call(args) and p.getattr('__call__').call(args) are
	 * the same
	 * 
	 * Similarly, a BooleanPrototype has an attribute  __bool__ which is a function that 
	 * returns the same value. i.e	p.bool() returns the same as p.getattr('__bool__').bool()
	 * 
	 * 
	 * Descriptors
	 * -------
	 * 
	 * Prototypes are simple containers. If you put a function in a slot it behaves like a function.
	 * This means there is no notion of a method call. Attributes have no notion of the containers 
	 * they are in.
	 * 
	 * So, when we lookup, set or delete an attribute, we should allow the attribute itself to have
	 * custom actions.
	 * 
	 * So, we introduce new attributes '__get__', '__set__' and '__del__'. These are all functions
	 * that take two arguments, the attribute prototype and the containing prototype. and return
	 * the desired attribute
	 *	 
	 * When we get an attribute, we check to see if it has a '__get__' attribute, and return
	 * that functions value instead of the attribute itself.
	 * 
	 * So, the method getattr(foo,name) does (roughly)
	 * 			def getattr(foo, name) {
	 * 				attr = slotlookup(name),
	 * 			   if attr.hasattr(__get__) {
	 * 					return getattr(attr,__get__).call(attr, foo)
	 * 				} else {
	 * 					return attr;
	 * 				}
	 * 			}
	 * 
	 * We can now define methods in terms of these descriptors, we can return
	 * a partially applied function with respect to the container on lookup
	 * 
	 */
	
	/** A prototype 
	 * 
	 * 
	 *  All prototypes have a number of java methods that correspond to python builtin functions
	 * 		getattr(), call(), etc.
	 * 
	 **/
	
	

	// attribute protocol in java
	public Prototype getattr(Prototype name);
	public boolean hasattr(Prototype name);
	public void delattr(Prototype name);
	public void setattr(Prototype name, Prototype value);
	
	/** these are useful java methods that forward the call to the corresponding slots **/
	public boolean bool();

	// function protocol
	public Prototype call(List<Prototype> args, Prototype listargs, Prototype dictargs);
	public Prototype callattr(Prototype name, List<Prototype> args);
	
	// dictionary protocol
	boolean contains(Prototype name);
	public Prototype getitem(Prototype args);
	public void delitem(Prototype args);
	public void setitem(Prototype arg, Prototype val);
	
	// iteration protocol
	public Prototype iter();
	public Prototype next();
	public Prototype len();
	
	public static class Builtins {

		public static Prototype switch_(Prototype value, Prototype fundict) {
			throw new UnsupportedOperationException();
		}

		public static Prototype match(Prototype value,	Prototype fundict) {
			throw new UnsupportedOperationException();
		}

		public static SlotPrototype bless(Prototype d) {
			return new SlotPrototype(d);
		}
	}
	
}