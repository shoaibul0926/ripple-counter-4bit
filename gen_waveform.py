"""Generate timing diagrams for the 4-bit ripple counter.

Models exactly what tb_ripple_counter_4bit.v does (10 ns clock, TPD = 1 ns per stage,
reset low 0-12 ns, async reset pulse at 339-342 ns, run to 358 ns) and draws every
bit as a 0/1 digital wave. Run: python gen_waveform.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TPD, END = 1, 358
NAMES = ["clk", "rst_n", "q[0]", "q[1]", "q[2]", "q[3]"]

# ---- stimulus -------------------------------------------------------------
clk_ev = [(0, 0)] + [(t, (t // 5) % 2) for t in range(5, END + 1, 5)]
rst_ev = [(0, 0), (12, 1), (339, 0), (342, 1)]

def val_at(events, t):
    v = events[0][1]
    for tt, vv in events:
        if tt <= t:
            v = vv
    return v

# ---- ripple model ---------------------------------------------------------
q = [[(0, 0)] for _ in range(4)]           # x -> 0 by async reset at t=0..1 (drawn as 0)
def cur(i, t): return val_at(q[i], t)

pending = []                                # (time, stage, action)
for i in range(1, len(clk_ev)):             # stage 0 clocked by clk falling edges
    t, v = clk_ev[i]
    if v == 0 and clk_ev[i - 1][1] == 1:
        pending.append((t, 0, "edge"))
pending.append((339, -1, "reset"))          # async reset fall

# process in time order, edges may spawn new edges on the next stage
import heapq
heap = [(t, s, a) for t, s, a in pending]
heapq.heapify(heap)
while heap:
    t, s, a = heapq.heappop(heap)
    if a == "reset":
        for i in range(4):
            if cur(i, t + TPD) != 0:
                q[i].append((t + TPD, 0))
        continue
    if val_at(rst_ev, t) == 0:              # reset dominates
        continue
    new = 1 - cur(s, t)
    q[s].append((t + TPD, new))
    if new == 0 and s < 3:                  # falling q[s] clocks the next stage
        heapq.heappush(heap, (t + TPD, s + 1, "edge"))

waves = [clk_ev, rst_ev] + q

def step_xy(events, t0, t1):
    xs, ys = [], []
    v = val_at(events, t0)
    xs.append(t0); ys.append(v)
    for t, vv in events:
        if t0 < t < t1:
            xs += [t, t]; ys += [v, vv]; v = vv
    xs.append(t1); ys.append(v)
    return xs, ys

def bus_segments(t0, t1):
    times = sorted({t0, t1} | {t for w in q for t, _ in w if t0 < t < t1})
    segs = []
    for a, b in zip(times, times[1:]):
        bits = [val_at(q[i], a) for i in range(4)]
        segs.append((a, b, "".join(str(x) for x in reversed(bits))))
    return segs

def draw(ax, t0, t1, label_min=4.0, edge_labels=False):
    rows = len(NAMES) + 1
    colors = ["#1f77b4", "#2ca02c", "#d62728", "#ff7f0e", "#9467bd", "#8c564b"]
    for r, (name, ev) in enumerate(zip(NAMES, waves)):
        base = (rows - 1 - r) * 1.8
        xs, ys = step_xy(ev, t0, t1)
        ax.plot(xs, [base + y for y in ys], color=colors[r], lw=1.6, drawstyle="default")
        ax.axhline(base, color="#dddddd", lw=0.5, zorder=0)
        ax.axhline(base + 1, color="#dddddd", lw=0.5, zorder=0)
        ax.text(t0 - (t1 - t0) * 0.005, base + 0.5, name, ha="right", va="center", fontsize=9, fontweight="bold")
        ax.text(t1 + (t1 - t0) * 0.004, base, "0", va="center", fontsize=7, color="#888")
        ax.text(t1 + (t1 - t0) * 0.004, base + 1, "1", va="center", fontsize=7, color="#888")
        # digit labels inside each level for the bit waves
        if r >= 2 or r == 1:
            pts = sorted({t0, t1} | {t for t, _ in ev if t0 < t < t1})
            for a, b in zip(pts, pts[1:]):
                if b - a >= label_min:
                    v = val_at(ev, a)
                    ax.text((a + b) / 2, base + (0.5 if v else 0.5), str(v), ha="center", va="center",
                            fontsize=7, color=colors[r], alpha=0.9,
                            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))
    # bus row
    base = 0
    ax.text(t0 - (t1 - t0) * 0.005, base + 0.5, "q[3:0]", ha="right", va="center", fontsize=9, fontweight="bold")
    for a, b, bits in bus_segments(t0, t1):
        w = b - a
        if w <= 1.5:                                   # transient (ripple glitch) values
            ax.fill([a, b, b, a], [0, 0, 1, 1], color="#f4c7c3", ec="#d62728", lw=0.6)
            if edge_labels and w >= 0.9:
                ax.text((a + b) / 2, 1.18, bits, ha="center", va="bottom", fontsize=6.5, color="#d62728", rotation=90)
        else:
            ax.fill([a, b, b, a], [0, 0, 1, 1], color="#e8f1fb", ec="#1f77b4", lw=0.8)
            if w >= label_min:
                ax.text((a + b) / 2, 0.5, bits, ha="center", va="center", fontsize=8, family="monospace", fontweight="bold")
    ax.set_xlim(t0, t1); ax.set_ylim(-0.4, rows * 1.8 - 0.4)
    ax.set_yticks([]); ax.set_xlabel("time (ns)")
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#eeeeee", lw=0.6)
    # clock-edge guide lines
    for t in range(10, END + 1, 10):
        if t0 <= t <= t1:
            ax.axvline(t, color="#cccccc", lw=0.5, ls=":", zorder=0)

# ---- figure 1: full run in two halves ------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(24, 11))
draw(axes[0], 0, 180); draw(axes[1], 178, END)
fig.suptitle("4-bit ripple counter: full simulation (all bits, 0/1)   |   clock 10 ns, TPD = 1 ns/stage; "
             "rst_n low 0-12 ns and again 339-342 ns", fontsize=13)
fig.tight_layout(rect=(0.04, 0, 1, 0.97))
fig.savefig("waveform_full.png", dpi=130)

# ---- figure 2: zoom on the worst-case ripple, 7 -> 8 ----------------------
fig, ax = plt.subplots(figsize=(14, 5.5))
draw(ax, 84, 96, label_min=0.9, edge_labels=True)
ax.set_title("Ripple detail: count 0111 -> 1000 at the falling clock edge (t = 90 ns). "
             "Each stage settles 1 ns after the previous one; red = transient values", fontsize=10)
fig.tight_layout(rect=(0.05, 0, 1, 1))
fig.savefig("waveform_ripple_zoom.png", dpi=150)

print("q0 events (first 6):", q[0][:6])
print("7->8 transitions:", [(i, [e for e in q[i] if 90 <= e[0] <= 94]) for i in range(4)])
