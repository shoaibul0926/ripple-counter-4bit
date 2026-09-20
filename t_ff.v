`timescale 1ns/1ps
// Negative-edge triggered T flip-flop with active-low async reset.
// T is tied high in the counter, so each stage toggles on every falling clk edge.
module t_ff (
    input  wire clk,
    input  wire rst_n,
    input  wire t,
    output reg  q
);
    parameter TPD = 1; // clk-to-Q delay (sim only) so the ripple is visible in waveforms

    always @(negedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= #TPD 1'b0;
        else if (t)
            q <= #TPD ~q;
    end
endmodule
