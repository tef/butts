/**
 * 
 */
package butts.prototype;

import java.util.Collections;
import java.util.List;

import butts.Prototype;

public abstract class AbstractFunctionPrototype extends FixedPrototype {

	private static DictPrototype slots = null;


	public AbstractFunctionPrototype() {
		super(slots);
	}

	abstract public Prototype call(List<Prototype> args, Prototype listargs, Prototype dictargs);
	
	public String toString() {
		return "<function:"+hashCode()+">";
	}

	public static void createSlotTable() {
		slots = Prototypes.dict();
	}

	public static void fillSlotTable() {
		slots.setitem(Prototypes.__call__, Prototypes.DESCRIPTOR_RETURN_SELF);
		slots.setitem(Prototypes.__bool__, Prototypes.methodReturnsValue(Prototypes.True));
		slots.dict = Collections.unmodifiableMap(slots.dict);
	}
}