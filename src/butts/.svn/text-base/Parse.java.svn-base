package butts;

import org.codehaus.jparsec.OperatorTable;
import org.codehaus.jparsec.Parser;
import org.codehaus.jparsec.Parsers;
import org.codehaus.jparsec.Scanners;
import org.codehaus.jparsec.Terminals;
import org.codehaus.jparsec.functors.Binary;
import org.codehaus.jparsec.functors.Map;
import org.codehaus.jparsec.functors.Unary;

import butts.Ast.BlockBuilder;
import butts.Ast.Expr;
import butts.Emulator.Block;
import butts.Emulator.Machine;
import butts.Emulator.OpCode;
import butts.prototype.Prototypes;

public class Parse {

	public static void main(String[] args) {
		Expr parse = P.parse("(8 + 1) * (4 - 3)");
		Expr prototypeExpression = new Ast.ReturnExpression(parse);
		BlockBuilder blockBuilder = new BlockBuilder();
		prototypeExpression.compile(blockBuilder);
		
		Block b = blockBuilder.getBlock();
		for (OpCode c: b.code) {
			System.out.println(c);
		}
		
		Machine m = new Machine(Prototypes.None, b);
		
		Prototype exec = m.exec();
		System.out.println(exec);
	}
	
	  enum BinaryOperator implements Binary<Expr> {
		    PLUS {
		      public Expr map(Expr a, Expr b) {
		        return new Ast.AddExpression(a,b);
		      }
		    },
		    MINUS {
		      public Expr map(Expr a, Expr b) {
		    	   return new Ast.SubExpression(a,b);
		    }
		    },
		    MUL {
		      public Expr map(Expr a, Expr b) {
		    	   return new Ast.MulExpression(a,b);
		      }
		    },
		    DIV {
		      public Expr map(Expr a, Expr b) {
		    	   return new Ast.DivExpression(a,b);
				     
		      }
		    }
		  }
		  
		  enum UnaryOperator implements Unary<Expr> {
		    NEG {
		      public Expr map(Expr n) {
		        return new Ast.SubExpression(new Ast.NumberExpr(0), n);
		      }
		    }
		  }
		  
		  static final Parser<Expr> NUMBER = Terminals.DecimalLiteral.PARSER.map(new Map<String, Expr>() {
		      public Expr map(String s) {
		        return new Ast.NumberExpr(s);
		      }
		    });
		     
		  private static final Terminals OPERATORS = Terminals.operators("+", "-", "*", "/", "(", ")");
		  
		  static final Parser<Void> IGNORED =
		      Parsers.or(Scanners.JAVA_LINE_COMMENT, Scanners.JAVA_BLOCK_COMMENT, Scanners.WHITESPACES).skipMany();
		      
		  static final Parser<?> TOKENIZER =
		      Parsers.or(Terminals.DecimalLiteral.TOKENIZER, OPERATORS.tokenizer());
		  
		  static Parser<?> term(String... names) {
		    return OPERATORS.token(names);
		  }
		  
		  static <T> Parser<T> op(String name, T value) {
		    return term(name).retn(value);
		  }
		  
		  static Parser<Expr> make(Parser<Expr> atom) {
		    Parser.Reference<Expr> ref = Parser.newReference();
		    Parser<Expr> unit = ref.lazy().between(term("("), term(")")).or(atom);
		    Parser<Expr> parser = new OperatorTable<Expr>()
		        .infixl(op("+", BinaryOperator.PLUS), 10)
		        .infixl(op("-", BinaryOperator.MINUS), 10)
		        .infixl(op("*", BinaryOperator.MUL), 20)
		        .infixl(op("/", BinaryOperator.DIV), 20)
		        .prefix(op("-", UnaryOperator.NEG), 30)
		        .build(unit);
		    ref.set(parser);
		    return parser;
		  }
		  
		  public static final Parser<Expr> P = make(NUMBER).from(TOKENIZER, IGNORED);
}
