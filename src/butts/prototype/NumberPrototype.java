/**
 * 
 */
package butts.prototype;

import java.math.BigDecimal;
import java.util.Collections;
import java.util.List;

import butts.Prototype;
final class NumberPrototype extends FixedPrototype {
	private static DictPrototype slots = null;

	final BigDecimal num;

	public NumberPrototype(int i) {
		super(slots);
		this.num = new BigDecimal(i);
	}
	public NumberPrototype(BigDecimal bigDecimal) {
		super(slots);
		this.num = bigDecimal;
	}
	
	static int getInt(Prototype p) {
		return ((NumberPrototype)p).num.intValue();
	}
	static BigDecimal getBigNum(Prototype p) {
		return ((NumberPrototype)p).num;		
	}
	@Override
	public boolean equals(Object other) {
		if (other instanceof NumberPrototype) {
			return num.equals(((NumberPrototype) other).num);				
		}
		return false;
	}

	@Override
	public int hashCode() {
		return num.hashCode();
	}
	
	public String toString() {
		return "<int:"+num+">";
	}
	public static void createSlotTable() {
		slots = Prototypes.dict();		
	}
	public static void fillSlotTable() {
		slots.setitem(Prototypes.__int__, Prototypes.METHOD_RETURN_SELF);
		slots.setitem(Prototypes.__bool__, Prototypes.METHOD_RETURN_BOOL);
		slots.setitem(Prototypes.__add__, Prototypes.method(new AbstractFunctionPrototype() {
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return new NumberPrototype(getBigNum(args.get(0)).add(getBigNum(args.get(1))));
			}
		}));
		slots.setitem(Prototypes.__mul__, Prototypes.method(new AbstractFunctionPrototype() {
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return new NumberPrototype(getBigNum(args.get(0)).multiply(getBigNum(args.get(1))));
						}
		}));
		slots.setitem(Prototypes.__div__, Prototypes.method(new AbstractFunctionPrototype() {
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return new NumberPrototype(getBigNum(args.get(0)).divide(getBigNum(args.get(1))));
						}
		}));
		slots.setitem(Prototypes.__sub__, Prototypes.method(new AbstractFunctionPrototype() {
			@Override
			public Prototype call(List<Prototype> args, Prototype l, Prototype k) {
				return new NumberPrototype(getBigNum(args.get(0)).subtract(getBigNum(args.get(1))));
						}
		}));
		slots.dict = Collections.unmodifiableMap(slots.dict);
			
	}

}