#Assembly Language Test
Start: lda 0x04
        adda 0x1F
        inva
        adda 0x2F
        sta 0x4000
        jsr [TEST]
        ldx 0x400
        sta 0x400
        inca
        sta 0x401
        inca
        sta 0x402
        ldb [X+0]
        ldb [X+1]
        ldb [x+2]
        stb [x+500]
        sta [X+501]


End:    hlt



TEST: lda 0x06
    ldb 0x03
    lds 0x5012
    psha
    pshb
    rfs