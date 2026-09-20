`timescale 1ns/1ps
// T flip-flop built from a D flip-flop and an inverter
module T_FF(q, clk, reset);
    output q;
    input  clk, reset;
    wire   d;

    D_FF dff0(q, d, clk, reset);
    not  n1(d, q);          // not is a Verilog primitive; D = ~Q makes it toggle
endmodule
