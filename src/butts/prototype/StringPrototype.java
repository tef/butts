/**
 * 
 */
package butts.prototype;

import java.util.Collections;

final class StringPrototype extends FixedPrototype {
	private static DictPrototype slots = null;
	
	private final String str;

	StringPrototype(String s) {
		super(slots);
		this.str = s;
	}

	@Override
	public boolean equals(Object other) {
		if (other instanceof StringPrototype) {
			return str.equals(((StringPrototype)other).str);	
		}
		return false;
	}

	@Override
	public int hashCode() {
		return str.hashCode();
	}
	

	public String toString() {
		return "<string:"+str+">";
	}

	public boolean bool() {
		return !str.isEmpty();
	}

	public static void createSlotTable() {
		slots = Prototypes.dict();		
	}

	public static void fillSlotTable() {
		slots.setitem(Prototypes.__str__, Prototypes.METHOD_RETURN_SELF);
		slots.setitem(Prototypes.__bool__, Prototypes.METHOD_RETURN_BOOL);
		slots.dict = Collections.unmodifiableMap(slots.dict);
	}
}