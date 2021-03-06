(define (problem FR_9_10)
 (:domain first-response)
 (:objects  l1 l2 l3 l4 l5 l6 l7 l8 l9  - location
	    f1 f2 - fire_unit
	    v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 - victim
	    m1 m2 m3 - medical_unit
)
 (:init 
	;;strategic locations
     (hospital l9)
     (hospital l4)
     (hospital l9)
     (hospital l2)
     (hospital l2)
     (water-at l1)
     (water-at l8)
     (water-at l7)
	;;disaster info
     (fire l9)
     (victim-at v1 l5)
     (victim-status v1 hurt)
     (fire l1)
     (victim-at v2 l7)
     (victim-status v2 hurt)
     (fire l8)
     (victim-at v3 l1)
     (victim-status v3 dying)
     (fire l1)
     (victim-at v4 l5)
     (victim-status v4 dying)
     (fire l3)
     (victim-at v5 l6)
     (victim-status v5 dying)
     (fire l5)
     (victim-at v6 l8)
     (victim-status v6 hurt)
     (fire l8)
     (victim-at v7 l3)
     (victim-status v7 dying)
     (fire l5)
     (victim-at v8 l6)
     (victim-status v8 hurt)
     (fire l1)
     (victim-at v9 l5)
     (victim-status v9 dying)
     (fire l5)
     (victim-at v10 l9)
     (victim-status v10 hurt)
	;;map info
	(adjacent l1 l1)
	(adjacent l2 l2)
	(adjacent l3 l3)
	(adjacent l4 l4)
	(adjacent l5 l5)
	(adjacent l6 l6)
	(adjacent l7 l7)
	(adjacent l8 l8)
	(adjacent l9 l9)
   (adjacent l1 l1)
   (adjacent l1 l1)
   (adjacent l2 l1)
   (adjacent l1 l2)
   (adjacent l2 l2)
   (adjacent l2 l2)
   (adjacent l2 l3)
   (adjacent l3 l2)
   (adjacent l2 l4)
   (adjacent l4 l2)
   (adjacent l2 l5)
   (adjacent l5 l2)
   (adjacent l3 l1)
   (adjacent l1 l3)
   (adjacent l3 l2)
   (adjacent l2 l3)
   (adjacent l3 l3)
   (adjacent l3 l3)
   (adjacent l4 l1)
   (adjacent l1 l4)
   (adjacent l4 l2)
   (adjacent l2 l4)
   (adjacent l4 l3)
   (adjacent l3 l4)
   (adjacent l5 l1)
   (adjacent l1 l5)
   (adjacent l7 l1)
   (adjacent l1 l7)
   (adjacent l8 l1)
   (adjacent l1 l8)
   (adjacent l8 l2)
   (adjacent l2 l8)
   (adjacent l8 l3)
   (adjacent l3 l8)
   (adjacent l8 l4)
   (adjacent l4 l8)
   (adjacent l9 l1)
   (adjacent l1 l9)
   (adjacent l9 l2)
   (adjacent l2 l9)
   (adjacent l9 l3)
   (adjacent l3 l9)
   (adjacent l9 l4)
   (adjacent l4 l9)
   (adjacent l9 l5)
   (adjacent l5 l9)
   (adjacent l9 l6)
   (adjacent l6 l9)
   (adjacent l9 l7)
   (adjacent l7 l9)
	(fire-unit-at f1 l5)
	(fire-unit-at f2 l9)
	(medical-unit-at m1 l3)
	(medical-unit-at m2 l5)
	(medical-unit-at m3 l6)
	)
 (:goal (and  (nfire l9) (nfire l1) (nfire l8) (nfire l1) (nfire l3) (nfire l5) (nfire l8) (nfire l5) (nfire l1) (nfire l5)  (victim-status v1 healthy) (victim-status v2 healthy) (victim-status v3 healthy) (victim-status v4 healthy) (victim-status v5 healthy) (victim-status v6 healthy) (victim-status v7 healthy) (victim-status v8 healthy) (victim-status v9 healthy) (victim-status v10 healthy)))
 )
