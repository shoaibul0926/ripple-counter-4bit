`timescale 1ns/1ps
// Stimulus block (testbench): drives clk and reset, prints q
module stimulus;
    reg        clk;
    reg        reset;
    wire [3:0] q;

    // instantiate the design block
    ripple_carry_counter r1(q, clk, reset);

    // clock: toggles every 5 ns (period 10 ns)
    initial clk = 1'b0;
    always #5 clk = ~clk;

    // control reset
    initial begin
        reset = 1'b1;       // reset the counter
        #15 reset = 1'b0;   // release reset, counting starts
        #180 reset = 1'b1;  // reset again mid-count
        #10 reset = 1'b0;
        #20 $finish;
    end

    // waveform dump (EDA Playground / EPWave) and console monitor
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, stimulus);
    end
    initial $monitor($time, " Output q = %d", q);
endmodule
