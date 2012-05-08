 package butts;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


import butts.Ast.Expr;
import butts.Emulator.Block;
import butts.Emulator.Instructions;
import butts.Emulator.Machine;
import butts.Emulator.OpCode;
import butts.Emulator.OpInstruction;
import butts.prototype.Prototypes;

public class Ast {

	public static void main(String[] args) {
		Expr prototypeExpression = new ReturnExpression(new SubExpression( new AddExpression(new NumberExpr(7), new NumberExpr(2)),new AddExpression( new NumberExpr(2),new NumberExpr(2))));

		BlockBuilder blockBuilder = new BlockBuilder();
		prototypeExpression.compile(blockBuilder);
		
		Block b = blockBuilder.getBlock();
		
		System.out.println(b.code);
		
		Machine m = new Machine(Prototypes.None, b);
		
		Prototype exec = m.exec();
		System.out.println(exec);
	}

	static abstract class Expr {
		abstract public VmRef compile(BlockBuilder blockBuilder);
	}
	
	static class ExprVar extends Expr {
		private final String name;

		public ExprVar(String name) {
			this.name = name;
			
		}

		@Override
		public VmRef compile(BlockBuilder blockBuilder) {
			return blockBuilder.defVar(name);
		}
	}

	static abstract class ExprArgs extends Expr {
		List<Expr> args;

		public ExprArgs(Expr... args) {
			this.args = Arrays.asList(args);
		}

		public VmRef compile(BlockBuilder blockBuilder) {
			ArrayList<VmRef> arg_regs = new ArrayList<VmRef>(args.size());
			for (Expr a: args) {
				arg_regs.add(a.compile(blockBuilder));
			}
			return addInstructions(arg_regs, blockBuilder);
		}

		abstract VmRef addInstructions(ArrayList<VmRef> argLocal, BlockBuilder blockBuilder);
	}

	static class NumberExpr extends Expr {

		private final int n;
		public NumberExpr(int n) {
			this.n = n;
		}
		public NumberExpr(String s) {
			this.n = Integer.parseInt(s);
		}
		
		@Override
		public VmRef compile(BlockBuilder blockBuilder) {
			return blockBuilder.storeConst(Prototypes.number(n));
		}

	}

	static class AddExpression extends ExprArgs {

		public AddExpression(Expr... args) {
			super(args);
		}
		@Override
		VmRef addInstructions(ArrayList<VmRef> argLocal, BlockBuilder blockBuilder) {
			return blockBuilder.pushThreeArg(Instructions.ADD,argLocal);
		}
	}

	static class MulExpression extends ExprArgs {

		public MulExpression(Expr... args) {
			super(args);
		}
		@Override
		VmRef addInstructions(ArrayList<VmRef> argLocal, BlockBuilder blockBuilder) {
			return blockBuilder.pushThreeArg(Instructions.MUL, argLocal);
		}
	}
	static class SubExpression extends ExprArgs {

		public SubExpression(Expr... args) {
			super(args);
		}
		@Override
		VmRef addInstructions(ArrayList<VmRef> argLocal, BlockBuilder blockBuilder) {
			return blockBuilder.pushThreeArg(Instructions.SUB,argLocal);
		}
	}
	static class DivExpression extends ExprArgs {

		public DivExpression(Expr... args) {
			super(args);
		}
		@Override
		VmRef addInstructions(ArrayList<VmRef> argLocal, BlockBuilder blockBuilder) {
			return blockBuilder.pushThreeArg(Instructions.DIV,argLocal);
		}
	}
	
	static class ReturnExpression extends ExprArgs {

		public ReturnExpression(Expr... args) {
			super(args);
		}
		@Override
		VmRef addInstructions(ArrayList<VmRef> argLocal, BlockBuilder blockBuilder) {
			return blockBuilder.pushReturn(argLocal);
		}
	}
	interface VmRef {

		int getLocalRef(BlockBuilder blockBuilder);
	}

	static class FrameReference implements VmRef {
		private final int out;

		public FrameReference(int out) {
			this.out = out;
		}

		@Override
		public
		int getLocalRef(BlockBuilder blockBuilder) {
			return out;
		}

	}

	static class DataReference implements VmRef {

		private final int indexOf;
		private int local = -1;

		public DataReference(int indexOf) {
			this.indexOf = indexOf;
		}

		@Override
		public
		int getLocalRef(BlockBuilder blockBuilder) {
			if (local < 0) {
				local = blockBuilder.getNextLocal();
				blockBuilder.pushOpCode(Instructions.LOAD.args(indexOf, local));			
			}
			return local;
		}

	}
	static class BlockBuilder {

		List<Prototype> data = new ArrayList<Prototype>();
		ArrayList<OpCode> code = new ArrayList<OpCode>();
		Map<String, VmRef> vars = new HashMap<String,VmRef>();
		
		int next_reg = 0;

		public VmRef storeConst(Prototype p) {
			if (data.contains(p)) return new DataReference(data.indexOf(p));
			data.add(p);
			return new DataReference(data.size()-1);
		}

		public VmRef defVar(String name) {
			if (vars.containsKey(name)) return vars.get(name);
			DataReference ref = new DataReference(getNextLocal());
			vars.put(name, ref);
			return ref;
		}

		public VmRef getVar(String name) {
			if (!vars.containsKey(name)) throw new RuntimeException();
			return vars.get(name);
		}

		public VmRef pushReturn(ArrayList<VmRef> argLocal) {
			VmRef left = argLocal.get(0);
			pushOpCode(Instructions.RETURN.args(left.getLocalRef(this)));
			return left;
		}

		public Block getBlock() {
			code.add(0, Instructions.FRAMERESIZE.args(next_reg));
			code.add(Instructions.RETURN.args(0));
			return new Block(data, code);
		}

		public VmRef pushThreeArg(OpInstruction  i, ArrayList<VmRef> argLocal) {
			int left = argLocal.get(0).getLocalRef(this);
			int right = argLocal.get(1).getLocalRef(this);
			int out = getNextLocal();
			pushOpCode(i.args(left, right, out));
			return new FrameReference(out);
		}
		
		private void pushOpCode(OpCode add) {
			code.add(add);
		}

		private int getNextLocal() {
			return 2+next_reg++;
		}

	}
}
