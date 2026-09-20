@echo off
rem Compile, simulate and open the waveform (Icarus Verilog + GTKWave in C:\iverilog)
set PATH=%PATH%;C:\iverilog\bin;C:\iverilog\gtkwave\bin
iverilog -o sim D_FF.v T_FF.v ripple_carry_counter.v stimulus.v || exit /b 1
vvp sim
start "" gtkwave dump.vcd --script view.tcl
