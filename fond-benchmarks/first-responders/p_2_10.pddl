(define (problem FR_2_10)
 (:domain first-response)
 (:objects  l1 l2  - location
	    f1 f2 - fire_unit
	    v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 - victim
	    m1 m2 - medical_unit
)
 (:init 
	;;strategic locations
     (hospital l1)
     (hospital l1)
     (water-at l2)
     (water-at l1)
	;;disaster info
     (fire l1)
     (victim-at v1 l2)
     (victim-status v1 dying)
     (fire l1)
     (victim-at v2 l1)
     (victim-status v2 hurt)
     (fire l2)
     (victim-at v3 l1)
     (victim-status v3 hurt)
     (fire l2)
     (victim-at v4 l1)
     (victim-status v4 dying)
     (fire l1)
     (victim-at v5 l2)
     (victim-status v5 dying)
     (fire l1)
     (victim-at v6 l2)
     (victim-status v6 hurt)
     (fire l2)
     (victim-at v7 l1)
     (victim-status v7 hurt)
     (fire l2)
     (victim-at v8 l1)
     (victim-status v8 dying)
     (fire l2)
     (victim-at v9 l2)
     (victim-status v9 dying)
     (fire l1)
     (victim-at v10 l2)
     (victim-status v10 hurt)
	;;map info
	(adjacent l1 l1)
	(adjacent l2 l2)
	(fire-unit-at f1 l1)
	(fire-unit-at f2 l2)
	(medical-unit-at m1 l2)
	(medical-unit-at m2 l1)
	)
 (:goal (and  (nfire l1) (nfire l1) (nfire l2) (nfire l2) (nfire l1) (nfire l1) (nfire l2) (nfire l2) (nfire l2) (nfire l1)  (victim-status v1 healthy) (victim-status v2 healthy) (victim-status v3 healthy) (victim-status v4 healthy) (victim-status v5 healthy) (victim-status v6 healthy) (victim-status v7 healthy) (victim-status v8 healthy) (victim-status v9 healthy) (victim-status v10 healthy)))
 )
