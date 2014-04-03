(define (problem tpp)
(:domain tpp-propositionalpreferences)
(:objects
	goods1 goods2 goods3 goods4 goods5 goods6 goods7 goods8 goods9 goods10 goods11 goods12 goods13 goods14 - goods
	truck1 truck2 truck3 - truck
	market1 market2 market3 market4 - market
	depot1 depot2 - depot
	level0 level1 level2 level3 level4 level5 level6 - level)

(:init
	(next level1 level0)
	(next level2 level1)
	(next level3 level2)
	(next level4 level3)
	(next level5 level4)
	(next level6 level5)
	(ready-to-load goods1 market1 level0)
	(ready-to-load goods1 market2 level0)
	(ready-to-load goods1 market3 level0)
	(ready-to-load goods1 market4 level0)
	(ready-to-load goods1 depot1 level0)
	(ready-to-load goods1 depot2 level0)
	(ready-to-load goods2 market1 level0)
	(ready-to-load goods2 market2 level0)
	(ready-to-load goods2 market3 level0)
	(ready-to-load goods2 market4 level0)
	(ready-to-load goods2 depot1 level0)
	(ready-to-load goods2 depot2 level0)
	(ready-to-load goods3 market1 level0)
	(ready-to-load goods3 market2 level0)
	(ready-to-load goods3 market3 level0)
	(ready-to-load goods3 market4 level0)
	(ready-to-load goods3 depot1 level0)
	(ready-to-load goods3 depot2 level0)
	(ready-to-load goods4 market1 level0)
	(ready-to-load goods4 market2 level0)
	(ready-to-load goods4 market3 level0)
	(ready-to-load goods4 market4 level0)
	(ready-to-load goods4 depot1 level0)
	(ready-to-load goods4 depot2 level0)
	(ready-to-load goods5 market1 level0)
	(ready-to-load goods5 market2 level0)
	(ready-to-load goods5 market3 level0)
	(ready-to-load goods5 market4 level0)
	(ready-to-load goods5 depot1 level0)
	(ready-to-load goods5 depot2 level0)
	(ready-to-load goods6 market1 level0)
	(ready-to-load goods6 market2 level0)
	(ready-to-load goods6 market3 level0)
	(ready-to-load goods6 market4 level0)
	(ready-to-load goods6 depot1 level0)
	(ready-to-load goods6 depot2 level0)
	(ready-to-load goods7 market1 level0)
	(ready-to-load goods7 market2 level0)
	(ready-to-load goods7 market3 level0)
	(ready-to-load goods7 market4 level0)
	(ready-to-load goods7 depot1 level0)
	(ready-to-load goods7 depot2 level0)
	(ready-to-load goods8 market1 level0)
	(ready-to-load goods8 market2 level0)
	(ready-to-load goods8 market3 level0)
	(ready-to-load goods8 market4 level0)
	(ready-to-load goods8 depot1 level0)
	(ready-to-load goods8 depot2 level0)
	(ready-to-load goods9 market1 level0)
	(ready-to-load goods9 market2 level0)
	(ready-to-load goods9 market3 level0)
	(ready-to-load goods9 market4 level0)
	(ready-to-load goods9 depot1 level0)
	(ready-to-load goods9 depot2 level0)
	(ready-to-load goods10 market1 level0)
	(ready-to-load goods10 market2 level0)
	(ready-to-load goods10 market3 level0)
	(ready-to-load goods10 market4 level0)
	(ready-to-load goods10 depot1 level0)
	(ready-to-load goods10 depot2 level0)
	(ready-to-load goods11 market1 level0)
	(ready-to-load goods11 market2 level0)
	(ready-to-load goods11 market3 level0)
	(ready-to-load goods11 market4 level0)
	(ready-to-load goods11 depot1 level0)
	(ready-to-load goods11 depot2 level0)
	(ready-to-load goods12 market1 level0)
	(ready-to-load goods12 market2 level0)
	(ready-to-load goods12 market3 level0)
	(ready-to-load goods12 market4 level0)
	(ready-to-load goods12 depot1 level0)
	(ready-to-load goods12 depot2 level0)
	(ready-to-load goods13 market1 level0)
	(ready-to-load goods13 market2 level0)
	(ready-to-load goods13 market3 level0)
	(ready-to-load goods13 market4 level0)
	(ready-to-load goods13 depot1 level0)
	(ready-to-load goods13 depot2 level0)
	(ready-to-load goods14 market1 level0)
	(ready-to-load goods14 market2 level0)
	(ready-to-load goods14 market3 level0)
	(ready-to-load goods14 market4 level0)
	(ready-to-load goods14 depot1 level0)
	(ready-to-load goods14 depot2 level0)
	(stored goods1 level0)
	(stored goods2 level0)
	(stored goods3 level0)
	(stored goods4 level0)
	(stored goods5 level0)
	(stored goods6 level0)
	(stored goods7 level0)
	(stored goods8 level0)
	(stored goods9 level0)
	(stored goods10 level0)
	(stored goods11 level0)
	(stored goods12 level0)
	(stored goods13 level0)
	(stored goods14 level0)
	(loaded goods1 truck1 level0)
	(loaded goods1 truck2 level0)
	(loaded goods1 truck3 level0)
	(loaded goods2 truck1 level0)
	(loaded goods2 truck2 level0)
	(loaded goods2 truck3 level0)
	(loaded goods3 truck1 level0)
	(loaded goods3 truck2 level0)
	(loaded goods3 truck3 level0)
	(loaded goods4 truck1 level0)
	(loaded goods4 truck2 level0)
	(loaded goods4 truck3 level0)
	(loaded goods5 truck1 level0)
	(loaded goods5 truck2 level0)
	(loaded goods5 truck3 level0)
	(loaded goods6 truck1 level0)
	(loaded goods6 truck2 level0)
	(loaded goods6 truck3 level0)
	(loaded goods7 truck1 level0)
	(loaded goods7 truck2 level0)
	(loaded goods7 truck3 level0)
	(loaded goods8 truck1 level0)
	(loaded goods8 truck2 level0)
	(loaded goods8 truck3 level0)
	(loaded goods9 truck1 level0)
	(loaded goods9 truck2 level0)
	(loaded goods9 truck3 level0)
	(loaded goods10 truck1 level0)
	(loaded goods10 truck2 level0)
	(loaded goods10 truck3 level0)
	(loaded goods11 truck1 level0)
	(loaded goods11 truck2 level0)
	(loaded goods11 truck3 level0)
	(loaded goods12 truck1 level0)
	(loaded goods12 truck2 level0)
	(loaded goods12 truck3 level0)
	(loaded goods13 truck1 level0)
	(loaded goods13 truck2 level0)
	(loaded goods13 truck3 level0)
	(loaded goods14 truck1 level0)
	(loaded goods14 truck2 level0)
	(loaded goods14 truck3 level0)
	(connected market1 market2)
	(connected market1 market3)
	(connected market1 market4)
	(connected market2 market1)
	(connected market2 market3)
	(connected market2 market4)
	(connected market3 market1)
	(connected market3 market2)
	(connected market3 market4)
	(connected market4 market1)
	(connected market4 market2)
	(connected market4 market3)
	(connected depot1 market1)
	(connected market1 depot1)
	(connected depot1 market2)
	(connected market2 depot1)
	(connected depot1 market3)
	(connected market3 depot1)
	(connected depot1 market4)
	(connected market4 depot1)
	(connected depot2 market1)
	(connected market1 depot2)
	(connected depot2 market2)
	(connected market2 depot2)
	(connected depot2 market3)
	(connected market3 depot2)
	(connected depot2 market4)
	(connected market4 depot2)
	(on-sale goods1 market1 level0)
	(on-sale goods2 market1 level1)
	(on-sale goods3 market1 level3)
	(on-sale goods4 market1 level2)
	(on-sale goods5 market1 level1)
	(on-sale goods6 market1 level2)
	(on-sale goods7 market1 level1)
	(on-sale goods8 market1 level0)
	(on-sale goods9 market1 level1)
	(on-sale goods10 market1 level0)
	(on-sale goods11 market1 level3)
	(on-sale goods12 market1 level0)
	(on-sale goods13 market1 level3)
	(on-sale goods14 market1 level0)
	(on-sale goods1 market2 level0)
	(on-sale goods2 market2 level0)
	(on-sale goods3 market2 level2)
	(on-sale goods4 market2 level0)
	(on-sale goods5 market2 level0)
	(on-sale goods6 market2 level0)
	(on-sale goods7 market2 level0)
	(on-sale goods8 market2 level1)
	(on-sale goods9 market2 level1)
	(on-sale goods10 market2 level2)
	(on-sale goods11 market2 level0)
	(on-sale goods12 market2 level3)
	(on-sale goods13 market2 level0)
	(on-sale goods14 market2 level0)
	(on-sale goods1 market3 level1)
	(on-sale goods2 market3 level1)
	(on-sale goods3 market3 level1)
	(on-sale goods4 market3 level2)
	(on-sale goods5 market3 level2)
	(on-sale goods6 market3 level3)
	(on-sale goods7 market3 level2)
	(on-sale goods8 market3 level1)
	(on-sale goods9 market3 level3)
	(on-sale goods10 market3 level1)
	(on-sale goods11 market3 level2)
	(on-sale goods12 market3 level3)
	(on-sale goods13 market3 level2)
	(on-sale goods14 market3 level2)
	(on-sale goods1 market4 level0)
	(on-sale goods2 market4 level1)
	(on-sale goods3 market4 level0)
	(on-sale goods4 market4 level0)
	(on-sale goods5 market4 level0)
	(on-sale goods6 market4 level0)
	(on-sale goods7 market4 level0)
	(on-sale goods8 market4 level0)
	(on-sale goods9 market4 level1)
	(on-sale goods10 market4 level0)
	(on-sale goods11 market4 level1)
	(on-sale goods12 market4 level0)
	(on-sale goods13 market4 level1)
	(on-sale goods14 market4 level1)
	(at truck1 depot1)
	(at truck2 depot2)
	(at truck3 depot1))
(:goal (and
	(stored goods1 level1)
	(stored goods2 level1)
	(stored goods3 level1)
	(stored goods4 level2)
	(stored goods5 level2)
	(stored goods6 level5)
	(stored goods7 level1)
	(stored goods8 level1)
	(stored goods9 level3)
	(stored goods10 level3)
	(stored goods11 level1)
	(stored goods12 level1)
	(stored goods13 level1)
	(stored goods14 level3)))
(:constraints
(and

(forall (?m - market ?t1 ?t2 - truck)(preference p1A (always (imply (and (at ?t1 ?m) (at ?t2 ?m))(= ?t1 ?t2)))))
(preference c1 (always (or (loaded goods4 truck2 level0) (stored goods4 level0) (at truck2 depot1) (at truck2 depot2))))
(preference c2 (always (loaded goods4 truck1 level0)))
(preference c3 (always (loaded goods4 truck3 level0)))
(preference c4 (always (or (loaded goods5 truck1 level0) (stored goods5 level0) (at truck1 depot1) (at truck1 depot2))))
(preference c5 (always (loaded goods5 truck2 level0)))
(preference c6 (always (loaded goods5 truck3 level0)))
(preference c7 (always (or (loaded goods6 truck3 level0) (stored goods6 level0) (at truck3 depot1) (at truck3 depot2))))
(preference c8 (always (loaded goods6 truck1 level0)))
(preference c9 (always (loaded goods6 truck2 level0)))
(preference c10 (always (or (loaded goods9 truck3 level0) (stored goods9 level0) (at truck3 depot1) (at truck3 depot2))))
(preference c11 (always (loaded goods9 truck2 level0)))
(preference c12 (always (loaded goods9 truck1 level0)))
(preference c13 (always (or (loaded goods10 truck3 level0) (stored goods10 level0) (at truck3 depot1) (at truck3 depot2))))
(preference c14 (always (loaded goods10 truck1 level0)))
(preference c15 (always (loaded goods10 truck2 level0)))
(preference c16 (always (or (loaded goods14 truck2 level0) (stored goods14 level0) (at truck2 depot1) (at truck2 depot2))))
(preference c17 (always (loaded goods14 truck3 level0)))
(preference c18 (always (loaded goods14 truck1 level0)))
)
)
(:metric minimize
(+
(* 1 (is-violated p1A))(* 1 (is-violated c15))
(* 1 (is-violated c10))
(* 1 (is-violated c17))
(* 1 (is-violated c11))
(* 1 (is-violated c4))
(* 1 (is-violated c6))
(* 1 (is-violated c8))
(* 1 (is-violated c7))
(* 1 (is-violated c14))
(* 1 (is-violated c9))
(* 1 (is-violated c13))
(* 1 (is-violated c18))
(* 1 (is-violated c2))
(* 1 (is-violated c1))
(* 1 (is-violated c16))
(* 1 (is-violated c3))
(* 1 (is-violated c5))
(* 1 (is-violated c12))
)
)
)
