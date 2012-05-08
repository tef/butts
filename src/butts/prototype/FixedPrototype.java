/**
 * 
 */
package butts.prototype;

import butts.Prototype;

abstract public class FixedPrototype extends SlotPrototype {

	public FixedPrototype(Prototype slots) {
		super(slots);
	}

	public FixedPrototype() {
		super();
	}
	

	public void setattr(Prototype name, Prototype value) {
		throw new WrappedPrototypeException(Prototypes.string("prototype is immutable"));
	}

}