(define (problem bw_1_1)
  (:domain blocks-domain)
  (:objects b1 - block)
  (:init (fair) (emptyhand) (on-table b1) (clear b1))
  (:goal (and (emptyhand) (on-table b1) (clear b1)))
)