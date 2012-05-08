/**
 * 
 */
package butts.prototype;

import java.util.Collections;

final class NonePrototype extends FixedPrototype {

	private static DictPrototype slots = null;

	public NonePrototype() {
		super(slots);
	}
	public String toString() {
		return "<none>";
	}
	
	public boolean bool() {
		return false;
	}
	public static void createSlotTable() {
		slots = Prototypes.dict();
	}
	public static void fillSlotTable() {
		slots.setitem(Prototypes.__bool__, Prototypes.methodReturnsValue(Prototypes.False));
		slots.dict = Collections.unmodifiableMap(slots.dict);
	}
}