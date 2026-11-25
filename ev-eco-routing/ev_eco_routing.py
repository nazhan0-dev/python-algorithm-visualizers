import heapq
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ══════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════
GRAPH = {
    "Songkhla":    {"Phatthalung": 15, "Satun": 20, "Pattani": 15, "Yala": 25},
    "Phatthalung": {"Songkhla": 15, "Trang": 30, "Satun":10},
    "Trang":       {"Phatthalung": 30, "Satun": 15},
    "Satun":       {"Songkhla": 20, "Trang": 15, "Yala":40, "Phatthalung":10},
    "Pattani":     {"Songkhla": 15, "Yala": 10, "Narathiwat": 20},
    "Yala":        {"Songkhla": 25, "Pattani": 10, "Narathiwat": 25, "Satun":40},
    "Narathiwat":  {"Pattani": 20, "Yala": 25},
}
CITIES = list(GRAPH.keys())

# พิกัดแผนที่ (x=ตะวันตก→ตะวันออก, y=เหนือ→ใต้)
POS = {
    "Trang":       (0.08, 0.88),
    "Phatthalung": (0.25, 0.72),
    "Satun":       (0.14, 0.52),
    "Songkhla":    (0.52, 0.62),
    "Pattani":     (0.72, 0.42),
    "Yala":        (0.60, 0.24),
    "Narathiwat":  (0.88, 0.10),
}

# ── Colour Palette ──
BG       = "#080c14"
PANEL    = "#0d1524"
CARD     = "#111d30"
BORDER   = "#1e3050"
ACCENT   = "#00d4ff"
GREEN    = "#00e676"
GOLD     = "#ffd166"
ORANGE   = "#ff6b35"
RED      = "#ff4466"
MUTED    = "#5a7a9a"
TEXT     = "#e8f4ff"
CYAN2    = "#00bcd4"


# ══════════════════════════════════════════════
#  DIJKSTRA
# ══════════════════════════════════════════════
def dijkstra(start: str, end: str):
    dist = {c: float("inf") for c in CITIES}
    prev = {}
    dist[start] = 0
    heap = [(0, start)]
    visited = set()
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            break
        for nb, w in GRAPH.get(node, {}).items():
            nc = cost + w
            if nc < dist[nb]:
                dist[nb] = nc
                prev[nb] = node
                heapq.heappush(heap, (nc, nb))
    if dist[end] == float("inf"):
        return float("inf"), []
    path, cur = [], end
    while cur:
        path.insert(0, cur)
        cur = prev.get(cur)
    return dist[end], path


