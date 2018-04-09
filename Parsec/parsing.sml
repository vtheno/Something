signature Pc =
sig
(* in there tuple
   char list <=> String
   empty list <=> "" empty String
 *)
val mread : string -> char list
type 'a Parser = char list -> ('a * char list) list
(* val succeed : 'a -> char list -> ('a * char list) list *)
(* val succeed : a -> 'a Parser *)
val succeed : 'a -> 'a Parser
(* type Parser a = Char List -> [(a,Char List)] 
   succeed :: a -> Parser a
   succeed :: a -> Char List -> [(a,Char List)]
   succeed : 'a -> char list -> ('a * char list) list
*)
val fail : 'a Parser
val item : char Parser
val sat : (char -> bool) -> char Parser
val literal : char -> char Parser
val alt : 'a Parser -> 'a Parser -> 'a Parser
val seq : 'a Parser -> 'b Parser -> ('a * 'b) Parser
val using : 'a Parser -> ('a -> 'b Parser) -> 'b Parser
val many : 'a Parser -> 'a list Parser
val many1 : 'a Parser -> 'a list Parser
(* val pstring : char list -> char list Parser *)
val xthen : 'a Parser -> 'b Parser -> 'b Parser
val thenx : 'a Parser -> 'b Parser -> 'a Parser
val lower : char Parser
val upper : char Parser
val digit : char Parser
val letter : char Parser
val alphanum : char Parser
val word : char list Parser
val mChar : char -> char Parser
val mString : char list -> char list Parser
val ident : char list Parser
val nat : int Parser
val mInt : int Parser
val mInts : int list Parser
val sepby1 : 'a Parser -> 'b Parser -> 'a list Parser
val bracket : 'a Parser -> 'b Parser -> 'c Parser -> 'b Parser
val sepby : 'a Parser -> 'b Parser -> 'a list Parser
val chainl1 : 'a Parser -> ('a -> 'a -> 'a) Parser -> 'a Parser
val chainr1 : 'a Parser -> ('a -> 'a -> 'a) Parser -> 'a Parser
val foldr1 : ('a -> 'a -> 'a) -> 'a list -> 'a
val chainl : 'a Parser -> ('a -> 'a -> 'a) Parser -> 'a -> 'a Parser
val chainr : 'a Parser -> ('a -> 'a -> 'a) Parser -> 'a -> 'a Parser
val ops : ('a Parser * 'b) list -> 'b Parser
(* 
 val ops : ['a Parser * 'b] -> 'b Parser 
*)
(*
 val addop : (int -> int -> int) Parser
 val factor : int Parser
 val expr : int Parser
*)
end

structure P :> Pc =
struct
type 'a Parser = char list -> ('a * char list) list
val mread = String.explode
fun succeed v inp =  [(v,inp)]
fun fail inp = []
fun sat p [] = fail []
  | sat p (x::xs) = if p x then succeed x xs else fail xs
