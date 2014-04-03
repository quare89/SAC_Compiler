(define (problem tpp)
(:domain tpp-propositionalpreferences)
(:objects
	goods1 goods2 goods3 - goods
	truck1 truck2 - truck
	market1 - market
	depot1 - depot
	level0 level1 level2 level3 - level)

(:init
	(next level1 level0)
	(next level2 level1)
	(next level3 level2)
	(ready-to-load goods1 market1 level0)
	(ready-to-load goods1 depot1 level0)
	(ready-to-load goods2 market1 level0)
	(ready-to-load goods2 depot1 level0)
	(ready-to-load goods3 market1 level0)
	(ready-to-load goods3 depot1 level0)
	(stored goods1 level0)
	(stored goods2 level0)
	(stored goods3 level0)
	(loaded goods1 truck1 level0)
	(loaded goods1 truck2 level0)
	(loaded goods2 truck1 level0)
	(loaded goods2 truck2 level0)
	(loaded goods3 truck1 level0)
	(loaded goods3 truck2 level0)
	(connected depot1 market1)
	(connected market1 depot1)
	(on-sale goods1 market1 level1)
	(on-sale goods2 market1 level3)
	(on-sale goods3 market1 level2)
	(at truck1 depot1)
	(at truck2 depot1))

(:goal (and
	(stored goods1 level1)
	(stored goods2 level2)
	(stored goods3 level2)))
(:constraints
(and

(forall (?m - market ?t1 ?t2 - truck)(preference p1A (always (imply (and (at ?t1 ?m) (at ?t2 ?m))(= ?t1 ?t2)))))
(preference c1 (always (or (loaded goods2 truck2 level0) (stored goods2 level0) (at truck2 depot1))))
(preference c2 (always (loaded goods2 truck1 level0)))
(preference c3 (always (or (loaded goods3 truck1 level0) (stored goods3 level0) (at truck1 depot1))))
(preference c4 (always (loaded goods3 truck2 level0)))
)
)
(:metric minimize
(+
(* 1 (is-violated p1A))(* 1 (is-violated c3))
(* 1 (is-violated c2))
(* 1 (is-violated c1))
(* 1 (is-violated c4))
)
)

)
