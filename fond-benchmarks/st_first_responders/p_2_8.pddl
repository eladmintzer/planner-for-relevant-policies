(define (problem fr_2_8)
    (:domain first-response)
    (:objects
        l1 l2 - location
        f1 - fire_unit
        v1 v2 v3 v4 v5 v6 v7 v8 - victim
        m1 m2 - medical_unit
    )
    (:init
        (hospital l2)
        (hospital l1)
        (water-at l2)
        (water-at l1)
        (fire l1)
        (victim-at v1 l2)
        (victim-status v1 hurt)
        (victim-at v2 l1)
        (victim-status v2 hurt)
        (fire l2)
        (victim-at v3 l1)
        (victim-status v3 dying)
        (victim-at v4 l2)
        (victim-status v4 dying)
        (victim-at v5 l2)
        (victim-status v5 hurt)
        (victim-at v6 l1)
        (victim-status v6 hurt)
        (victim-at v7 l1)
        (victim-status v7 hurt)
        (victim-at v8 l2)
        (victim-status v8 dying)
        (adjacent l1 l1)
        (adjacent l2 l2)
        (adjacent l2 l1)
        (adjacent l1 l2)
        (fire-unit-at f1 l2)
        (medical-unit-at m1 l1)
        (medical-unit-at m2 l1)
    )
    (:goal
        (and
            (nfire l1)
            (nfire l2)
            (victim-status v1 healthy)
            (victim-status v2 healthy)
            (victim-status v3 healthy)
            (victim-status v4 healthy)
            (victim-status v5 healthy)
            (victim-status v6 healthy)
            (victim-status v7 healthy)
            (victim-status v8 healthy)
        )
    )
)