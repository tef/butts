/**
 * 
 */
package butts.prototype;

import java.util.Collections;

public final class BooleanPrototype extends FixedPrototype {
	private static DictPrototype slots = null;

	private final Boolean b;
	BooleanPrototype(boolean b) {
		super(slots);
		this.b = b;
	}

	@Override
	public boolean equals(Object other) {
		if (other instanceof BooleanPrototype) {
			return b.equals(((BooleanPrototype)other).b);				
		}
		return false;
	}

	public boolean bool() {
		return b;
	}
	@Override
	public int hashCode() {
		return b.hashCode();
	}
	public String toString() {
		return "<"+b+">";
	}

	public static void createSlotTable() {
		slots = Prototypes.dict();
	}

	public static void fillSlotTable() {
		slots.setitem(Prototypes.__bool__, Prototypes.METHOD_RETURN_SELF);
		slots.dict = Collections.unmodifiableMap(slots.dict);
			
	}
}