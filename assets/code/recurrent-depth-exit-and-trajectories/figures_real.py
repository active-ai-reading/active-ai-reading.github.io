"""Figures drawn from real measurements on Huginn-0125 (see scratchpad/probe/huginn_probe.py + analyze.py).
Set FIGDATA=/path/to/figdata.json; render each class with  manim -s."""
import json, os
from manim import *
from narrated import *
from partA import block, same_height, C_PRE, C_CORE, C_CODA, C_STATE, C_DEF, C_OURS, C_BASE, C_EMB
from illustrations import note


def header(scene, _n, title):
    h = fit(tex(title, 36), 13.4).to_edge(UP, buff=0.25)
    scene.add(h)
    return h

FD = json.load(open(os.environ["FIGDATA"]))
MAXT = 64


def user_span(toks):
    """Index range of the user's question inside the chat template (from 'Tom' to '?')."""
    a = next(i for i, t in enumerate(toks) if t.strip() == "Tom")
    b = next(i for i in range(len(toks) - 1, -1, -1) if toks[i].strip() == "?")
    return a, b + 1


def tt(s, size=14, color=WHITE):
    s = s.replace("\\", "\\textbackslash ").replace("_", "\\_").replace("#", "\\#").replace("&", "\\&").replace("%", "\\%").replace("$", "\\$").replace("{", "\\{").replace("}", "\\}").replace("~", "\\textasciitilde ").replace("^", "\\^{}")
    if s.strip() == "":
        s = "\\textvisiblespace"
    return tex(f"\\texttt{{{s.strip()}}}", size, color)


class RealExits(Scene):
    def construct(self):
        d = FD["apples"]
        toks, ex = d["prompt_tokens"], d["prompt_exit"]
        a, b = user_span(toks)
        items = [(toks[i], ex[i], 0) for i in range(a, b)] + [(g["token"], g["exit"] if g["exited"] else None, 1) for g in d["generated"] if g["token"] not in ("<|end_turn|>", "<|end_text|>")]
        header(self, 8, "Measured on Huginn-0125: trips before the exit rule fires, token by token")
        n = len(items)
        width = 13.2
        dx = width / n
        x0 = -width / 2 + dx / 2
        unit = 2.9 / MAXT
        y0 = -0.55
        bars, cnts, labs = VGroup(), VGroup(), VGroup()
        for k, (t, r, ans) in enumerate(items):
            x = x0 + k * dx
            col = C_OURS if ans else C_CORE
            if r is None:
                bar = Rectangle(width=dx * 0.62, height=MAXT * unit, stroke_color=C_HEAVY, stroke_width=1.5, fill_color=C_HEAVY, fill_opacity=0.25)
                bar.move_to([x, y0 + MAXT * unit / 2, 0])
                cnts.add(tex("$>$64", 12, C_HEAVY).next_to(bar, UP, buff=0.04))
            else:
                cells = VGroup(*[Rectangle(width=dx * 0.62, height=unit, stroke_color=BLACK, stroke_width=0.5, fill_color=col, fill_opacity=0.9 if ans else 0.65) for _ in range(r)]).arrange(UP, buff=0)
                bar = cells.move_to([x, y0 + r * unit / 2, 0])
                cnts.add(tex(str(r), 13, C_TARGET if r >= 20 else WHITE).next_to(bar, UP, buff=0.04))
            bars.add(bar)
            labs.add(tt(t, 13, WHITE if ans else GREY_A).rotate(PI / 3).move_to([x, y0 - 0.12, 0], aligned_edge=UR).shift(RIGHT * 0.1))
        base = Line([-width / 2, y0, 0], [width / 2, y0, 0], color=GREY_B, stroke_width=1.5)
        npr = sum(1 for it in items if it[2] == 0)
        xs = x0 + (npr - 0.5) * dx
        sep = DashedLine([xs, y0, 0], [xs, 3.05, 0], color=GREY_B, stroke_width=1.5)
        bp = tex("the question (prompt tokens)", 16, C_CORE).move_to([(x0 - dx / 2 + xs) / 2, 3.15, 0])
        ba = tex("the answer, generated token by token", 16, C_OURS).move_to([(xs + width / 2) / 2, 3.15, 0])
        fin = [r for _, r, _ in items if r is not None]
        mean = sum(fin) / len(fin)
        ml = DashedLine([-width / 2, y0 + mean * unit, 0], [width / 2, y0 + mean * unit, 0], color=C_NOTE, stroke_width=1, dash_length=0.08)
        mll = tex(f"dashed line: mean of the tokens that exit, {mean:.1f} trips", 13, C_NOTE).move_to([-width / 2 + 2.2, 2.55, 0], aligned_edge=LEFT)
        ans = tex("model's answer: \\texttt{" + d["answer"].strip().replace("\n", " ") + "}", 16, C_OURS).move_to([0, -1.95, 0])
        kw = dict(size=15, width=4.35, line_buff=0.07, title_size=19)
        p1 = panel("how this was measured", ["we ran the recurrence ourselves, one trip at a time, on an", "Apple M4 laptop; after each trip the coda + unembedding give", "token probabilities; a token 'exits' at the first trip where", "KL(previous, current) $< 5\\cdot10^{-4}$, the paper's rule"], C_TARGET, **kw)
        p2 = panel("what the bars show", ["prompt tokens: the trip at which the rule \\emph{would} fire", "(during prompt processing all 64 trips still run);", "answer tokens: the model really stopped there and the", "token was read off at that trip (greedy decoding)"], C_OURS, **kw)
        p3 = panel("what we see", ["the numbers, `and', `now' loop longest; `How', `many',", "`does', `apples' settle in about ten trips; the digit `2'", "of 12 never settled within 64 trips (next figure);", "the answer itself is right, with 7 to 28 trips per token"], C_NOTE, **kw)
        row = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.18)
        same_height(p1, p2, p3)
        fit(row, 13.4)
        self.add(base, bars, cnts, labs, sep, bp, ba, ml, mll, ans, row)


