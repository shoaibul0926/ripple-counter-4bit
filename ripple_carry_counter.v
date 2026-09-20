`timescale 1ns/1ps
// Top block: 4-bit ripple carry counter
module ripple_carry_counter(q, clk, reset);
    output [3:0] q;
    input        clk, reset;

    // 4 instances of the T flip-flop; each is clocked by the previous stage's q
    T_FF tff0(q[0], clk,  reset);
    T_FF tff1(q[1], q[0], reset);
    T_FF tff2(q[2], q[1], reset);
    T_FF tff3(q[3], q[2], reset);
endmodule
