`timescale 1ns/1ps

module tb_ripple_counter_4bit;
    reg        clk;
    reg        rst_n;
    wire [3:0] q;

    integer errors;
    integer i;
    reg [3:0] expected;

    ripple_counter_4bit dut (.clk(clk), .rst_n(rst_n), .q(q));

    // 100 MHz clock (period 10 ns); the ripple settles in ~4 ns, well inside a cycle
    initial clk = 1'b0;
    always #5 clk = ~clk;

    task check(input [3:0] exp, input [255:0] what);
        begin
            if (q !== exp) begin
                errors = errors + 1;
                $display("FAIL @%0t: %0s: q=%0d expected=%0d", $time, what, q, exp);
            end
        end
    endtask

    initial begin
        $dumpfile("ripple_counter_4bit.vcd");
        $dumpvars(0, tb_ripple_counter_4bit);

        errors = 0;
        rst_n  = 1'b0;
        #12;
        check(4'd0, "after reset");
        rst_n = 1'b1;

        // Count through 2 full wraps (32 falling edges). Sample just before each
        // next falling edge, after the ripple has settled.
        expected = 4'd0;
        for (i = 0; i < 32; i = i + 1) begin
            @(negedge clk);
            expected = expected + 4'd1;   // wraps 15 -> 0 naturally
            #8;                           // > 4 x TPD
            check(expected, "count");
            $display("t=%0t q=%b (%0d)", $time, q, q);
        end

        // Async reset mid-count: must clear without waiting for a clock edge
        #1 rst_n = 1'b0;
        #3 check(4'd0, "async reset mid-count");
        rst_n = 1'b1;

        // Counts again from 0 after reset release
        @(negedge clk); #8;
        check(4'd1, "first count after reset");

        if (errors == 0) $display("PASS: all checks passed");
        else             $display("FAIL: %0d error(s)", errors);
        $finish;
    end
endmodule