class RealKL(Scene):
    def construct(self):
        d = FD["apples"]
        toks, ex, kl = d["prompt_tokens"], d["prompt_exit"], d["prompt_kl"]
        a, b = user_span(toks)
        header(self, 9, "The exit rule at work: how far the next-token distribution moves on each trip")
        W, H = 8.6, 4.6
        ax = VGroup(Line([0, 0, 0], [W, 0, 0], color=GREY_B), Line([0, 0, 0], [0, H, 0], color=GREY_B))
        lo, hi = -7.0, 1.0

        def Y(v):
            return (np.clip(np.log10(max(v, 1e-12)), lo, hi) - lo) / (hi - lo) * H

        ticks = VGroup()
        for e in range(int(lo), int(hi) + 1):
            y = (e - lo) / (hi - lo) * H
            ticks.add(Line([-0.08, y, 0], [0, y, 0], color=GREY_B, stroke_width=1), tex(f"$10^{{{e}}}$", 12, C_NOTE).move_to([-0.45, y, 0]))
        for t in [1, 8, 16, 24, 32, 40, 48, 56, 64]:
            x = (t - 1) / (MAXT - 1) * W
            ticks.add(Line([x, -0.08, 0], [x, 0, 0], color=GREY_B, stroke_width=1), tex(str(t), 12, C_NOTE).move_to([x, -0.28, 0]))
        xl = tex("trip around the loop", 15, C_NOTE).move_to([W / 2, -0.6, 0])
        yl = tex("KL(previous trip, this trip)", 15, C_NOTE).rotate(PI / 2).move_to([-1.0, H / 2, 0])
        thr = DashedLine([0, Y(5e-4), 0], [W, Y(5e-4), 0], color=C_TARGET, stroke_width=1.5, dash_length=0.1)
        thrl = VGroup()
        # choose positions: fastest, a middle one, slowest finite, one that never exits
        idx = list(range(a, b))
        fin = [i for i in idx if ex[i] is not None]
        never = [i for i in idx if ex[i] is None]
        pick = [min(fin, key=lambda i: ex[i]), sorted(fin, key=lambda i: ex[i])[len(fin) // 2], max(fin, key=lambda i: ex[i])] + never[:1]
        cols = [C_CORE, C_PRE, C_TARGET, C_HEAVY]
        curves, leg = VGroup(), VGroup()
        for i, c in zip(pick, cols):
            pts = [[(t) / (MAXT - 1) * W, Y(kl[i][t]), 0] for t in range(MAXT)]
            curves.add(VMobject(color=c, stroke_width=2.5).set_points_as_corners(pts))
            if ex[i] is not None:
                curves.add(Dot(pts[ex[i] - 1], radius=0.07, color=c))
            lab = f"exits at trip {ex[i]}" if ex[i] is not None else "never below the threshold"
            leg.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=3), VGroup(tt(toks[i], 14, c), tex(lab, 13, C_NOTE)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.12))
        leg.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        chart = VGroup(ax, ticks, xl, yl, thr, thrl, curves)
        exp = VGroup(
            panel("reading the plot", ["after every trip we ask: how different is the", "next-token distribution from the one a trip ago?", "the curves fall as the state settles; the dot", "marks the first trip under the threshold"], C_TARGET, size=15, width=4.3, line_buff=0.07, title_size=19),
            panel("tokens in the question", [leg, VGroup(DashedLine(ORIGIN, RIGHT * 0.4, color=C_TARGET, stroke_width=2, dash_length=0.08), tex("exit threshold $5\\cdot10^{-4}$", 13, C_NOTE)).arrange(RIGHT, buff=0.12)], WHITE, size=15, width=4.3, line_buff=0.07, title_size=19),
            panel("the paper's point", ["no training for this: the exit rule is a", "zero-shot check on the output; most tokens", "settle, one hovers just above the line for", "all 64 trips, and the compute follows"], C_OURS, size=15, width=4.3, line_buff=0.07, title_size=19),
        ).arrange(DOWN, buff=0.18)
        both = VGroup(chart, exp).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.35)
        fit(both, 13.4, 6.6)
        self.add(both)


