# 4-Bit Ripple Counter (Verilog)

Asynchronous 4-bit up counter built from four negative-edge T flip-flops. Each stage is clocked by the previous stage's output, so the count ripples from `q[0]` to `q[3]`.

```
clk ─▶ FF0 ─q0─▶ FF1 ─q1─▶ FF2 ─q2─▶ FF3 ─q3
        T=1        T=1        T=1        T=1      (all share active-low async rst_n)
```

## Files
| File | Purpose |
|---|---|
| `t_ff.v` | Negedge T flip-flop, async active-low reset, `TPD` clk-to-Q delay |
| `ripple_counter_4bit.v` | Top module: 4 chained T flip-flops |
| `tb_ripple_counter_4bit.v` | Self-checking testbench (reset, 2 full wraps, async reset mid-count) |

## Run online (no install)
1. Open [EDA Playground](https://www.edaplayground.com/).
2. Simulator: **Icarus Verilog**; check **Open EPWave after run**.
3. Paste `tb_ripple_counter_4bit.v` in the testbench pane and `t_ff.v` + `ripple_counter_4bit.v` in the design pane.
4. Run. Expect `PASS: all checks passed`.

## Run locally (Icarus Verilog)
```
iverilog -o sim t_ff.v ripple_counter_4bit.v tb_ripple_counter_4bit.v
vvp sim
gtkwave ripple_counter_4bit.vcd
```

## Notes
- Ripple counters are not fully synchronous: outputs settle stage by stage (about 4 × `TPD`), so the max clock frequency is limited by the total ripple delay, and intermediate glitch values appear briefly on `q`.
- The testbench samples 8 ns after each falling edge, once the ripple has settled.