fun literal a = sat (fn t => t = a)
fun alt p1 p2 inp = (p1 inp) @ (p2 inp)
(* old seq 
 fun seq p q inp = 
     let val [(v,inp')] = p inp
     in let val [(w,inp'')] = q inp'
        in [ ( (v,w) ,inp'') ]
        end
     end
*)
(* old using
 fun using p f inp = 
     let val [(v,out)] = p inp 	(* because p inp maybe more length not only one *)
     in [(f v out)]
     end 
 *)
fun using p f inp = 
    let val temp = p inp 
	fun uncurry f = fn (a,b) => f a b
    in List.concat (List.map (uncurry f) temp)
		   (* u need something about list map and concat and function uncurry *)
		   (* p >>= f = [f (a,b) | (a,b) <- p inp ] 
		      [ (a,b) | (a,b) <- p inp ]
		      [ (a,b) | (a,b) <- zip [1..2] [4..5]]  is [(1,4),(2,5)]
		      zip [1,2] [4,5] is [(1,4),(2,5)]
		      then (a,b) <- e 
		      like python [ i for i in e ]
		      so,
		     this uncurry is SML tuple mulit arguments anb curry function 
		    *)
    end
fun seq p q =
    using p (fn v => using q (fn w => succeed (v,w)))
fun many p =
    alt (using p (fn x => using (many p) (fn  xs => succeed (x::xs) )))
	(succeed [])
fun many1 p = 
    using p (fn x => 
		using (many p) (fn xs => succeed (x::xs) ) )

fun xthen p1 p2 = 
    using (seq p1 p2) (fn (a,b) => succeed(b) )
	  (* old (fn (a,b) => b) 
	     using is bind
	   *)
fun thenx p1 p2 =
    using (seq p1 p2) (fn (a,b) => succeed(a) )
val lower = sat (fn x => #"a" <= x andalso x <= #"z")
val upper = sat (fn x => #"A" <= x andalso x <= #"Z")
val digit = sat (fn x => #"0" <= x andalso x <= #"9")
val letter  = alt lower upper
val alphanum = alt letter digit
fun word inp = 
    let val neWord = using letter (fn x =>
				      using word (fn xs => succeed (x::xs) ) )
    in (alt neWord (succeed []) inp)
    end
fun mChar x = sat (fn y => x = y)
fun mString [] = succeed []
  | mString (x::xs) = using (mChar x) (fn _ =>
					  using (mString xs) (fn _ => succeed (x::xs) ) )
(* stirng "" = do result ""
   string (x:xs) = do 
                     char x
                     string xs
                     result (x:xs)
   these is haskell style
 *)
fun item [] = []
  | item (x::xs) = [(x,xs)]
(* sat :: (char -> bool) -> char Parser 
  another version sat using the bind <=> using
  sat p = using item (fn x => if p x then succeed x else fail
  sat p = [x | x <- item , p x] ;; [if p x then x <- item in list]
  sat p = do x <- item 
             if (p x) then return x ;; return <=> result <=> succeed 
  word :: string Parser
  word = [x:xs | x <- lettet,xs <- word] ++ [""]
  haskell String <=> sml char list 
  many :: 'a Parser -> 'a list Parser
  many p = [x:xs | x <- p ,xs <- many] ++ [[]]
  ident :: char list Parser
  ident = [x:xs | x <- lower , xs <- alphanum ]
  many1 :: 'a Parser -> 'a list Parser
  many1 p = [x:xs | x <- p ,xs <- many p]
 *)
val ident = using lower (fn x =>
			    using (many alphanum) (fn xs => succeed (x::xs) ) )
(*
val nat = 
    let 
	fun eval xs = valOf (Int.fromString (String.implode xs))
    in 
	using (many1 digit) 
	      (fn xs => 
		  succeed (eval xs) )
    end
*)
fun sepby1 p sep = 
    let val temp = many (using sep (fn _ => using p  (fn y => succeed y) ) )
    in 
	using p (fn x => 
		    using temp
			  (fn xs => succeed (x::xs) ) )
    end

fun bracket Open p Close = 
    using Open (fn _ => using p (fn x => using Close (fn _ => succeed x)) )
fun sepby p sep = alt (sepby1 p sep) (succeed [])
fun chainl1 p Op =
    let fun rest x =  alt (using Op (fn f => using p (fn y => rest (f x y))))
			  (succeed x)
    in
	using p rest
    end
fun chainr1 p Op =
    using p (fn x => 
		alt
		    (using Op (fn f => using (chainr1 p Op) (fn y => succeed (f x y) )))
		    (succeed x) )
val nat = 
    let 
	fun Op a b = a * 10 + b
	val temp = using digit (fn x => succeed( (Char.ord x) - (Char.ord #"0") ) )
    in 
	chainl1 temp (succeed Op)
    end

val mInt =
    let val Op = alt (using (mChar #"-")
			    (fn _ => succeed op~))
		     (succeed (fn x => x))
    in 
	using Op (fn f =>
		     using nat (fn n => succeed (f n) ) )
    end

val mInts = 
    using (mChar #"[") 
	  (fn _ => using mInt 
		       (fn n => 
			   using (many (using (mChar #",")
					      (fn _ => using mInt
							   (fn x => succeed x) )))
				 (fn xs => using (mChar #"]")
					       (fn _ => succeed (n::xs)) ) ) )

exception EmptyError
fun foldr1 (f:'a -> 'a -> 'a) (x::nil:'a list) : 'a =  x
  | foldr1 (f:'a -> 'a -> 'a) ((x::xs):'a list) : 'a =  f x (foldr1 f xs)
  | foldr1 (f:'a -> 'a -> 'a) ([]:'a list) :'a  = raise EmptyError
fun chainl p Op v = alt (chainl1 p Op) (succeed v)
fun chainr p Op v = alt (chainr1 p Op) (succeed v)
fun ops xs = foldr1 alt (map (fn (p,Op) => using p (fn _ => succeed Op)) xs)
end 
val aaaa = P.mread "aaaa"
val Then = P.seq
val isA = P.literal #"a"
val isB = P.literal #"b"
val moreA = P.many isA
val moreD = P.many P.digit
val words = P.many P.alphanum
open P;
(*
 val addop = alt ( using (mChar #"+") (fn _ => succeed ( fn a => fn b => a + b) )) 
 		( using (mChar #"-") (fn _ => succeed ( fn a => fn b => a - b) )) 
 fun mFold f acc [] = acc
   | mFold f acc (x::xs) = foldl f (f (x,acc)) xs
*)
infix >>= 
(* 左结合 还是 右结合 emmm *)
fun a >>= b = (using a b)
(* 
 val expr : int Parser 		
 val addop : (int -> int -> int) Parser
 val factor : int Parser
 foldr : ('a * 'b -> 'b) -> 'b -> 'a list -> 'b
 foldl : ('a * 'b -> 'b) -> 'b -> 'a list -> 'b
 fun foldr (f:'a*'b->'b) (acc:'b) (l:'a list):'b = 
     case l of
        [] => acc
       | x::xs => f(x, (foldr f acc xs))
 fun foldl 
 fun foldr1 f []  =  []
   | foldr1 f (x::xs) = foldr f x xs
*)
fun unCurry func = fn (a,b) => func a b
fun choice ps = foldr (unCurry alt) (succeed []) ps
(* fun ops xs = foldr1 alt (map (fn (p,Op) => p >>= (fn _ => succeed Op)) xs); *)
val addop = ops [(literal #"+",fn a => fn b => a + b),
		 (literal #"-",fn a => fn b => a - b)]
val expop = ops [(literal #"*",fn a => fn b => a * b)]
fun expr inp   = (chainl1 term addop) inp
and term inp   = (chainr1 factor expop) inp
and factor inp = alt nat (bracket (literal #"(") expr (literal #")")) inp

(* eval :: int Paeser *)
val eval = 
    let
	val add = nat >>= (fn x => (literal #"+") >>= (fn _ => (nat >>= (fn y => succeed (x + y)))))
	val sub = nat >>= (fn x => (literal #"-") >>= (fn _ => (nat >>= (fn y => succeed (x - y)))))
    in
	alt add sub
    end

val eval' = 
    let 
	fun add x = (literal #"+") >>= (fn _ => (nat >>= (fn y => succeed (x + y))))
	fun sub x = (literal #"-") >>= (fn _ => (nat >>= (fn y => succeed (x - y))))
    in 
	nat >>= (fn x => (alt (add x) (sub x)) >>= (fn v => succeed v))
    end
val eval'' = 
    let 
	val add = fn x => fn y => x + y
	val sub = fn x => fn y => x - y
    in 
	nat >>= (fn x => (ops [(literal #"+" ,add),(literal #"-",sub)])
			   >>= (fn f => nat >>= (fn y => succeed (f x y) )))
    end

(* m force : 'a Paeser -> 'a Paeser *)
fun fst (a,b) = a
fun snd (a,b) = b
val head = hd
val tail = tl
(*
 val mforce = fn : 'a Parser -> 'a Parser
 val mMany = fn : 'a Parser -> 'a list Parser
 *)
fun mforce (p:'a Parser): 'a Parser= fn inp =>
		  let val x = p inp
		  in 
		      (fst (head x),snd (head x))::(tail x)
		  end

fun mMany p = 
    mforce ( 
	alt (p >>= (fn x => (mMany p) >>= (fn xs => succeed (x::xs))))
	    (succeed [])
	  )
(* number : int Parser *)
val number:int Parser = alt nat (succeed 0)
fun first (p:'a Parser) : 'a Parser = 
    fn inp => case p inp of
		[] => []
	     | (x::xs) => [x]
			     
(* (+++) : 'a Parser -> 'a Parser -> 'a Parser *)
infix +++ 
fun p +++ q = first (alt p q)
(* sml infix is unCurry function so,
   op+++ : 'a Parser * 'a Parser -> 'a Parser 
 *)
(* val colour : char list Parser *)
val colour = 
    let 
	val p1 = mString (mread "yellow")
	val p2 = mString (mread "orange")
    in 
	p1 +++ p2
    end		
exception EmptyError
fun take i [] = raise EmptyError
  | take i (x::xs) =
    if i = 0 then []
    else x:: (take (i - 1) xs)

fun first' (p:'a Parser) :'a Parser = 
 fn inp =>
    take 1 (p inp)

fun first'' (p:'a Parser) :'a Parser =
    fn inp => case p inp of
		[] => []
	     | (x::xs) => x::take 0 xs

val spaces : unit Parser = (* haskell () <=> sml unit *)
    let fun isSpace x = (x = #" ") orelse (x = #"\n") orelse (x = #"\t")
    in 
	(many1 (sat isSpace)) >>= (fn _ => succeed () )
    end

val comment : unit Parser =
    (mString [#"-",#"-"]) 
	>>= 
	(fn _ =>
	    (many (sat (fn x => x <> #"\n")))
		>>= (fn _ => succeed () )
	)
			   
val junk : unit Parser = 
    (many (spaces +++ comment)) >>= (fn _ => succeed (()) )
fun parse (p:'a Parser) :'a Parser = 
    p >>= (fn v => junk >>= (fn _ => succeed v))
(* remove junk before parser *)
fun token (p:'a Parser) :'a Parser =
    junk >>= (fn _ => p >>= (fn v => succeed v))  
(* remove junk after parser *)
val natural:int Parser = 
    token nat
val integer:int Parser =
    token mInt
fun symbol (xs:char list) : (char list)Parser=
    token (mString xs)
fun elem x [] = false
  | elem x (c::cs) = if c = x 
		     then true
		     else elem x cs
(* val identifier = fn : char list list -> char list Parser *)				
fun identifier (ks:(char list list)) =
    token ( ident >>= (fn x => if elem x ks
			     then fail
			     else succeed x)
	  )
datatype Expr = App of Expr * Expr
              | Lam of (char list) *  Expr
	      | Let of (char list) *  Expr * Expr
	      | Var of (char list)
fun Curry f = fn a => fn b => f (a,b)
val mLet = symbol (mread "let")
val In  = symbol (mread "in")
val Eq  = symbol (mread "=")
val Lm  = symbol (mread "\\")
val To  = symbol (mread "->")
fun expr p = (chainl1 atom (succeed (Curry App))) p
and atom p = (lamp +++ letp +++ var +++ paren) p (* alt( alt (lamp,letp),varp) *)
and lamp p = 
    (Lm       >>= (fn _ =>
     variable >>= (fn x => 
     To       >>= (fn _ =>
     expr     >>= (fn e =>
     succeed (Lam (x,e))  ))))) p
and letp p = 
    (mLet     >>= (fn _ =>
    variable  >>= (fn x =>
    Eq        >>= (fn _ =>
    expr      >>= (fn e =>
    In        >>= (fn _ =>
    expr      >>= (fn b =>
	      succeed (Let (x,e,b)) ))))))) p
and variable p = identifier [mread "let",mread "in"] p
and var p      = (variable >>= (fn x => succeed (Var x) )) p
and paren p    = ( bracket (symbol [#"("]) expr (symbol [#")"]) ) p

(* >>= :: 'a m-> ('a -> 'b m) -> 'b m *)
(* using(bind) : 'a Parser -> ('a -> 'b Parser) -> 'b Parser *)
(*
 前置了解 粗略了解过 lambda calculus
 a list map is about list Monad bind ???
 p1 `bind` \x1 ->
 p2 `bind` \x2 ->
  ... 
 pn `bind` \xn ->
 <=> equiv
  [ f x1 x2 ... xn | x1 <- p1
                   , x2 <- p2
                   , ...
                   , xn <- pn ] 
 上述 是 list monad 的语法糖 和 do 语法糖 相似 ,注意 x1 <- p1 的顺序
 上述等价 同样应用在 haskell 的 list comprehension 语法糖中
 而 对于 list 的 bind 同样等价的解释 (递归定义了?? )
 他就像是函数套用一样，
 只差在他不接受普通值，
 他是接受一个 monadic value（也就是具有 context 的值）
 并且把他喂给一个接受普通值的函数，
 并回传一个 monadic value。
 就是类似 看 scheme 的 monad 语法糖实现
 list map :: (a -> b) -> list a -> list b
 list bind :: list a -> (a -> list b) -> list b
 bind <=> using <=> (>>=)
 bind :: M a -> (a -> M b) M b
 functor fmap <=> map  <=> (<$>)
 fmap :: (a -> b) -> f a -> f b
 pure <=> return <=> result <=> unit <=> datatype constructor
 (<*>) :: Applicative f => f (a -> b) -> f a -> f b

 file:///E:/pj_hs/my-parsec/doc/Monadic-Parser-Combinators.pdf
 了解 bind 
 用 Standard ML 学 Haskell
 用 Haskell     学 Standard ML 
 *)
(*
 monad 的三种描述办法
 join map flatMap (也就是 >>= ) mcompose ( join <=> concat )
 join m = m >>= id -- (用 >>= 定义出 join)
 map f ma = ma >>= (return . f)  -- (用 >>= 定义出 map)
 *)
