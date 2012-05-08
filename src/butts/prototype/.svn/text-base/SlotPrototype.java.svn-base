/**
 * 
 */
package butts.prototype;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import butts.Prototype;

public class SlotPrototype implements Prototype {
	/** A prototype 
	 * 
	 * 
	 *  All prototypes have a number of java methods that correspond to python builtin functions
	 * 		getattr(), call(), etc.
	 * 
	 **/
	
	
	
	protected Prototype __slots__;

	public SlotPrototype() {
		this.__slots__ = Prototypes.dict();
	}

	public SlotPrototype(Prototype slots) {
		this.__slots__ = slots;
	}
	
	// * used after prototype initialization to freeze the slots for built in types

	// Contains the attribute
	public boolean hasattr(Prototype name) {
		try {
			getattr(name);
			return true;
		} catch (WrappedPrototypeException e) {
			return false;
		}
	}
	
	// Get an attribute - either it is in the slots, or one of the slots
	// is a __getattr__ function which can be called to get the value.
	public Prototype getattr(Prototype name) {
		if (Prototypes.__slots__.equals(name)) {
			return __slots__;
		}

		Prototype attr = null;
		if (__slots__.contains(name)) {
			attr = __slots__.getitem(name);
		} else {
			if (!Prototypes.__getattr__.equals(name) && __slots__.contains(Prototypes.__getattr__)) {
				attr= callattr(Prototypes.__getattr__,Collections.singletonList(name));
			} else {
				throw new WrappedPrototypeException(Prototypes.string("missing prototype"));
			}
		}
		// Descriptors
		// When you retrieve an attribute, you call the __get__ attribute it contains
		// and pass it the attribute itself and the containing object
		
		// Descriptors allow us to implement methods, explained further below

		if (attr.hasattr(Prototypes.__get__)) {
			attr = attr.callattr(Prototypes.__get__, Arrays.asList(attr, this));
		} 
		return attr;
	}

	public void setattr(Prototype name, Prototype value) {
		if (Prototypes.__slots__.equals(name)) {
			__slots__ = value;
		} else {
			if (__slots__.contains(Prototypes.__setattr__)) {
				callattr(Prototypes.__setattr__, Arrays.asList(name, value));
			} else {
				try {
					if (__slots__.hasattr(name) && __slots__.getattr(name).hasattr(Prototypes.__set__)) {
						__slots__.getattr(name).callattr(Prototypes.__set__, Arrays.asList(value));
					} else {
						__slots__.setitem(name, value);	
					}
				} catch (UnsupportedOperationException e) {
					throw new WrappedPrototypeException(Prototypes.string("prototype is immutable"));
				}
			}
		}
	}

	public void delattr(Prototype name) {
		if (Prototypes.__slots__.equals(name)) {
			__slots__ = Prototypes.None;
		} else {
			if (__slots__.contains(Prototypes.__delattr__)) {
				callattr(Prototypes.__delattr__, Arrays.asList(name));
			} else {
				try {
					if (__slots__.hasattr(name) && __slots__.getattr(name).hasattr(Prototypes.__del__)) {
						__slots__.getattr(name).callattr(Prototypes.__del__, Collections.<Prototype>emptyList());
					} else {
						__slots__.delitem(name);				
					}
				} catch (WrappedPrototypeException e) {
					throw new WrappedPrototypeException(Prototypes.string("prototype is immutable"));
				}
			}
		}
			

	}
	/** these are useful java methods that forward the call to the corresponding slots **/
	public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
		return getattr(Prototypes.__call__).call(args, l,k);
	}
	
	public boolean bool() {
		return callattr(Prototypes.__bool__, Collections.<Prototype>emptyList()).bool();
	}
	
	
	public Prototype callattr(Prototype name, List<Prototype> args) {
		return getattr(name).call(args, Prototypes.EmptyList, Prototypes.EmptyList);
	}
	
	
	public Prototype getitem(Prototype args) {
		return callattr(Prototypes.__getitem__, Arrays.asList(args));
	}
	
	public void delitem(Prototype args) {
		callattr(Prototypes.__delitem__, Arrays.asList(args));
	}

	public void setitem(Prototype arg, Prototype val) {
		callattr(Prototypes.__setitem__, Arrays.asList(arg, val));
	}
	
	public boolean contains(Prototype name) {
		return callattr(Prototypes.__contains__, Collections.<Prototype>singletonList(name)).bool();
	}

	
	public String toString() {
    	return getClass().getName() + "@" + Integer.toHexString(super.hashCode());
    }

	@Override
	public Prototype iter() {
		return callattr(Prototypes.__iter__, Collections.<Prototype>emptyList());
	}

	@Override
	public Prototype len() {
		return callattr(Prototypes.__len__, Collections.<Prototype>emptyList());
	}

	@Override
	public Prototype next() {
		return callattr(Prototypes.__next__, Collections.<Prototype>emptyList());
	}
}