class RealTraj(Scene):
    def construct(self):
        d = FD["apples"]
        toks, ex = d["prompt_tokens"], d["prompt_exit"]
        a, b = user_span(toks)
        header(self, 10, "Latent trajectories measured on Huginn-0125: a big early swing, then small orbits")
        idx = list(range(a, b))
        never = [i for i in idx if ex[i] is None]
        fin = sorted([i for i in idx if ex[i] is not None], key=lambda i: ex[i])
        order = (never[:1] + [fin[-1], fin[0]])
        cols = {}
        rows = [VGroup(), VGroup()]
        for i in order:
            P = d["pca"][str(i)]
            col = C_HEAVY if ex[i] is None else (C_TARGET if ex[i] >= 20 else C_OURS)
            cols[i] = col
            for r, (key, vkey, t0) in enumerate([("xy", "var", 0), ("xy_late", "var_late", 32)]):
                xy = np.array(P[key]); xy = xy / (np.abs(xy).max() + 1e-9) * 0.95
                n = len(xy)
                dots = VGroup(*[Dot([x, y, 0], radius=0.045, color=interpolate_color(GREY_D, col, k / (n - 1))) for k, (x, y) in enumerate(xy)])
                path = VMobject(color=col, stroke_width=1.2, stroke_opacity=0.5).set_points_as_corners([[x, y, 0] for x, y in xy])
                box = Square(2.3, stroke_color=GREY_B, stroke_width=1)
                var = P[vkey]
                lab = (f"trips 1--64" if r == 0 else "trips 33--64 only, re-projected")
                cap = VGroup(VGroup(tt(toks[i], 16, col), tex("exits at trip " + str(ex[i]) if ex[i] is not None else "never exits", 13, C_NOTE)).arrange(RIGHT, buff=0.15),
                             tex(lab + f"; PC1+PC2 = {100 * (var[0] + var[1]):.0f}\\% of the variance", 11, C_NOTE)).arrange(DOWN, buff=0.04)
                rows[r].add(VGroup(VGroup(box, path, dots), cap).arrange(DOWN, buff=0.08))
        grid = VGroup(rows[0].arrange(RIGHT, buff=0.45), rows[1].arrange(RIGHT, buff=0.45)).arrange(DOWN, buff=0.2)
        # per-trip movement for the three tokens
        W, H = 3.6, 2.2
        ax = VGroup(Line([0, 0, 0], [W, 0, 0], color=GREY_B), Line([0, 0, 0], [0, H, 0], color=GREY_B))
        mv = {i: np.array(d["pca"][str(i)]["move"]) for i in order}
        top = max(m.max() for m in mv.values())
        cv = VGroup()
        for i in order:
            m = mv[i]
            cv.add(VMobject(color=cols[i], stroke_width=2.5).set_points_as_corners([[k / (len(m) - 1) * W, np.log10(m[k] / top * 1000) / 3 * H, 0] for k in range(len(m))]))
        tk = VGroup(*[tex(str(t), 11, C_NOTE).move_to([(t - 2) / 62 * W, -0.2, 0]) for t in [2, 16, 32, 48, 64]])
        yl = VGroup(tex("1/1000", 10, C_NOTE).move_to([-0.4, 0, 0]), tex("1/10", 10, C_NOTE).move_to([-0.4, 2 / 3 * H, 0]), tex("1", 10, C_NOTE).move_to([-0.4, H, 0]))
        ch = VGroup(ax, cv, tk, yl, tex("trip", 12, C_NOTE).move_to([W / 2, -0.45, 0]), tex("distance moved on this trip, relative to the largest (log)", 12, C_NOTE).move_to([W / 2, H + 0.2, 0]))
        side = VGroup(ch, panel("how to read", ["top row: the state after each trip, dark to bright,", "projected on the token's own two leading principal", "directions. Bottom row: trips 33 to 64 only, re-projected,", "so the late moves are not squashed by the early ones.", "Chart: step length per trip, all three tokens alike:", "a swing of a few trips, then steady small steps of", "about 1/300 of the first. Small, but not random: the", "late states trace orbits and spirals, the patterns of", "the paper's Figure 10, even for tokens that exited early"], WHITE, size=14, width=4.6, line_buff=0.06, title_size=18)).arrange(DOWN, buff=0.35)
        both = VGroup(grid, side).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.35)
        fit(both, 13.4, 6.7)
        self.add(both)


