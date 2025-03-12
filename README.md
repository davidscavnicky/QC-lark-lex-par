# 12/3/2025: Week 6

## Lecture: 

The PDF of the lecture is here:
http://www.nbi.dk/~avery/QCC/qcc4.pdf

Bjarnes pictures of the blackboard part of the lecture are here:
http://www.nbi.dk/~avery/QCC/blackboards/2025/w6.zip

## Reading:

This week, we are going to implement the synthesis stage: transforming from a general set of quantum gates down to a small machine-dependent subset of elementary gates. I.e., we need to synthesize complex gates in terms of a limited gate set. In the data lab, we're going to transform our PE-generated intermediate code consisting of "machine instruction" gates for two different quantum computers with different physically implemented gate sets.

To read before Wednesday:

     Shende, Bullock and Markov: Synthesis of Quantum Logic Circuits: 
     https://web.eecs.umich.edu/~imarkov/pubs/jour/tcad06-qsd.pdf
 
## Lab instrutions:

This week will implement the synthesis stage of the quantum compiler. Each quantum computer architecture will only implement a small subset of gates with physical operations, and generate the remaining gates from these. In the synthesis stage, we transform the "full" gateset into this limited generator set.

Your output after partial evaluation for the two sample programs should be a list of quantum gate statements, but with nested blocks. Use the provided helper function `flatten_program` from `flatten.py` to transform into a single-block flat list of quantum operations.

Your task: Synthesize the CQ qupdate (unconditional and controlled) to generate code for a quantum architecture Q that implements only the operations {X,SX,CX,RZ,measure}, which we will call "elementary gates".

     1. Write a function that translates each single-qubit gate to a sequence of elementary gates.
     2. Do the same for the 2-qubit controlled gates ("qupdate if qbit")[
     3. Generate quantum circuits code for initialize.cq and qft2.cq with the classical part PE'd away. Use the simulator from simulators.py to check the synthesized code.
     4. Implement the general decomposition of 2x2 unitaries into Rz Ry Rz rotations.
     
The various helper code is on the github repository here: http://github.com/jamesavery/QCC

There is a reference implementation of the CQ partial evaluator provided as `PEjames.py`, in case you didn't get your own to work.

# 5/3/2025: Week 5

## Lecture
Bjarnes pictures of the blackboard part of the lecture are here:
http://www.nbi.dk/~avery/QCC/blackboards/2025/w5.zip

## Topic overview:

Programs as data: Semantics-preserving program transformations.
CQ-: a small intermediate quantum sub-language.
Partial evaluation for quantum-program generation.

This coming week, we're going to build a partial evaluator that transforms a mixed classical-quantum CQ program to a pure quantum program in the CQ- sub-language. Partial evaluation is a semantics preserving program transformation, which we will learn about in today's lecture.

## Reading instructions:

1. Neil Jones: "An Introduction to Partial Evaluation" (First 8 pages)
https://dl.acm.org/doi/pdf/10.1145/243439.243447

2. Uwe Meyer: "Techniques for Partial Evaluation of Imperative
Languages" (Full paper, this is the technique you will use)
http://www.nbi.dk/~avery/QCC/PE-imperative.pdf

## Lab instructions:

This week we're implementing (most of) a partial evaluator for CQ, which we use to evaluate away the classical parts of the programs, so that what remains is a "flat" quantum program in a simpler subset of CQ, which we will call CQ- ("CQ minus") and use as intermediate code. 

The files you need this week are on http://github.com/jamesavery/QCC - start by `git clone`ing it.

In the new file `show.py`, there are functions to print out a CQ AST back into CQ syntax, very useful for debugging.

This week's task:

In PE-skeleton.py, I've provided both the easiest and most difficult parts - what's left for you to implement are declarations and expressions. 

1. Implement partial evaluation of declarations (PE_declaration(d,value_env)), and test on declaration examples.
2. Start on PE_statement(d,value_env) and implement assignments and quantum operations.
   Test on examples.
3. Implement blocks, test on examples.
4. Implement if-conditionals, and while-loops.
   What are considerations for how to partially evaluate conditionals and while-loops?
   Test on examples.

For full-program specialization, you can either use my implementation for program and procedures,
or implement your own (a bit tricky).

5. Once you have debugged the components, you should be able to to partially evaluate
   any CQ-program without function calls; in particular initialize.cq and qft2.cq

Notice that you get some unnecessary blocks, etc., that doesn't to anything in the residual code.
You can get rid of unnecessary nested blocks in the following way:
1. If the block contains no declarations, its statements can be merged directly back
   into the parent block.
2. If the block contains declarations with no name clashes in the parent block,
   i)  the declarations can be appended to the parent block's declarations, and
   ii) the statements can be merged in-place with the parent block's statements.
3. If the block contains declarations that clash with variables in the parent block's scope,
   append a unique suffix to the names and proceed like case 2.
In this way, you obtain a flat program consisting only of a single flat scope,
with variables declared at the top. Only loops that depend on quantum operations remain.

The jupyter file `datalab5.3.ipynb` has helpful examples to test with.


# 26/2/2025: Week 4

## Lecture
Here are the slides from today's lecture, which includes the data lab problem descriptions. Enjoy!

http://www.nbi.dk/~avery/QCC/qcc2.pdf


# 19/2/2025: Week 3
Here are the slides from today's lecture:

http://www.nbi.dk/~avery/QCC/qcc1.pdf
