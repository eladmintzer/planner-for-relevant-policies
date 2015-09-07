(define (problem rect-20-20-5-5-11)
  (:domain rectangle-world)
  (:objects n0 n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 n13 n14 n15 n16 n17 n18 n19 - int)
  (:init (xpos n0)
	 (ypos n0)
         (next n0 n1)
         (next n1 n2)
         (next n2 n3)
         (next n3 n4)
         (next n4 n5)
         (next n5 n6)
         (next n6 n7)
         (next n7 n8)
         (next n8 n9)
         (next n9 n10)
         (next n10 n11)
         (next n11 n12)
         (next n12 n13)
         (next n13 n14)
         (next n14 n15)
         (next n15 n16)
         (next n16 n17)
         (next n17 n18)
         (next n18 n19)
	 (safeX n3)
	 (safeX n5)
	 (safeX n14)
	 (safeX n17)
	 (safeY n1)
	 (safeY n3)
	 (safeY n9)
	 (safeY n15)
	 (unsafe n0 n5)
	 (unsafe n0 n13)
	 (unsafe n0 n16)
	 (unsafe n1 n4)
	 (unsafe n1 n9)
	 (unsafe n1 n10)
	 (unsafe n2 n10)
	 (unsafe n2 n14)
	 (unsafe n3 n2)
	 (unsafe n3 n3)
	 (unsafe n3 n4)
	 (unsafe n3 n8)
	 (unsafe n3 n18)
	 (unsafe n4 n5)
	 (unsafe n4 n6)
	 (unsafe n4 n12)
	 (unsafe n4 n15)
	 (unsafe n4 n19)
	 (unsafe n5 n1)
	 (unsafe n5 n9)
	 (unsafe n5 n11)
	 (unsafe n6 n6)
	 (unsafe n6 n8)
	 (unsafe n6 n12)
	 (unsafe n7 n10)
	 (unsafe n7 n12)
	 (unsafe n7 n18)
	 (unsafe n8 n5)
	 (unsafe n8 n6)
	 (unsafe n8 n11)
	 (unsafe n8 n17)
	 (unsafe n10 n1)
	 (unsafe n11 n5)
	 (unsafe n11 n8)
	 (unsafe n11 n9)
	 (unsafe n11 n13)
	 (unsafe n11 n15)
	 (unsafe n12 n4)
	 (unsafe n12 n5)
	 (unsafe n12 n8)
	 (unsafe n12 n10)
	 (unsafe n12 n15)
	 (unsafe n12 n18)
	 (unsafe n12 n19)
	 (unsafe n13 n1)
	 (unsafe n13 n3)
	 (unsafe n13 n5)
	 (unsafe n13 n14)
	 (unsafe n14 n4)
	 (unsafe n15 n5)
	 (unsafe n15 n7)
	 (unsafe n15 n13)
	 (unsafe n15 n15)
	 (unsafe n15 n17)
	 (unsafe n16 n0)
	 (unsafe n16 n6)
	 (unsafe n16 n10)
	 (unsafe n16 n18)
	 (unsafe n17 n1)
	 (unsafe n17 n2)
	 (unsafe n17 n3)
	 (unsafe n17 n5)
	 (unsafe n17 n7)
	 (unsafe n17 n8)
	 (unsafe n17 n9)
	 (unsafe n18 n2)
	 (unsafe n18 n5)
	 (unsafe n18 n10)
	 (unsafe n18 n14)
	 (unsafe n19 n2)
	 (unsafe n19 n3)
	 (unsafe n19 n10)
  )
  (:goal (and (xpos n19) (ypos n19)))
  (:goal-reward 1000)
  (:metric maximize (reward))
)