class RealTrajGrid(Scene):
    """Late-window (trips 33-64) trajectories of every token in the question."""
    def construct(self):
        d = FD["apples"]
        toks, ex = d["prompt_tokens"], d["prompt_exit"]
        a, b = user_span(toks)
        header(self, 11, "Where each token of the question goes late in the loop (trips 33 to 64, measured on Huginn-0125)")
        cards = VGroup()
        for i in range(a, b):
            P = d["pca"][str(i)]
            col = C_HEAVY if ex[i] is None else (C_TARGET if ex[i] >= 20 else C_OURS)
            xy = np.array(P["xy_late"]); xy = xy / (np.abs(xy).max() + 1e-9) * 0.8
            n = len(xy)
            dots = VGroup(*[Dot([x, y, 0], radius=0.04, color=interpolate_color(GREY_D, col, k / (n - 1))) for k, (x, y) in enumerate(xy)])
            path = VMobject(color=col, stroke_width=1.2, stroke_opacity=0.55).set_points_as_corners([[x, y, 0] for x, y in xy])
            box = Square(1.9, stroke_color=GREY_B, stroke_width=1)
            lab = "never exits" if ex[i] is None else f"exit {ex[i]}"
            cap = VGroup(tt(toks[i], 15, col), tex(lab, 12, C_NOTE)).arrange(RIGHT, buff=0.12)
            cards.add(VGroup(VGroup(box, path, dots), cap).arrange(DOWN, buff=0.06))
        grid = cards.arrange_in_grid(rows=4, cols=5, buff=(0.3, 0.18))
        leg = VGroup(
            VGroup(Dot(radius=0.06, color=C_OURS), tex("exits before trip 20", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(radius=0.06, color=C_TARGET), tex("exits at trip 20 or later", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(radius=0.06, color=C_HEAVY), tex("never below the KL threshold in 64 trips", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            tex("dark $\\rightarrow$ bright: trip 33 $\\rightarrow$ 64", 13, C_NOTE),
            tex("axes: each token's own top-2 PCA", 13, C_NOTE),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        legp = panel("legend", [leg], WHITE, size=13, width=3.2, line_buff=0.08, title_size=16)
        slot = VGroup(legp).move_to(cards[-1]).shift(RIGHT * (cards[1].get_center()[0] - cards[0].get_center()[0]))
        # put the legend in the empty 20th slot
        fit(legp, cards[0].width, cards[0].height)
        legp.move_to(cards[-1].get_center() + RIGHT * (cards[1].get_center()[0] - cards[0].get_center()[0]))
        all_ = VGroup(grid, legp).move_to(DOWN * 0.35)
        fit(all_, 13.4, 6.8)
        self.add(all_)


AD = os.environ.get("ANSWER_DIR", "")


def answer_data():
    g = json.load(open(f"{AD}/answer.json"))
    lat = np.load(f"{AD}/latents_answer.npy").astype(np.float32)    # tokens x trips x 5280
    return g, lat


def show_tok(t):
    return "end" if t.startswith("<|end") else t


class RealAnswerTraj(Scene):
    """Late-window trajectories of the state that produced each answer token."""
    def construct(self):
        g, lat = answer_data()
        header(self, 12, "The same picture for the answer: where the state goes while each token is being produced")
        cards = VGroup()
        for k, t in enumerate(g):
            X = lat[k, 32:]
            X = X - X.mean(0, keepdims=True)
            U, s, _ = np.linalg.svd(X, full_matrices=False)
            xy = U[:, :2] * s[:2]
            xy = xy / (np.abs(xy).max() + 1e-9) * 0.8
            ex = t["exit"] if t["exited"] else None
            col = C_HEAVY if ex is None else (C_TARGET if ex >= 20 else C_OURS)
            n = len(xy)
            dots = VGroup(*[Dot([x, y, 0], radius=0.04, color=interpolate_color(GREY_D, col, i / (n - 1))) for i, (x, y) in enumerate(xy)])
            path = VMobject(color=col, stroke_width=1.2, stroke_opacity=0.55).set_points_as_corners([[x, y, 0] for x, y in xy])
            box = Square(1.9, stroke_color=GREY_B, stroke_width=1)
            cap = VGroup(tt(show_tok(t["token"]), 15, col), tex("never exits" if ex is None else f"exit {ex}", 12, C_NOTE)).arrange(RIGHT, buff=0.12)
            cards.add(VGroup(VGroup(box, path, dots), cap).arrange(DOWN, buff=0.06))
        grid = cards.arrange_in_grid(rows=3, cols=5, buff=(0.3, 0.18))
        leg = VGroup(
            VGroup(Dot(radius=0.06, color=C_OURS), tex("exits before trip 20", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(radius=0.06, color=C_TARGET), tex("exits at trip 20 or later", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            tex("dark $\\rightarrow$ bright: trip 33 $\\rightarrow$ 64", 13, C_NOTE),
            tex("axes: each token's own top-2 PCA", 13, C_NOTE),
            tex("state of the last position while", 13, C_NOTE), tex("that token was being generated", 13, C_NOTE),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        legp = panel("legend", [leg], WHITE, size=13, width=3.2, line_buff=0.08, title_size=16)
        fit(legp, cards[0].width, cards[0].height)
        legp.move_to(cards[-1].get_center() + RIGHT * (cards[1].get_center()[0] - cards[0].get_center()[0]))
        all_ = VGroup(grid, legp).move_to(DOWN * 0.35)
        fit(all_, 13.4, 6.8)
        self.add(all_)


class RealAnswerTable(Scene):
    """What the answer would have been if we had stopped at each trip."""
    def construct(self):
        g, _ = answer_data()
        header(self, 13, "If we had stopped at trip $t$: the most likely next token after each trip, for every answer position")
        T = 32
        cw, rh = 0.37, 0.36
        x0 = -6.2 + 1.3
        rows = VGroup()
        for k, t in enumerate(g):
            y = 2.6 - k * rh
            final = t["token"]
            pt = t["per_trip"]
            # runs of equal prediction
            runs = []
            start = 0
            for i in range(1, T + 1):
                if i == T or pt[i] != pt[start]:
                    runs.append((start, i, pt[start]))
                    start = i
            cells = VGroup()
            for s_, e_, tokn in runs:
                same = tokn == final
                r = Rectangle(width=(e_ - s_) * cw, height=rh * 0.82, stroke_color=BLACK, stroke_width=0.6,
                              fill_color=C_OURS if same else C_HEAVY, fill_opacity=0.75 if same else 0.45)
                r.move_to([x0 + (s_ + (e_ - s_) / 2) * cw, y, 0])
                cells.add(r)
                if (e_ - s_) * cw > 0.5:
                    cells.add(tt(show_tok(tokn), 12, WHITE).move_to(r))
                else:
                    cells.add(tt(show_tok(tokn), 9, WHITE).move_to(r))
            ex = t["exit"]
            tick = Line([x0 + ex * cw, y - rh / 2, 0], [x0 + ex * cw, y + rh / 2, 0], color=C_TARGET, stroke_width=2.5)
            lab = VGroup(tex(f"token {k + 1}:", 12, C_NOTE), tt(show_tok(final), 13, WHITE)).arrange(RIGHT, buff=0.08).move_to([x0 - 0.15, y, 0], aligned_edge=RIGHT)
            rows.add(VGroup(cells, tick, lab))
        ticks = VGroup()
        for tnum in [1, 4, 8, 12, 16, 20, 24, 28, 32]:
            x = x0 + (tnum - 0.5) * cw
            ticks.add(tex(str(tnum), 11, C_NOTE).move_to([x, 2.6 + rh * 0.75, 0]))
        tl = tex("trip at which we stop", 13, C_NOTE).move_to([x0 + T * cw / 2, 2.6 + rh * 1.45, 0])
        leg = VGroup(
            VGroup(Rectangle(width=0.35, height=0.2, fill_color=C_OURS, fill_opacity=0.75, stroke_width=0), tex("same token as the final answer", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            VGroup(Rectangle(width=0.35, height=0.2, fill_color=C_HEAVY, fill_opacity=0.45, stroke_width=0), tex("a different token", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
            VGroup(Line(ORIGIN, UP * 0.25, color=C_TARGET, stroke_width=2.5), tex("where the exit rule stopped", 13, C_NOTE)).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.5).move_to([x0 + T * cw / 2, 2.6 - len(g) * rh - 0.05, 0])
        note_ = tex("each row is one position of the answer, generated after the earlier rows were fixed; the cell at trip $t$ is the token the coda would output if the loop stopped there. No row changes after trip 11; trips 33 to 64 are identical and omitted", 13, C_NOTE).move_to([0, 2.6 - len(g) * rh - 0.5, 0])
        fit(note_, 13.2)
        self.add(rows, ticks, tl, leg, note_)