# ══════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════
class EVRoutingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EV Eco-Routing · ภาคใต้ตอนล่าง")
        self.configure(bg=BG)
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.resizable(True, True)

        self.sel_start = tk.StringVar(value="")
        self.sel_end   = tk.StringVar(value="")
        self.battery   = tk.IntVar(value=75)
        self.mode      = "start"   # 'start' | 'end'
        self._city_btns = {}

        self._build_header()
        self._build_body()
        self._draw_map([], None, None)  # empty map

    # ─────────────────────────────────────────
    #  HEADER
    # ─────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=PANEL, height=62)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        # logo box
        logo = tk.Label(hdr, text="⚡", bg=ACCENT, fg="#020c14",
                        font=("Helvetica", 20, "bold"), width=3, height=1)
        logo.pack(side="left", padx=(16, 12), pady=10)

        info = tk.Frame(hdr, bg=PANEL)
        info.pack(side="left")
        tk.Label(info, text="EV ECO-ROUTING", bg=PANEL, fg=ACCENT,
                 font=("Courier", 15, "bold")).pack(anchor="w")
        tk.Label(info, text="ระบบนำทางประหยัดแบตเตอรี่ · ภาคใต้ตอนล่าง · Dijkstra's Algorithm",
                 bg=PANEL, fg=MUTED, font=("Helvetica", 9)).pack(anchor="w")

        # separator line
        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x")

    # ─────────────────────────────────────────
    #  BODY  (sidebar + canvas)
    # ─────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_canvas_area(body)

    # ─────────────────────────────────────────
    #  SIDEBAR
    # ─────────────────────────────────────────
    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=PANEL, width=310)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # right border
        tk.Frame(parent, bg=BORDER, width=1).pack(side="left", fill="y")

        inner = tk.Frame(sb, bg=PANEL)
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # ── Section: เลือกจุดเดินทาง ──
        self._section_label(inner, "เลือกจุดเดินทาง")

        # Mode toggle
        mode_row = tk.Frame(inner, bg=PANEL)
        mode_row.pack(fill="x", pady=(4, 8))
        self.btn_mode_start = self._mode_btn(mode_row, "📍 เลือก ต้นทาง", "start")
        self.btn_mode_start.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.btn_mode_end   = self._mode_btn(mode_row, "🏁 เลือก ปลายทาง", "end")
        self.btn_mode_end.pack(side="left", fill="x", expand=True)
        self._refresh_mode_btns()

        # City grid
        grid = tk.Frame(inner, bg=PANEL)
        grid.pack(fill="x")
        for i, city in enumerate(CITIES):
            btn = tk.Button(
                grid, text=city, bg=CARD, fg=MUTED,
                relief="flat", bd=0, cursor="hand2",
                font=("Helvetica", 9, "bold"),
                activebackground=BORDER, activeforeground=TEXT,
                command=lambda c=city: self._select_city(c),
            )
            btn.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew", ipady=7)
            grid.columnconfigure(i%2, weight=1)
            self._city_btns[city] = btn

        # Spacer
        tk.Frame(inner, bg=PANEL, height=10).pack()

        # ── Selection display ──
        sel_row = tk.Frame(inner, bg=PANEL)
        sel_row.pack(fill="x", pady=(0, 10))

        start_box = self._sel_box(sel_row, "📍 ต้นทาง", GREEN)
        start_box.pack(side="left", fill="x", expand=True)
        self.lbl_start_val = self._sel_val(start_box, "—", GREEN)

        tk.Label(sel_row, text="→", bg=PANEL, fg=MUTED,
                 font=("Helvetica", 14)).pack(side="left", padx=4)

        end_box = self._sel_box(sel_row, "🏁 ปลายทาง", GOLD)
        end_box.pack(side="left", fill="x", expand=True)
        self.lbl_end_val = self._sel_val(end_box, "—", GOLD)

        # ── Battery ──
        self._section_label(inner, "แบตเตอรี่ปัจจุบัน")
        bat_card = tk.Frame(inner, bg=CARD, padx=12, pady=10)
        bat_card.pack(fill="x")
        self._add_border(bat_card)

        bat_top = tk.Frame(bat_card, bg=CARD)
        bat_top.pack(fill="x")
        bat_left = tk.Frame(bat_top, bg=CARD)
        bat_left.pack(side="left")
        tk.Label(bat_left, text="STATE OF CHARGE", bg=CARD, fg=MUTED,
                 font=("Courier", 7, "bold")).pack(anchor="w")
        self.lbl_bat_pct = tk.Label(bat_left, text="75%", bg=CARD, fg=GREEN,
                                    font=("Courier", 22, "bold"))
        self.lbl_bat_pct.pack(anchor="w")
        self.lbl_bat_emoji = tk.Label(bat_top, text="🔋", bg=CARD,
                                      font=("Helvetica", 22))
        self.lbl_bat_emoji.pack(side="right")

        # Battery bar (canvas-drawn)
        self.bat_canvas = tk.Canvas(bat_card, height=12, bg=CARD,
                                    highlightthickness=0)
        self.bat_canvas.pack(fill="x", pady=(8, 6))
        self.bat_canvas.bind("<Configure>", lambda e: self._draw_bat_bar())

        # Slider
        slider = ttk.Scale(bat_card, from_=0, to=100,
                           variable=self.battery, orient="horizontal",
                           command=lambda v: self._on_battery_change())
        slider.pack(fill="x")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TScale", troughcolor=BORDER, background=ACCENT,
                        sliderlength=18, sliderrelief="flat")

        # ── Calculate button ──
        tk.Frame(inner, bg=PANEL, height=12).pack()
        calc_btn = tk.Button(
            inner, text="⚡  คำนวณเส้นทาง",
            bg=ACCENT, fg="#020c14", relief="flat", bd=0, cursor="hand2",
            font=("Helvetica", 11, "bold"), activebackground="#009ecc",
            command=self._calculate,
        )
        calc_btn.pack(fill="x", ipady=11)

        # ── Result card ──
        tk.Frame(inner, bg=PANEL, height=8).pack()
        self.result_frame = tk.Frame(inner, bg=CARD, padx=10, pady=10)
        self.result_frame.pack(fill="x")
        self.lbl_result_status = tk.Label(self.result_frame, text="",
                                          bg=CARD, font=("Helvetica", 10, "bold"),
                                          wraplength=260, justify="left")
        self.lbl_result_status.pack(anchor="w")
        self.lbl_result_path = tk.Label(self.result_frame, text="",
                                        bg=CARD, fg=MUTED,
                                        font=("Helvetica", 9),
                                        wraplength=260, justify="left")
        self.lbl_result_path.pack(anchor="w", pady=(4, 0))

        self.stat_row = tk.Frame(self.result_frame, bg=CARD)
        self.stat_row.pack(fill="x", pady=(8, 0))

        # ── Legend ──
        tk.Frame(inner, bg=PANEL, height=10).pack()
        self._section_label(inner, "สัญลักษณ์")
        leg = tk.Frame(inner, bg=PANEL)
        leg.pack(fill="x")
        items = [
            (GREEN,  "●", "ต้นทาง"),
            (GOLD,   "●", "ปลายทาง"),
            (CYAN2,  "●", "โหนดผ่าน"),
            (MUTED,  "●", "โหนดอื่น"),
            (ACCENT, "━", "เส้นทางที่เลือก"),
            (BORDER, "╌", "เส้นทางอื่น"),
        ]
        for i, (col, sym, txt) in enumerate(items):
            f = tk.Frame(leg, bg=PANEL)
            f.grid(row=i//2, column=i%2, sticky="w", padx=(0,10), pady=1)
            tk.Label(f, text=sym, bg=PANEL, fg=col,
                     font=("Helvetica", 11)).pack(side="left")
            tk.Label(f, text=txt, bg=PANEL, fg=MUTED,
                     font=("Helvetica", 8)).pack(side="left", padx=3)

    # ─────────────────────────────────────────
    #  CANVAS AREA
    # ─────────────────────────────────────────
    def _build_canvas_area(self, parent):
        area = tk.Frame(parent, bg=BG)
        area.pack(side="left", fill="both", expand=True)

        self.fig = Figure(facecolor=BG)
        self.ax  = self.fig.add_subplot(111)
        self.ax.set_facecolor(BG)

        self.mpl_canvas = FigureCanvasTkAgg(self.fig, master=area)
        self.mpl_canvas.get_tk_widget().pack(fill="both", expand=True)

    # ─────────────────────────────────────────
    #  HELPER WIDGETS
    # ─────────────────────────────────────────
    def _section_label(self, parent, text):
        tk.Label(parent, text=text.upper(),
                 bg=PANEL if parent["bg"]==PANEL else CARD,
                 fg=ACCENT, font=("Courier", 7, "bold")).pack(anchor="w", pady=(6,2))

    def _mode_btn(self, parent, text, mode):
        return tk.Button(
            parent, text=text, relief="flat", bd=0, cursor="hand2",
            font=("Helvetica", 8, "bold"),
            command=lambda m=mode: self._set_mode(m),
        )

    def _sel_box(self, parent, label_text, color):
        f = tk.Frame(parent, bg=CARD, padx=8, pady=6)
        tk.Label(f, text=label_text, bg=CARD, fg=MUTED,
                 font=("Courier", 7)).pack(anchor="w")
        return f

    def _sel_val(self, parent, text, color):
        lbl = tk.Label(parent, text=text, bg=CARD, fg=color,
                       font=("Courier", 10, "bold"))
        lbl.pack(anchor="w")
        return lbl

    def _add_border(self, widget):
        widget.config(highlightbackground=BORDER,
                      highlightthickness=1,
                      highlightcolor=ACCENT)

    # ─────────────────────────────────────────
    #  BATTERY BAR
    # ─────────────────────────────────────────
    def _draw_bat_bar(self):
        c = self.bat_canvas
        c.delete("all")
        w = c.winfo_width()
        h = 12
        # track
        c.create_rounded_rect(0, 2, w, h-2, radius=5, fill=BORDER, outline="")
        # fill
        pct = self.battery.get() / 100
        fw  = max(10, int(w * pct))
        col = GREEN if pct >= 0.6 else (GOLD if pct >= 0.3 else RED)
        c.create_rounded_rect(0, 2, fw, h-2, radius=5, fill=col, outline="")

    def _on_battery_change(self):
        v = self.battery.get()
        self.lbl_bat_pct.config(text=f"{v}%")
        col = GREEN if v >= 60 else (GOLD if v >= 30 else RED)
        self.lbl_bat_pct.config(fg=col)
        em = "🔋" if v >= 70 else ("🪫" if v >= 30 else "⚠️")
        self.lbl_bat_emoji.config(text=em)
        self._draw_bat_bar()

    # ─────────────────────────────────────────
    #  MODE & CITY SELECTION
    # ─────────────────────────────────────────
    def _set_mode(self, mode):
        self.mode = mode
        self._refresh_mode_btns()

    def _refresh_mode_btns(self):
        if self.mode == "start":
            self.btn_mode_start.config(bg=CARD, fg=GREEN,
                                       highlightbackground=GREEN,
                                       highlightthickness=1,
                                       text="📍 กำลังเลือก ต้นทาง")
            self.btn_mode_end.config(bg=CARD, fg=MUTED,
                                     highlightbackground=BORDER,
                                     highlightthickness=1,
                                     text="🏁 เลือก ปลายทาง")
        else:
            self.btn_mode_start.config(bg=CARD, fg=MUTED,
                                       highlightbackground=BORDER,
                                       highlightthickness=1,
                                       text="📍 เลือก ต้นทาง")
            self.btn_mode_end.config(bg=CARD, fg=GOLD,
                                     highlightbackground=GOLD,
                                     highlightthickness=1,
                                     text="🏁 กำลังเลือก ปลายทาง")

    def _select_city(self, city):
        if self.mode == "start":
            self.sel_start.set(city)
            self.lbl_start_val.config(text=city)
            self._set_mode("end")  # auto switch
        else:
            self.sel_end.set(city)
            self.lbl_end_val.config(text=city)
        self._refresh_city_buttons()

    def _refresh_city_buttons(self):
        s, e = self.sel_start.get(), self.sel_end.get()
        for city, btn in self._city_btns.items():
            if city == s:
                btn.config(bg="#0d2b1a", fg=GREEN,
                           highlightbackground=GREEN, highlightthickness=1)
            elif city == e:
                btn.config(bg="#2b2200", fg=GOLD,
                           highlightbackground=GOLD, highlightthickness=1)
            else:
                btn.config(bg=CARD, fg=MUTED,
                           highlightbackground=BORDER, highlightthickness=1)

    # ─────────────────────────────────────────
    #  CALCULATE
    # ─────────────────────────────────────────
    def _clear_stat_row(self):
        for w in self.stat_row.winfo_children():
            w.destroy()

    def _calculate(self):
        s = self.sel_start.get()
        e = self.sel_end.get()
        bat = self.battery.get()

        self._clear_stat_row()

        if not s or not e:
            self._show_result(False, "⚠️ กรุณาเลือกต้นทางและปลายทาง", "")
            return
        if s == e:
            self._show_result(False, "⚠️ ต้นทางและปลายทางต้องไม่ใช่เมืองเดียวกัน", "")
            return

        cost, path = dijkstra(s, e)

        if not path:
            self._show_result(False, "❌ ไม่พบเส้นทาง", "")
            self._draw_map([], s, e)
            return

        path_str = " → ".join(path)

        if bat >= cost:
            rem = bat - cost
            self._show_result(True,
                              "✅ แบตเตอรี่เพียงพอ สามารถเดินทางได้",
                              f"เส้นทาง: {path_str}")
            self._add_stats(
                ("แบตที่ใช้", f"{cost}%", ORANGE),
                ("แบตที่เหลือ", f"{rem}%", GREEN),
            )
            self._draw_map(path, s, e)
        else:
            lack = cost - bat
            self._show_result(False,
                              "❌ แบตเตอรี่ไม่เพียงพอ กรุณาชาร์จก่อนออกเดินทาง",
                              f"ต้องใช้: {cost}%  |  มีแค่: {bat}%")
            self._add_stats(
                ("ต้องใช้",  f"{cost}%",    ORANGE),
                ("ขาดอยู่", f"-{lack}%",   RED),
            )
            self._draw_map([], s, e)   # ไม่แสดงเส้นทาง

    def _show_result(self, ok, status, path_text):
        col = GREEN if ok else RED
        border_col = GREEN if ok else RED
        self.result_frame.config(highlightbackground=border_col,
                                 highlightthickness=1,
                                 highlightcolor=border_col)
        self.lbl_result_status.config(text=status, fg=col)
        self.lbl_result_path.config(text=path_text)

    def _add_stats(self, *stats):
        for label, val, col in stats:
            f = tk.Frame(self.stat_row, bg=CARD)
            f.pack(side="left", expand=True)
            tk.Label(f, text=val, bg=CARD, fg=col,
                     font=("Courier", 13, "bold")).pack()
            tk.Label(f, text=label, bg=CARD, fg=MUTED,
                     font=("Helvetica", 7)).pack()

    # ─────────────────────────────────────────
    #  DRAW MAP
    # ─────────────────────────────────────────
    def _draw_map(self, path, start, end):
        ax = self.ax
        ax.clear()
        ax.set_facecolor(BG)
        self.fig.patch.set_facecolor(BG)

        # Grid dots
        for xi in np.arange(0.0, 1.05, 0.07):
            for yi in np.arange(0.0, 1.05, 0.07):
                ax.plot(xi, yi, ".", color=ACCENT, alpha=0.07, markersize=2, zorder=0)

        path_edges = set()
        for i in range(len(path)-1):
            path_edges.add((path[i], path[i+1]))
            path_edges.add((path[i+1], path[i]))

        drawn = set()
        # ── Draw edges ──
        for city_a, neighbors in GRAPH.items():
            for city_b, weight in neighbors.items():
                if (city_a, city_b) in drawn or (city_b, city_a) in drawn:
                    continue
                drawn.add((city_a, city_b))

                xa, ya = POS[city_a]
                xb, yb = POS[city_b]
                is_path = (city_a, city_b) in path_edges

                if is_path:
                    # glow under-layer
                    ax.plot([xa, xb], [ya, yb], color=ACCENT, lw=10,
                            alpha=0.18, solid_capstyle="round", zorder=1)
                    # main line
                    ax.plot([xa, xb], [ya, yb], color=ACCENT, lw=3.5,
                            solid_capstyle="round", zorder=2)
                    # arrow head
                    if path and city_a in path and city_b in path:
                        idx_a = path.index(city_a) if city_a in path else -1
                        idx_b = path.index(city_b) if city_b in path else -1
                        if idx_a != -1 and idx_b != -1 and abs(idx_a - idx_b) == 1:
                            if idx_a < idx_b:
                                dx, dy = xb-xa, yb-ya
                            else:
                                dx, dy = xa-xb, ya-yb
                            mx, my = (xa+xb)/2, (ya+yb)/2
                            ax.annotate("", xy=(mx+dx*0.01, my+dy*0.01),
                                        xytext=(mx-dx*0.01, my-dy*0.01),
                                        arrowprops=dict(arrowstyle="-|>",
                                                        color=ORANGE, lw=1.5),
                                        zorder=3)
                else:
                    ax.plot([xa, xb], [ya, yb], color=BORDER, lw=1.2,
                            linestyle=(0,(5,4)), solid_capstyle="round", zorder=1)

                # Edge weight label
                mx, my = (xa+xb)/2, (ya+yb)/2
                lbl_col  = "#ffffff" if is_path else MUTED
                lbl_bg   = ACCENT    if is_path else "#0d1524"
                ax.text(mx, my, f"{weight}%",
                        ha="center", va="center",
                        fontsize=8.5, color=lbl_col, fontweight="bold" if is_path else "normal",
                        bbox=dict(boxstyle="round,pad=0.25", fc=lbl_bg,
                                  ec=ACCENT if is_path else BORDER,
                                  lw=1.0 if is_path else 0.5),
                        zorder=4)

        # ── Draw nodes ──
        for city in CITIES:
            x, y = POS[city]
            is_start = city == start
            is_end   = city == end
            in_path  = city in path and not is_start and not is_end

            if is_start:
                node_col  = GREEN
                ring_col  = GREEN
                text_col  = GREEN
                icon      = "📍"
                size      = 220
                ring_size = 320
            elif is_end:
                node_col  = GOLD
                ring_col  = GOLD
                text_col  = GOLD
                icon      = "🏁"
                size      = 220
                ring_size = 320
            elif in_path:
                node_col  = CYAN2
                ring_col  = CYAN2
                text_col  = CYAN2
                icon      = "•"
                size      = 160
                ring_size = 240
            else:
                node_col  = "#1e2d45"
                ring_col  = BORDER
                text_col  = MUTED
                icon      = "·"
                size      = 120
                ring_size = 180

            # glow ring
            if is_start or is_end or in_path:
                ax.scatter(x, y, s=ring_size, color=ring_col,
                           alpha=0.18, zorder=5, linewidths=0)
            # outer ring
            ax.scatter(x, y, s=size+60, color=BG,
                       edgecolors=ring_col, linewidths=1.8, zorder=6)
            # fill
            ax.scatter(x, y, s=size, color=node_col,
                       alpha=0.9 if (is_start or is_end) else 0.75,
                       zorder=7, linewidths=0)

            # city name
            offset_y = -0.06
            ax.text(x, y + offset_y, city,
                    ha="center", va="top",
                    fontsize=9, color=text_col, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", fc="#080c14",
                              ec="none", alpha=0.85),
                    zorder=8)

        # Watermark
        ax.text(0.99, 0.01, "EV ECO-ROUTING · DIJKSTRA",
                ha="right", va="bottom",
                fontsize=7, color=ACCENT, alpha=0.22,
                transform=ax.transAxes, zorder=9)

        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.axis("off")
        self.fig.tight_layout(pad=0.5)
        self.mpl_canvas.draw()

def _create_rounded_rect(canvas, x1, y1, x2, y2, radius=8, **kwargs):
    pts = [
        x1+radius, y1,  x2-radius, y1,
        x2, y1,          x2, y1+radius,
        x2, y2-radius,  x2, y2,
        x2-radius, y2,  x1+radius, y2,
        x1, y2,          x1, y2-radius,
        x1, y1+radius,  x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)

tk.Canvas.create_rounded_rect = _create_rounded_rect

if __name__ == "__main__":
    app = EVRoutingApp()
    app.mainloop()