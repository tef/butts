package butts;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


import butts.Prototype.Builtins;
import butts.prototype.Prototypes;

public class Emulator {

	public static void main(String[] args) {
		ArrayList<OpCode> code = new ArrayList<OpCode>();
		List<Prototype> data = new ArrayList<Prototype>();
		Prototype two = Prototypes.number(2);
		data.add(two);
		data.add(Prototypes.__add__);
		code.add(Instructions.FRAMERESIZE.args(3));
		code.add(Instructions.LOAD.args(0, 2));
		code.add(Instructions.LOAD.args(1, 3));
		
		code.add(Instructions.GETATTR.args(2, 3, 3));
		code.add(Instructions.CALL.args(3, 2, 1, 0, 0, 2));
		code.add(Instructions.RETURN.args(2));


		Machine m = new Machine(Prototypes.None, code, data);
		Prototype exec = m.exec();
		System.out.println(exec);
	}

	public static class OpCode {
		OpInstruction i;
		int[] d;

		public OpCode(OpInstruction i, int... d) {
			this.i = i;
			this.d = d;
		}

		public boolean exec(Machine machine) {
			return i.exec(machine, d);
		}
		
		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append(i);
			for (int d : this.d) {
				sb.append(" ");
				sb.append(d);
			}
			return sb.toString();
		}
	}

	public interface OpInstruction {
		public boolean exec(Machine m, int... args);
		public OpCode args(int... a);
	}

	public static class Block {
		public Block(List<Prototype> data2, List<OpCode> code2) {
			code = code2;
			data = data2;
		}
		List<OpCode> code;
		List<Prototype> data;	
	}
	public static class Machine {
		List<OpCode> code;
		List<Prototype> frame;
		List<Prototype> data;
		private int value = 0;
		private int pc = 0;

		public Machine(Prototype global, List<OpCode> code, List<Prototype> data) {
			this.code = code;
			this.data = data;
			this.frame = new ArrayList<Prototype>(2);
			frame.add(Prototypes.None);
			frame.add(global);
		}

		public Machine(Prototype global, Block block) {
			this.code = block.code;
			this.data = block.data;
			this.frame = new ArrayList<Prototype>(2);
			frame.add(Prototypes.None);
			frame.add(global);
		}
		Prototype call(List<Prototype> args) {
			return null;
		}

		Prototype exec() {
			while (code.get(pc).exec(this)) {
				System.out.println("step");
				pc++;
			}
			return register(value);

		}

		private Prototype register(int value) {
			return frame.get(value);
		}

		public void setReturn(int value) {
			this.value = value;

		}
		public void set(int out, Prototype getattr) {
			System.out.println(" setting r("+out+") to "+getattr);
			if (out == 0) return;
			frame.set(out, getattr);
		}
		public void resizeFrame(int diff) {
			if (diff > 0) {
				while (diff-- > 0)
					frame.add(Prototypes.None);
			} else if (diff < 0) {
				while (diff++ < 0) {
					frame.remove(frame.size()-1);
				}
			}
		}
		public Prototype local(int offset) {
			return data.get(offset);
		} 


	}


	enum Instructions implements OpInstruction {
		ADD {
			@Override
			public boolean exec(Machine m, int... args) {
				m.set(args[2], m.register(args[0]).callattr(Prototypes.__add__, Collections.<Prototype>singletonList(m.register(args[1]))));
				return true; 
			}
		},
		MUL {
			@Override
			public boolean exec(Machine m, int... args) {
				m.set(args[2], m.register(args[0]).callattr(Prototypes.__mul__, Collections.<Prototype>singletonList(m.register(args[1]))));
				return true; 
			}
		},
		SUB {
			@Override
			public boolean exec(Machine m, int... args) {
				m.set(args[2], m.register(args[0]).callattr(Prototypes.__sub__, Collections.<Prototype>singletonList(m.register(args[1]))));
				return true; 
			}
		},
		DIV {
			@Override
			public boolean exec(Machine m, int... args) {
				m.set(args[2], m.register(args[0]).callattr(Prototypes.__div__, Collections.<Prototype>singletonList(m.register(args[1]))));
				return true; 
			}
		},
		GETATTR {
			@Override
			public boolean exec(Machine m, int... args) {
				Prototype register = m.register(args[0]);
				Prototype register2 = m.register(args[1]);
				System.out.println("GETATTR r("+args[0]+").r("+args[1]+")  "+register+"."+register2+" --> r("+args[2]+")");
				m.set(args[2],register.getattr(register2));
				return true;
			}
		},
		SETATTR { 
			public boolean exec(Machine m,int... args) {
				int object = args[0];
				int name = args[1];
				int value = args[2];
				m.register(object).setattr(m.register(name), m.register(value));

				return true; 
			}
		},
		CALL {
			@Override
			public boolean exec(Machine m,int... args) {
				System.out.println("CALL");
				int object = args[0];
				int start = args[1];
				int offset = args[2];
//				int largs = args[3];
//				int dargs = args[4];
				int output = args[5];

				Prototype register = m.register(object);
				m.set(output,register.call(m.frame.subList(start, start+offset), Prototypes.EmptyList, Prototypes.EmptyList));
				return true; 
			}
		},
		RETURN {
			@Override
			public boolean exec(Machine m, int... args) {
				int value = args[0];

				System.out.println("RETURN");
				m.setReturn(value);
				return false; 
			}
		},
		MOVE {
			@Override
			public boolean exec(Machine m, int... args) {
				int offset = args[0];
				int out = args[1];

				Prototype local = m.local(offset);
				System.out.println("LOAD "+local+"-> r("+out+")");
				m.set(out, local);
				return true; 
			}
		},
		THROW{
			@Override
			public boolean exec(Machine m, int... args) {
				// TODO Auto-generated method stub
				return false;
			}
		},
		RESCUE{
			@Override
			public boolean exec(Machine m, int... args) {
				// TODO Auto-generated method stub
				return false;
			}
		},
		CUTRESCUE{
			@Override
			public boolean exec(Machine m, int... args) {
				// TODO Auto-generated method stub
				return false;
			}
		},
		JUMP{
			@Override
			public boolean exec(Machine m, int... args) {
				m.pc +=(args[0]-1);
				return true;
			}
		},
		BOOLJUMP{
			@Override
			public boolean exec(Machine m, int... args) {
				if (m.register(args[0]).bool()) m.pc +=(args[1]-1);
				return true;
			}
		},
		SWITCH{
			@Override
			public boolean exec(Machine m, int... args) {
				m.set(args[2],Builtins.switch_(m.register(args[0]), m.register(args[1])));
				return true;
			}
		},
		MATCH{
			@Override
			public boolean exec(Machine m, int... args) {
				m.set(args[2],Builtins.match(m.register(args[0]), m.register(args[1])));
				return true;
			}
		},
		IMPORT{
			@Override
			public boolean exec(Machine m, int... args) {
					throw new UnsupportedOperationException();
			}
		},
		LOAD {
			@Override
			public boolean exec(Machine m, int... args) {
				int offset = args[0];
				int out = args[1];

				Prototype local = m.local(offset);
				System.out.println("LOAD "+local+"-> r("+out+")");
				m.set(out, local);
				return true; 
			}

		},
		FRAMERESIZE {
			@Override
			public boolean exec(Machine m, int... args) {
				int diff = args[0];

				System.out.println("frameresize:" + diff);
				m.resizeFrame(diff);
				return true; 
			}

		};

		public OpCode args(int... a) {
			return new OpCode(this, a);
		}

		abstract public boolean exec(Machine m, int... args);
	}

}
