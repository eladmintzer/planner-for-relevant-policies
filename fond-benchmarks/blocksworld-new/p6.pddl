(define (problem bw_6_6)
  (:domain blocks-domain)
  (:objects b1 b2 b3 b4 b5 b6 - block)
  (:init (emptyhand) (on b1 b2) (on-table b2) (on b3 b4) (on b4 b6) (on b5 b1) (on-table b6) (clear b3) (clear b5))
  (:goal (and (emptyhand) (on b1 b3) (on b2 b5) (on b3 b4) (on b4 b2) (on-table b5) (on b6 b1) (clear b6)))
)
