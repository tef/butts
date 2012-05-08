/**
 * 
 */
package butts.prototype;

import java.util.List;

import butts.Prototype;

public final class ListPrototype extends FixedPrototype {
	private static DictPrototype slots = null;
	// not final for bootstrap reasons :(
	List<Prototype> list;

	ListPrototype(List<Prototype> wrapped) {
		super(slots);
		this.list = wrapped;
	}
	
	public Prototype getitem(Prototype args) {
		 Prototype p = this.list.get(((NumberPrototype)args).num.intValue());
		 if (p == null) throw new WrappedPrototypeException(Prototypes.string("missing item"));
		 return p;
	}
	
	public void delitem(Prototype args) {
		 boolean p = this.list.remove(args);
		 if (!p) throw new WrappedPrototypeException(Prototypes.string("missing item"));
	}

	public void setitem(Prototype arg, Prototype val) {
		 this.list.set(((NumberPrototype)arg).num.intValue(), val);
	}
	
	public boolean contains(Prototype name) {
		return this.list.contains(name);
	}
	
	@Override
	public boolean equals(Object other) {
		if (other instanceof ListPrototype) {
			return list.equals(((ListPrototype)other).list);	
		}
		if (other instanceof TuplePrototype) {
			return list.equals(((TuplePrototype)other).list);	
		}
		return false;
	}

	@Override
	public int hashCode() {
		return list.hashCode();
	}
	

	public String toString() {
		return "<slots:"+list+">";
	}

	public boolean bool() {
		return !list.isEmpty();
	}
	
	static void createSlotTable() {
		slots = Prototypes.dict();
	}
	static void fillSlotTable() {
		slots.setitem(Prototypes.__bool__, Prototypes.METHOD_RETURN_BOOL);
		slots.setitem(Prototypes.__getitem__, Prototypes.METHOD_GETITEM);
		slots.setitem(Prototypes.__setitem__, Prototypes.METHOD_SETITEM);
		slots.setitem(Prototypes.__delitem__, Prototypes.METHOD_DELITEM);
		slots.setitem(Prototypes.__contains__, Prototypes.METHOD_CONTAINS);		
	}
	

}