(define (domain tpp-propositionalpreferences)
(:requirements :adl)
(:types level locatable place - object
	goods - locatable
	truck - locatable
	depot - place
	market - place)
(:predicates
	(on-sale ?g - goods ?m - market ?l - level)
	(ready-to-load ?g - goods ?m - place ?l - level)
	(next ?l1 - level ?l2 - level)
	(stored ?g - goods ?l - level)
	(connected ?p1 - place ?p2 - place)
	(at ?t - truck ?p - place)
	(loaded ?g - goods ?t - truck ?l - level))
(:action load
:parameters ( ?g - goods ?m - market ?l4 - level ?l2 - level ?l3 - level ?l1 - level ?t - truck)
:precondition (and (at ?t ?m) (loaded ?g ?t ?l3) (ready-to-load ?g ?m ?l2) (next ?l2 ?l1) (next ?l4 ?l3))
:effect (and (loaded ?g ?t ?l4) (not (loaded ?g ?t ?l3)) (ready-to-load ?g ?m ?l1) (not (ready-to-load ?g ?m ?l2)) )
)
(:action buy
:parameters ( ?g - goods ?m - market ?l4 - level ?l2 - level ?l3 - level ?l1 - level ?t - truck)
:precondition (and (at ?t ?m) (on-sale ?g ?m ?l2) (ready-to-load ?g ?m ?l3) (next ?l2 ?l1) (next ?l4 ?l3))
:effect (and (on-sale ?g ?m ?l1) (not (on-sale ?g ?m ?l2)) (ready-to-load ?g ?m ?l4) (not (ready-to-load ?g ?m ?l3)) )
)
(:action drive
:parameters ( ?to - place ?from - place ?t - truck)
:precondition (and (at ?t ?from) (connected ?from ?to))
:effect (and (not (at ?t ?from)) (at ?t ?to) )
)
(:action unload
:parameters ( ?d - depot ?g - goods ?l4 - level ?l2 - level ?l3 - level ?l1 - level ?t - truck)
:precondition (and (at ?t ?d) (loaded ?g ?t ?l2) (stored ?g ?l3) (next ?l2 ?l1) (next ?l4 ?l3))
:effect (and (loaded ?g ?t ?l1) (not (loaded ?g ?t ?l2)) (stored ?g ?l4) (not (stored ?g ?l3)) )
)
)
