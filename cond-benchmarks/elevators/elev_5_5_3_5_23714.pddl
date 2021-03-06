(define (problem elev_5_5_3_5_23714)
  (:domain elevators)
  (:objects f2 f3 f4 f5 - floor p2 p3 p4 p5 - pos e1 e2 e3 - elevator c1 c2 c3 c4 c5 - coin)
  (:init (at f1 p1) (dec_f f2 f1) (dec_f f3 f2) (dec_f f4 f3) (dec_f f5 f4) (dec_p p2 p1) (dec_p p3 p2) (dec_p p4 p3) (dec_p p5 p4) (shaft e1 p4) (in e1 f1) (shaft e2 p4) (in e2 f2) (shaft e3 p2) (in e3 f1) (coin-at c1 f2 p5) (coin-at c2 f4 p4) (coin-at c3 f3 p1) (coin-at c4 f5 p1) (coin-at c5 f3 p2) (gate f2 p2) (gate f4 p3) (gate f5 p2) (gate f5 p4) (gate f5 p5))
  (:goal (and (have c1) (have c2) (have c3) (have c4) (have c5)))
)
