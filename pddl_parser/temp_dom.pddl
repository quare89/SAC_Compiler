(define (domain trucks-qualitativepreferences)
(:requirements :adl :typing)
(:types locatable truckarea location time - object
	package - locatable
	truck - locatable)
(:predicates
	(closer ?a1 - truckarea ?a2 - truckarea)
	(delivered ?p - package ?l - location ?t - time)
	(le ?t1 - time ?t2 - time)
	(at-destination ?p - package ?l - location)
	(free ?a - truckarea ?t - truck)
	(next ?t1 - time ?t2 - time)
	(time-now ?t - time)
	(at ?x - locatable ?l - location)
	(in ?p - package ?t - truck ?a - truckarea)
	(connected ?x - location ?y - location))
(:action l
:parameters ( ?a1 - truckarea ?p - package ?t - truck ?l - location)
:precondition (and (at ?t ?l) (at ?p ?l) (free ?a1 ?t) (forall (?a2 - truckarea) (or (not (closer ?a2 ?a1)) (free ?a2 ?t))))
:effect (and (not (at ?p ?l)) (not (free ?a1 ?t)) (in ?p ?t ?a1) )
)
(:action d
:parameters ( ?p - package ?t2 - time ?l - location ?t1 - time)
:precondition (and (at ?p ?l) (time-now ?t1) (le ?t1 ?t2))
:effect (and (not (at ?p ?l)) (delivered ?p ?l ?t2) (at-destination ?p ?l) )
)
(:action dr
:parameters ( ?to - location ?t2 - time ?from - location ?t - truck ?t1 - time)
:precondition (and (at ?t ?from) (connected ?from ?to) (time-now ?t1) (next ?t1 ?t2))
:effect (and (not (at ?t ?from)) (not (time-now ?t1)) (time-now ?t2) (at ?t ?to) )
)
(:action u
:parameters ( ?a1 - truckarea ?p - package ?t - truck ?l - location)
:precondition (and (at ?t ?l) (in ?p ?t ?a1) (forall (?a2 - truckarea) (or (not (closer ?a2 ?a1)) (free ?a2 ?t))))
:effect (and (not (in ?p ?t ?a1)) (free ?a1 ?t) (at ?p ?l) )
)
)
