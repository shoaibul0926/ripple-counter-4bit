`timescale 1ns/1ps
// 4-bit asynchronous (ripple) up counter.
// Each stage is clocked by the output of the previous stage, not by the
// common clock, so the count ripples from Q[0] to Q[3].
module ripple_counter_4bit (
    input  wire       clk,
    input  wire       rst_n,   // active-low asynchronous reset
    output wire [3:0] q
);
    t_ff ff0 (.clk(clk),  .rst_n(rst_n), .t(1'b1), .q(q[0]));
    t_ff ff1 (.clk(q[0]), .rst_n(rst_n), .t(1'b1), .q(q[1]));
    t_ff ff2 (.clk(q[1]), .rst_n(rst_n), .t(1'b1), .q(q[2]));
    t_ff ff3 (.clk(q[2]), .rst_n(rst_n), .t(1'b1), .q(q[3]));
endmodule
