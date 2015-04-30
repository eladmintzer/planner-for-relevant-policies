(define (problem p20)
    (:domain ctp)
    
    (:objects
        v0 v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 v11 v12 v13 v14 v15 v16 v17 v18 v19 v20 - vertex
        e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 e10 e11 e12 e13 e14 e15 e16 e17 e18 e19 e20 e21 e22 e23 e24 e25 e26 e27 e28 e29 e30 e31 e32 e33 e34 e35 e36 e37 e38 e39 - edge)
    (:init
    
        (adjacent v0 e0) (adjacent v1 e0)
        (adjacent v0 e1) (adjacent v1 e1)
        
        (adjacent v1 e2) (adjacent v2 e2)
        (adjacent v1 e3) (adjacent v2 e3)
        
        (adjacent v2 e4) (adjacent v3 e4)
        (adjacent v2 e5) (adjacent v3 e5)
        
        (adjacent v3 e6) (adjacent v4 e6)
        (adjacent v3 e7) (adjacent v4 e7)
        
        (adjacent v4 e8) (adjacent v5 e8)
        (adjacent v4 e9) (adjacent v5 e9)
        
        (adjacent v5 e10) (adjacent v6 e10)
        (adjacent v5 e11) (adjacent v6 e11)
        
        (adjacent v6 e12) (adjacent v7 e12)
        (adjacent v6 e13) (adjacent v7 e13)
        
        (adjacent v7 e14) (adjacent v8 e14)
        (adjacent v7 e15) (adjacent v8 e15)
        
        (adjacent v8 e16) (adjacent v9 e16)
        (adjacent v8 e17) (adjacent v9 e17)
        
        (adjacent v9 e18) (adjacent v10 e18)
        (adjacent v9 e19) (adjacent v10 e19)
        
        (adjacent v10 e20) (adjacent v11 e20)
        (adjacent v10 e21) (adjacent v11 e21)
        
        (adjacent v11 e22) (adjacent v12 e22)
        (adjacent v11 e23) (adjacent v12 e23)
        
        (adjacent v12 e24) (adjacent v13 e24)
        (adjacent v12 e25) (adjacent v13 e25)
        
        (adjacent v13 e26) (adjacent v14 e26)
        (adjacent v13 e27) (adjacent v14 e27)
        
        (adjacent v14 e28) (adjacent v15 e28)
        (adjacent v14 e29) (adjacent v15 e29)
        
        (adjacent v15 e30) (adjacent v16 e30)
        (adjacent v15 e31) (adjacent v16 e31)
        
        (adjacent v16 e32) (adjacent v17 e32)
        (adjacent v16 e33) (adjacent v17 e33)
        
        (adjacent v17 e34) (adjacent v18 e34)
        (adjacent v17 e35) (adjacent v18 e35)
        
        (adjacent v18 e36) (adjacent v19 e36)
        (adjacent v18 e37) (adjacent v19 e37)
        
        (adjacent v19 e38) (adjacent v20 e38)
        (adjacent v19 e39) (adjacent v20 e39)
        
        (at v0)
        
        (oneof (traversable e0) (traversable e1))
        (oneof (traversable e2) (traversable e3))
        (oneof (traversable e4) (traversable e5))
        (oneof (traversable e6) (traversable e7))
        (oneof (traversable e8) (traversable e9))
        (oneof (traversable e10) (traversable e11))
        (oneof (traversable e12) (traversable e13))
        (oneof (traversable e14) (traversable e15))
        (oneof (traversable e16) (traversable e17))
        (oneof (traversable e18) (traversable e19))
        (oneof (traversable e20) (traversable e21))
        (oneof (traversable e22) (traversable e23))
        (oneof (traversable e24) (traversable e25))
        (oneof (traversable e26) (traversable e27))
        (oneof (traversable e28) (traversable e29))
        (oneof (traversable e30) (traversable e31))
        (oneof (traversable e32) (traversable e33))
        (oneof (traversable e34) (traversable e35))
        (oneof (traversable e36) (traversable e37))
        (oneof (traversable e38) (traversable e39))
    )
    
    (:goal (at v20))
)