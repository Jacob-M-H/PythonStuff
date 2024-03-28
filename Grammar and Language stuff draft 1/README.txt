Hey,

It's been awhile since I last pushed, I've been trying to keep my github tidy, and I haven't much experience in that.
	You'll have to bear with semi completed projects and code heaps until I start bringing a close to these.


Motivation: Many of the projects started in college and after have required parsing complex strings. Many of the projects have also been abandoned at that stage due to the number of cases to match for.
		Eventually my research on grammar and language led me to the single most useful Proper Noun I needed, an LL(K) Parser. 
		An LL(K) parser uses regular expressions and pattern matching to define certain rules, which can then be created as objects. In this way complex rulesets can be handled with a relatively simple UX.
		Examples of such parsers being used is LaTeX, Mathematica, Python, and other interpreted languages.
		There is some theory involved, but this project's main goal is to take some relatively non standardized grammar, and create a AST of the input string(s). 
		Additional goals is expanding a grammar by comparing AST's of rule sets, source implementation of Atomics, and outputting properly formatted languages. 
		It is important to note that the grammar itself will not have any 'power', but the tool should combine languages and reformat language files to be inline with theory. 
		An additional tool to be developed creates forward declarations of each rule object with it's expected arguments to further help draw work away from parsing and pattern matching, and more towards UI/UX and the Algorithmic power of the langauge/implementation itself.


Comments/Notes: 
	The algorithms used may be improved, however a deepdive on multi threading, and the types of returns available in the implemented language would be important to re-evaluate. For example C++ has pointers and references, while python has pass by assignment, and java is usually passed by value.
	The algorithms base assumptions to stay in line with theory dictates longer cases should appear earlier in the pattern matching. However, so long as it's sorted by similar strings and then by length, it doesn't really matter.
	Memoization and the above sorting priority brings the alg. time in line with On [apparently] when parsing.
	Regular expression(s) will be implemented, as I realized part of what I was trying to do was implement a form of regular expressions. I will try to match the ptyhon Re library's assumptions, so that there is an example to follow. 

	This draft will now start focusing on some organizational improvements, rewording/cleaning comments on the algorithms, and re-establishing what the metadata/grammar files should look like to make the language objects able to comapre faster.
	Eventually merging langauges will likely look like an NP hard problem, so there is some heavy lifting to be done to reduce the likelyhood that it attempts to deeply merge when there are clear differences, or grammar that makes other pattern matching inaccessible.