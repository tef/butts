package butts.prototype;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import butts.Prototype;


public final class Prototypes {
	
	
	
	public static void main (String[] args) {
		
		Prototype two = number(2);
		// 2 + 2
		System.out.println(two.callattr(__add__, Collections.singletonList(two)));
	

		// p = object { "cocks": 1919, "foo" : method (function (self) { return self.cocks }) }
		
		Prototype p = new SlotPrototype();
		p.setattr(string("cocks"),number(1919));
		
		p.setattr(string("foo"),method(new AbstractFunctionPrototype() {
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return args.get(0).getattr(string("cocks"));
			}

		}));
		
		System.out.println(p.callattr(string("foo"), Collections.<Prototype>emptyList()));
		
		
		AbstractFunctionPrototype functionPrototype = new AbstractFunctionPrototype() {
			
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return null;
			}
		};
		System.out.println(functionPrototype);
		System.out.println(functionPrototype.getattr(__call__));
		
		
	}

	public static StringPrototype string(String s) {
		return new StringPrototype(s);
	}
	public static NumberPrototype number(int i) {
		return new NumberPrototype(i);
	}
	public static SlotPrototype prototype() {
		return new SlotPrototype();
	}
	public static DictPrototype dict(Map<Prototype,Prototype> dict) {
		return new DictPrototype(dict);
	}

	public static DictPrototype dict() {
		return new DictPrototype(new LinkedHashMap<Prototype, Prototype>());
	}
	

	static {
		DictPrototype.createSlotTable();
		BooleanPrototype.createSlotTable();
		AbstractFunctionPrototype.createSlotTable();
		NonePrototype.createSlotTable();
		NumberPrototype.createSlotTable();
		StringPrototype.createSlotTable();
		TuplePrototype.createSlotTable();
		ListPrototype.createSlotTable();
	}
	
	// Attribute protocol
	public static final StringPrototype __getattr__ = string("__getattr__");
	public static final StringPrototype __setattr__ = string("__setattr__");
	public static final StringPrototype __delattr__ = string("__delattr__");

	// Function protocol
	public static final StringPrototype __call__ = string("__call__");
	
	// Casting protocol
	public static final StringPrototype __str__ = string("__str__");
	public static final StringPrototype __bool__ = string("__bool__");
	public static final StringPrototype __int__ = string("__int__");
	
	// A + B is A.__add__(B)
	public static final StringPrototype __add__ = string("__add__");
	public static final StringPrototype __mul__ = string("__mul__");
	public static final StringPrototype __div__ = string("__div__");
	public static final StringPrototype __sub__ = string("__sub__");

	// For methods, this attribute contains the wrapped function
	public static final StringPrototype __func__ = string("__func__");
	
	// Descriptor protocol, allows us to override attribute access per attribute
	public static final StringPrototype __get__ = string("__get__");
	public static final StringPrototype __del__ = string("__del__");
	public static final StringPrototype __set__ = string("__set__");

	// Dictionary protocol, allows us to override attribute access per attribute
	public static final StringPrototype __getitem__ = string("__getitem__");
	public static final StringPrototype __delitem__ = string("__delitem__");
	public static final StringPrototype __setitem__ = string("__setitem__");

	public static final StringPrototype __contains__ = string("__contains__");

	public static final StringPrototype __len__ = string("__len__");
	public static final StringPrototype __iter__ = string("__iter__");
	public static final StringPrototype __next__ = string("__next__");


	// This is the prototypes slots
	public static final StringPrototype __slots__ = string("__slots__");

	
	// Built in types
	
	public static final Prototype True = new BooleanPrototype(true);
	public static final Prototype False = new BooleanPrototype(false);
	public static final Prototype None = new NonePrototype();
	public static final Prototype EmptyList = new TuplePrototype(Collections.<Prototype>emptyList());
	

	private static AbstractFunctionPrototype BOUND_FUNCTION = new AbstractFunctionPrototype() {
		@Override
		public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
			final Prototype me = args.get(0);
			final Prototype owner = args.get(1); 
			return new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype listargs, Prototype dictargs) {
					ArrayList<Prototype> arrayList = new ArrayList<Prototype>();
					arrayList.add(owner);
					arrayList.addAll(args);
					return me.getattr(Prototypes.__func__).call(arrayList, listargs, dictargs);
				}
			};
		}
	};
	
	
	public static Prototype method(final Prototype f) {
		Prototype p = new SlotPrototype() {
			public String toString() {
				return "<bound method>";
			};
		};
		p.setattr(Prototypes.__func__, f);	
		p.setattr(Prototypes.__get__, BOUND_FUNCTION);
		return p;
	}
	
	
	// this is for things like __str__, so that if you
	// ask for .a= "foo".__str__, a() is "foo";
	static final Prototype METHOD_RETURN_SELF = method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					return args.get(0);
				}
			}
	);
	static final Prototype METHOD_RETURN_BOOL = method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					return args.get(0).bool() ? True : False;
				}
			}
	);
	

	public static final Prototype METHOD_GETITEM =  method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					return args.get(0).getitem(args.get(1));
				}
			}
	);
	public static final Prototype METHOD_SETITEM =  method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					args.get(0).setitem(args.get(1), args.get(2));
					return None;
				}
			}
	);
	public static final Prototype METHOD_DELITEM =  method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					args.get(0).delitem(args.get(1));
					return None;
				}
			}
	);
	public static final Prototype METHOD_CONTAINS =  method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					return args.get(0).contains(args.get(1)) ? True : False;
				}
			}
	);


	static final Prototype methodReturnsValue(final Prototype ret) { 
		return method(
			new AbstractFunctionPrototype() {
				@Override
				public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
					return ret;
				}
			}
		);
	}
	
	// this is for things like __call__
	
	static final Prototype DESCRIPTOR_RETURN_SELF = new SlotPrototype();
	static {
		DESCRIPTOR_RETURN_SELF.setattr(__get__, new AbstractFunctionPrototype() {			
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return args.get(1);
			}
		});
	}
	
	static {
		DictPrototype.fillSlotTable();
		BooleanPrototype.fillSlotTable();
		AbstractFunctionPrototype.fillSlotTable();
		NonePrototype.fillSlotTable();
		NumberPrototype.fillSlotTable();
		StringPrototype.fillSlotTable();
		ListPrototype.fillSlotTable();
		TuplePrototype.fillSlotTable();
	}

	
	
}
