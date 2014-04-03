(define (problem truck-12)
(:domain trucks-qualitativepreferences)
(:objects
	truck1 - truck
	package1 - package
	package2 - package
	package3 - package
	package4 - package
	package5 - package
	package6 - package
	package7 - package
	package8 - package
	package9 - package
	package10 - package
	package11 - package
	package12 - package
	package13 - package
	package14 - package
	l1 - location
	l2 - location
	l3 - location
	l4 - location
	t0 - time
	t1 - time
	t2 - time
	t3 - time
	t4 - time
	t5 - time
	t6 - time
	t7 - time
	t8 - time
	t9 - time
	t10 - time
	t11 - time
	t12 - time
	t13 - time
	t14 - time
	t15 - time
	t16 - time
	t17 - time
	t18 - time
	t19 - time
	t20 - time
	t21 - time
	t22 - time
	t23 - time
	t24 - time
	t25 - time
	t26 - time
	t27 - time
	t28 - time
	a1 - truckarea
	a2 - truckarea
	a3 - truckarea)

(:init
	(at truck1 l1)
	(free a1 truck1)
	(free a2 truck1)
	(free a3 truck1)
	(closer a1 a2)
	(closer a1 a3)
	(closer a2 a3)
	(at package1 l2)
	(at package2 l2)
	(at package3 l2)
	(at package4 l1)
	(at package5 l1)
	(at package6 l1)
	(at package7 l4)
	(at package8 l4)
	(at package9 l4)
	(at package10 l1)
	(at package11 l1)
	(at package12 l1)
	(at package13 l2)
	(at package14 l2)
	(connected l1 l2)
	(connected l1 l3)
	(connected l1 l4)
	(connected l2 l1)
	(connected l2 l3)
	(connected l2 l4)
	(connected l3 l1)
	(connected l3 l2)
	(connected l3 l4)
	(connected l4 l1)
	(connected l4 l2)
	(connected l4 l3)
	(time-now t0)
	(le t1 t1)
	(le t1 t2)
	(le t1 t3)
	(le t1 t4)
	(le t1 t5)
	(le t1 t6)
	(le t1 t7)
	(le t1 t8)
	(le t1 t9)
	(le t1 t10)
	(le t1 t11)
	(le t1 t12)
	(le t1 t13)
	(le t1 t14)
	(le t1 t15)
	(le t1 t16)
	(le t1 t17)
	(le t1 t18)
	(le t1 t19)
	(le t1 t20)
	(le t1 t21)
	(le t1 t22)
	(le t1 t23)
	(le t1 t24)
	(le t1 t25)
	(le t1 t26)
	(le t1 t27)
	(le t1 t28)
	(le t2 t2)
	(le t2 t3)
	(le t2 t4)
	(le t2 t5)
	(le t2 t6)
	(le t2 t7)
	(le t2 t8)
	(le t2 t9)
	(le t2 t10)
	(le t2 t11)
	(le t2 t12)
	(le t2 t13)
	(le t2 t14)
	(le t2 t15)
	(le t2 t16)
	(le t2 t17)
	(le t2 t18)
	(le t2 t19)
	(le t2 t20)
	(le t2 t21)
	(le t2 t22)
	(le t2 t23)
	(le t2 t24)
	(le t2 t25)
	(le t2 t26)
	(le t2 t27)
	(le t2 t28)
	(le t3 t3)
	(le t3 t4)
	(le t3 t5)
	(le t3 t6)
	(le t3 t7)
	(le t3 t8)
	(le t3 t9)
	(le t3 t10)
	(le t3 t11)
	(le t3 t12)
	(le t3 t13)
	(le t3 t14)
	(le t3 t15)
	(le t3 t16)
	(le t3 t17)
	(le t3 t18)
	(le t3 t19)
	(le t3 t20)
	(le t3 t21)
	(le t3 t22)
	(le t3 t23)
	(le t3 t24)
	(le t3 t25)
	(le t3 t26)
	(le t3 t27)
	(le t3 t28)
	(le t4 t4)
	(le t4 t5)
	(le t4 t6)
	(le t4 t7)
	(le t4 t8)
	(le t4 t9)
	(le t4 t10)
	(le t4 t11)
	(le t4 t12)
	(le t4 t13)
	(le t4 t14)
	(le t4 t15)
	(le t4 t16)
	(le t4 t17)
	(le t4 t18)
	(le t4 t19)
	(le t4 t20)
	(le t4 t21)
	(le t4 t22)
	(le t4 t23)
	(le t4 t24)
	(le t4 t25)
	(le t4 t26)
	(le t4 t27)
	(le t4 t28)
	(le t5 t5)
	(le t5 t6)
	(le t5 t7)
	(le t5 t8)
	(le t5 t9)
	(le t5 t10)
	(le t5 t11)
	(le t5 t12)
	(le t5 t13)
	(le t5 t14)
	(le t5 t15)
	(le t5 t16)
	(le t5 t17)
	(le t5 t18)
	(le t5 t19)
	(le t5 t20)
	(le t5 t21)
	(le t5 t22)
	(le t5 t23)
	(le t5 t24)
	(le t5 t25)
	(le t5 t26)
	(le t5 t27)
	(le t5 t28)
	(le t6 t6)
	(le t6 t7)
	(le t6 t8)
	(le t6 t9)
	(le t6 t10)
	(le t6 t11)
	(le t6 t12)
	(le t6 t13)
	(le t6 t14)
	(le t6 t15)
	(le t6 t16)
	(le t6 t17)
	(le t6 t18)
	(le t6 t19)
	(le t6 t20)
	(le t6 t21)
	(le t6 t22)
	(le t6 t23)
	(le t6 t24)
	(le t6 t25)
	(le t6 t26)
	(le t6 t27)
	(le t6 t28)
	(le t7 t7)
	(le t7 t8)
	(le t7 t9)
	(le t7 t10)
	(le t7 t11)
	(le t7 t12)
	(le t7 t13)
	(le t7 t14)
	(le t7 t15)
	(le t7 t16)
	(le t7 t17)
	(le t7 t18)
	(le t7 t19)
	(le t7 t20)
	(le t7 t21)
	(le t7 t22)
	(le t7 t23)
	(le t7 t24)
	(le t7 t25)
	(le t7 t26)
	(le t7 t27)
	(le t7 t28)
	(le t8 t8)
	(le t8 t9)
	(le t8 t10)
	(le t8 t11)
	(le t8 t12)
	(le t8 t13)
	(le t8 t14)
	(le t8 t15)
	(le t8 t16)
	(le t8 t17)
	(le t8 t18)
	(le t8 t19)
	(le t8 t20)
	(le t8 t21)
	(le t8 t22)
	(le t8 t23)
	(le t8 t24)
	(le t8 t25)
	(le t8 t26)
	(le t8 t27)
	(le t8 t28)
	(le t9 t9)
	(le t9 t10)
	(le t9 t11)
	(le t9 t12)
	(le t9 t13)
	(le t9 t14)
	(le t9 t15)
	(le t9 t16)
	(le t9 t17)
	(le t9 t18)
	(le t9 t19)
	(le t9 t20)
	(le t9 t21)
	(le t9 t22)
	(le t9 t23)
	(le t9 t24)
	(le t9 t25)
	(le t9 t26)
	(le t9 t27)
	(le t9 t28)
	(le t10 t10)
	(le t10 t11)
	(le t10 t12)
	(le t10 t13)
	(le t10 t14)
	(le t10 t15)
	(le t10 t16)
	(le t10 t17)
	(le t10 t18)
	(le t10 t19)
	(le t10 t20)
	(le t10 t21)
	(le t10 t22)
	(le t10 t23)
	(le t10 t24)
	(le t10 t25)
	(le t10 t26)
	(le t10 t27)
	(le t10 t28)
	(le t11 t11)
	(le t11 t12)
	(le t11 t13)
	(le t11 t14)
	(le t11 t15)
	(le t11 t16)
	(le t11 t17)
	(le t11 t18)
	(le t11 t19)
	(le t11 t20)
	(le t11 t21)
	(le t11 t22)
	(le t11 t23)
	(le t11 t24)
	(le t11 t25)
	(le t11 t26)
	(le t11 t27)
	(le t11 t28)
	(le t12 t12)
	(le t12 t13)
	(le t12 t14)
	(le t12 t15)
	(le t12 t16)
	(le t12 t17)
	(le t12 t18)
	(le t12 t19)
	(le t12 t20)
	(le t12 t21)
	(le t12 t22)
	(le t12 t23)
	(le t12 t24)
	(le t12 t25)
	(le t12 t26)
	(le t12 t27)
	(le t12 t28)
	(le t13 t13)
	(le t13 t14)
	(le t13 t15)
	(le t13 t16)
	(le t13 t17)
	(le t13 t18)
	(le t13 t19)
	(le t13 t20)
	(le t13 t21)
	(le t13 t22)
	(le t13 t23)
	(le t13 t24)
	(le t13 t25)
	(le t13 t26)
	(le t13 t27)
	(le t13 t28)
	(le t14 t14)
	(le t14 t15)
	(le t14 t16)
	(le t14 t17)
	(le t14 t18)
	(le t14 t19)
	(le t14 t20)
	(le t14 t21)
	(le t14 t22)
	(le t14 t23)
	(le t14 t24)
	(le t14 t25)
	(le t14 t26)
	(le t14 t27)
	(le t14 t28)
	(le t15 t15)
	(le t15 t16)
	(le t15 t17)
	(le t15 t18)
	(le t15 t19)
	(le t15 t20)
	(le t15 t21)
	(le t15 t22)
	(le t15 t23)
	(le t15 t24)
	(le t15 t25)
	(le t15 t26)
	(le t15 t27)
	(le t15 t28)
	(le t16 t16)
	(le t16 t17)
	(le t16 t18)
	(le t16 t19)
	(le t16 t20)
	(le t16 t21)
	(le t16 t22)
	(le t16 t23)
	(le t16 t24)
	(le t16 t25)
	(le t16 t26)
	(le t16 t27)
	(le t16 t28)
	(le t17 t17)
	(le t17 t18)
	(le t17 t19)
	(le t17 t20)
	(le t17 t21)
	(le t17 t22)
	(le t17 t23)
	(le t17 t24)
	(le t17 t25)
	(le t17 t26)
	(le t17 t27)
	(le t17 t28)
	(le t18 t18)
	(le t18 t19)
	(le t18 t20)
	(le t18 t21)
	(le t18 t22)
	(le t18 t23)
	(le t18 t24)
	(le t18 t25)
	(le t18 t26)
	(le t18 t27)
	(le t18 t28)
	(le t19 t19)
	(le t19 t20)
	(le t19 t21)
	(le t19 t22)
	(le t19 t23)
	(le t19 t24)
	(le t19 t25)
	(le t19 t26)
	(le t19 t27)
	(le t19 t28)
	(le t20 t20)
	(le t20 t21)
	(le t20 t22)
	(le t20 t23)
	(le t20 t24)
	(le t20 t25)
	(le t20 t26)
	(le t20 t27)
	(le t20 t28)
	(le t21 t21)
	(le t21 t22)
	(le t21 t23)
	(le t21 t24)
	(le t21 t25)
	(le t21 t26)
	(le t21 t27)
	(le t21 t28)
	(le t22 t22)
	(le t22 t23)
	(le t22 t24)
	(le t22 t25)
	(le t22 t26)
	(le t22 t27)
	(le t22 t28)
	(le t23 t23)
	(le t23 t24)
	(le t23 t25)
	(le t23 t26)
	(le t23 t27)
	(le t23 t28)
	(le t24 t24)
	(le t24 t25)
	(le t24 t26)
	(le t24 t27)
	(le t24 t28)
	(le t25 t25)
	(le t25 t26)
	(le t25 t27)
	(le t25 t28)
	(le t26 t26)
	(le t26 t27)
	(le t26 t28)
	(le t27 t27)
	(le t27 t28)
	(le t28 t28)
	(next t0 t1)
	(next t1 t2)
	(next t2 t3)
	(next t3 t4)
	(next t4 t5)
	(next t5 t6)
	(next t6 t7)
	(next t7 t8)
	(next t8 t9)
	(next t9 t10)
	(next t10 t11)
	(next t11 t12)
	(next t12 t13)
	(next t13 t14)
	(next t14 t15)
	(next t15 t16)
	(next t16 t17)
	(next t17 t18)
	(next t18 t19)
	(next t19 t20)
	(next t20 t21)
	(next t21 t22)
	(next t22 t23)
	(next t23 t24)
	(next t24 t25)
	(next t25 t26)
	(next t26 t27)
	(next t27 t28))

(:goal (and
 
	(at-destination package1 l1)
	(at-destination package2 l1)
	(at-destination package3 l3)
	(at-destination package4 l2)
	(at-destination package5 l2)
	(at-destination package6 l3)
	(at-destination package7 l3)
	(at-destination package8 l3)
	(at-destination package9 l2)
	(at-destination package10 l3)
	(at-destination package11 l3)
	(at-destination package12 l3)
	(at-destination package13 l3)
	(at-destination package14 l1))

)

(:constraints
(and

(forall (?p - package ?t - truck)
	   (preference p1A (always (forall (?a - truckarea) (imply (in ?p ?t ?a) (closer ?a a2))))))
(forall (?p - package ?t - truck)
	   (preference p1B (always (forall (?a - truckarea) (imply (in ?p ?t ?a) (closer ?a a3))))))
(forall (?p - package ?t - truck)
	   (preference p1C (always (forall (?a - truckarea) (imply (in ?p ?t ?a) (closer ?a a1))))))(preference c1 (always (or (time-now t10) (time-now t5) (time-now t7) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (time-now t0) (time-now t11) (time-now t1) (at-destination package3 l3) (time-now t13))))
(preference c2 (always (or (time-now t10) (time-now t5) (time-now t7) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (time-now t0) (at-destination package2 l1) (time-now t11) (time-now t1) (time-now t13))))
(preference c3 (always (or (time-now t10) (time-now t5) (time-now t7) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (time-now t0) (time-now t11) (time-now t1) (time-now t13) (at-destination package6 l3))))
(preference c4 (always (or (time-now t10) (time-now t5) (time-now t7) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (at-destination package12 l3) (time-now t0) (time-now t11) (time-now t1) (time-now t13))))
(preference c5 (always (or (time-now t10) (time-now t5) (time-now t7) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (time-now t0) (time-now t11) (time-now t1) (time-now t13) (at-destination package13 l3))))
(preference c6 (always (or (time-now t10) (time-now t5) (time-now t7) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (time-now t0) (time-now t11) (time-now t1) (time-now t13) (at-destination package14 l1))))
(preference c7 (always (or (time-now t10) (time-now t5) (time-now t7) (at-destination package5 l2) (time-now t6) (time-now t3) (time-now t8) (time-now t2) (time-now t4) (time-now t9) (time-now t12) (time-now t0) (time-now t11) (time-now t1) (time-now t13))))
)
)
(:metric minimize
(+
(* 1 (is-violated p1A))(* 1 (is-violated p1B))(* 1 (is-violated p1C))(* 1 (is-violated c4))
(* 1 (is-violated c6))
(* 1 (is-violated c7))
(* 1 (is-violated c2))
(* 1 (is-violated c1))
(* 1 (is-violated c3))
(* 1 (is-violated c5))
)
)

)
