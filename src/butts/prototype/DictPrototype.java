/**
 * 
 */
package butts.prototype;

import java.util.LinkedHashMap;
import java.util.Map;

import butts.Prototype;

public final class DictPrototype extends FixedPrototype {
	private static DictPrototype hashmapslots = null;
	// not final for bootstrap reasons :(
	Map<Prototype, Prototype> dict;

	DictPrototype(Map<Prototype, Prototype> wrapped) {
		super(hashmapslots);
		this.dict = wrapped;
	}
	private DictPrototype() {
		super((Prototype)null);
		this.dict = new LinkedHashMap<Prototype, Prototype>();
		this.__slots__ = this;
	}

	public Prototype getitem(Prototype args) {
		 Prototype p = this.dict.get(args);
		 if (p == null) throw new WrappedPrototypeException(Prototypes.string("missing item"));
		 return p;
	}
	
	public void delitem(Prototype args) {
		 Prototype p = this.dict.remove(args);
		 if (p == null) throw new WrappedPrototypeException(Prototypes.string("missing item"));
	}

	public void setitem(Prototype arg, Prototype val) {
		 this.dict.put(arg,val);
	}
	
	public boolean contains(Prototype name) {
		return this.dict.containsKey(name);
	}
	
	@Override
	public boolean equals(Object other) {
		if (other instanceof DictPrototype) {
			return dict.equals(((DictPrototype)other).dict);	
		}
		return false;
	}

	@Override
	public int hashCode() {
		return dict.hashCode();
	}
	

	public String toString() {
		return "<slots:"+dict+">";
	}

	public boolean bool() {
		return !dict.isEmpty();
	}
	
	static void createSlotTable() {
		hashmapslots = new DictPrototype();
	}
	static void fillSlotTable() {
		hashmapslots.setitem(Prototypes.__bool__, Prototypes.METHOD_RETURN_BOOL);
		hashmapslots.setitem(Prototypes.__getitem__, Prototypes.METHOD_GETITEM);
		hashmapslots.setitem(Prototypes.__setitem__, Prototypes.METHOD_SETITEM);
		hashmapslots.setitem(Prototypes.__delitem__, Prototypes.METHOD_DELITEM);
		hashmapslots.setitem(Prototypes.__contains__, Prototypes.METHOD_CONTAINS);		
	}
	

}