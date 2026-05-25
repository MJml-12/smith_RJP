import streamlit as st
import pandas as pd
import altair as alt
from itertools import combinations

# === PAGE CONFIG ===
st.set_page_config(
    page_title="いい食事取ろう！",
    page_icon="🍱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === LOAD DATA ===
df = pd.read_csv("smith_clean.csv")
df["p/c_score"] = pd.to_numeric(df["p/c_score"], errors="coerce")
df["タンパク"]   = pd.to_numeric(df["タンパク"],   errors="coerce")
df["値段"]       = pd.to_numeric(df["値段"],       errors="coerce")

KARBO_CATS = ["パン", "おにぎり", "ご飯"]
BENTO_CATS = ["弁当"]

def get_grup(cat):
    if cat in KARBO_CATS: return "karbo"
    if cat in BENTO_CATS: return "bento"
    return "lauk"

df["grup"] = df["カテゴリ"].apply(get_grup)

# === GLOBAL CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 1.2rem 1rem 2rem 1rem !important;
    max-width: 500px !important;
}

.app-header {
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.app-title {
    font-size: 1.55rem;
    font-weight: 600;
    color: #E2F5F1;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0 0 4px 0;
}
.app-sub {
    font-size: 0.75rem;
    color: #64a89f;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 0;
}

/* STAT CARDS */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-bottom: 1rem;
}
.stat-card {
    background: rgba(13, 148, 136, 0.08);
    border: 1px solid rgba(13, 148, 136, 0.18);
    border-radius: 12px;
    padding: 10px 8px 8px;
    text-align: center;
}
.stat-val {
    font-size: 1.2rem;
    font-weight: 600;
    color: #5EEAD4;
    line-height: 1.1;
    display: block;
    font-family: 'DM Mono', monospace;
}
.stat-lbl {
    font-size: 0.63rem;
    color: #64a89f;
    margin-top: 3px;
    display: block;
    letter-spacing: 0.02em;
}

/* SECTION TITLE */
.section-title {
    font-size: 0.68rem;
    font-weight: 600;
    color: #64a89f;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.5rem;
}

/* GROUP LABEL */
.group-label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 1rem 0 0.4rem;
}
.group-badge {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 20px;
}
.badge-lauk  { background: rgba(13,148,136,0.2);  color: #5EEAD4; }
.badge-karbo { background: rgba(245,158,11,0.2);  color: #F59E0B; }
.badge-bento { background: rgba(168,85,247,0.2);  color: #C084FC; }

/* RANK ITEMS */
.rank-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    margin-bottom: 6px;
}
.rank-item:hover { background: rgba(13,148,136,0.07); }
.rank-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    color: #64a89f;
    width: 18px;
    flex-shrink: 0;
    text-align: center;
}
.rank-num.gold   { color: #F59E0B; }
.rank-num.silver { color: #94A3B8; }
.rank-num.bronze { color: #92765A; }
.rank-name {
    flex: 1;
    font-size: 0.85rem;
    font-weight: 500;
    color: #E2F5F1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.rank-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    flex-shrink: 0;
    gap: 2px;
}
.rank-protein {
    font-size: 0.85rem;
    font-weight: 600;
    color: #5EEAD4;
    font-family: 'DM Mono', monospace;
}
.rank-price {
    font-size: 0.68rem;
    color: #64a89f;
}
.pc-badge {
    font-size: 0.6rem;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
}
.pc-hi  { background: rgba(13,148,136,0.25); color: #5EEAD4; }
.pc-mid { background: rgba(245,158,11,0.2);  color: #F59E0B; }
.pc-lo  { background: rgba(239,68,68,0.15);  color: #F87171; }

/* COMBO CARD */
.combo-card {
    background: rgba(13,148,136,0.06);
    border: 1px solid rgba(13,148,136,0.2);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 10px;
}
.combo-rank-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #64a89f;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.combo-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.combo-icon {
    font-size: 1rem;
    width: 24px;
    text-align: center;
    flex-shrink: 0;
}
.combo-name {
    flex: 1;
    font-size: 0.83rem;
    color: #E2F5F1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.combo-price-tag {
    font-size: 0.72rem;
    color: #64a89f;
    font-family: 'DM Mono', monospace;
    flex-shrink: 0;
}
.combo-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.combo-total-protein {
    font-size: 1.1rem;
    font-weight: 700;
    color: #5EEAD4;
    font-family: 'DM Mono', monospace;
}
.combo-total-price {
    font-size: 0.8rem;
    color: #94A3B8;
    font-family: 'DM Mono', monospace;
}
.combo-change-tag {
    font-size: 0.65rem;
    color: #64a89f;
}

/* DIVIDER */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 0.8rem 0;
}

/* Slider label */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-size: 0.72rem !important;
    color: #64a89f !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}

.vega-embed { border-radius: 12px; overflow: hidden; }

/* Tab styling */
div[data-testid="stTabs"] button {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# === HELPERS ===
def pc_badge(score):
    if score >= 5.0: return "pc-hi",  f"P/C {score:.1f} ✅"
    elif score >= 2.0: return "pc-mid", f"P/C {score:.1f} 🔶"
    else: return "pc-lo",  f"P/C {score:.1f} ❌"

RANK_ICONS = ["①","②","③","④","⑤"]
RANK_CLS   = ["gold","silver","bronze","",""]

def render_rank_list(data, max_n=5):
    if data.empty:
        st.info("該当する商品がありません")
        return
    for i, (_, row) in enumerate(data.head(max_n).iterrows()):
        bc, bt = pc_badge(row["p/c_score"])
        num_str = RANK_ICONS[i] if i < 5 else f"{i+1}"
        num_cls = RANK_CLS[i] if i < 3 else ""
        st.markdown(f"""
        <div class="rank-item">
            <span class="rank-num {num_cls}">{num_str}</span>
            <span class="rank-name">{row['商品名']}</span>
            <div class="rank-meta">
                <span class="rank-protein">{row['タンパク']}g</span>
                <span class="rank-price">¥{int(row['値段'])}</span>
                <span class="pc-badge {bc}">{bt}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def find_best_combos(df_lauk, df_karbo, df_bento, budget, n_lauk, n_karbo, include_bento, top_n=3):
    """Find top combos by total protein within budget."""
    results = []

    # Helper: get best lauk combo
    candidates = df_lauk[df_lauk["値段"] <= budget].sort_values("p/c_score", ascending=False).head(15)

    def lauk_combos(remaining, n):
        eligible = candidates[candidates["値段"] <= remaining]
        # Kalau n == 0 (tanpa lauk), return empty list
        if n == 0:
            return [[]]
        elif len(eligible) < n:
            combo = list(eligible.iloc[:].copy().iterrows())
            # Hanya ambil Series-nya
            combos = [[row for (idx, row) in combo]]
        else:
            combos = list(combinations(range(len(eligible)), n))
            combos = [[eligible.iloc[i] for i in c] for c in combos]
        return combos

    if include_bento:
        # Bento mode: bento only (already complete meal)
        for _, b in df_bento[df_bento["値段"] <= budget].iterrows():
            results.append({
                "items": [{"name": b["商品名"], "price": b["値段"], "protein": b["タンパク"], "type": "bento"}],
                "total_protein": b["タンパク"],
                "total_price": b["値段"]
            })
    else:
        # Karbo + Lauk mode
        karbo_pool = df_karbo[df_karbo["値段"] <= budget].sort_values("p/c_score", ascending=False).head(10) if n_karbo > 0 else pd.DataFrame()
        
        if n_karbo == 0:
            karbo_options = [None]
        else:
            karbo_options = [row for _, row in karbo_pool.iterrows()]

        for k_item in karbo_options:
            k_cost = k_item["値段"] if k_item is not None else 0
            if k_cost > budget:
                continue
            remaining = budget - k_cost

            lc = lauk_combos(remaining, n_lauk)
            for lset in lc:
                tp = sum(r["タンパク"] for r in lset)
                tc = sum(r["値段"] for r in lset)
                if tc <= remaining:
                    item_list = []
                    # Tambahkan karbo jika ada
                    if k_item is not None:
                        item_list.append({
                            "name": k_item["商品名"],
                            "price": k_item["値段"],
                            "protein": k_item["タンパク"],
                            "type": "karbo"
                        })
                    # Tambahkan lauk-lauk
                    for r in lset:
                        item_list.append({
                            "name": r["商品名"],
                            "price": r["値段"],
                            "protein": r["タンパク"],
                            "type": "lauk"
                        })
                    total_protein = (k_item["タンパク"] if k_item is not None else 0) + tp
                    total_price = k_cost + tc
                    results.append({
                        "items": item_list,
                        "total_protein": total_protein,
                        "total_price": total_price
                    })

    results.sort(key=lambda x: x["total_protein"], reverse=True)
    # Deduplicate by item name sets
    seen = set()
    unique = []
    for r in results:
        key = frozenset(i["name"] for i in r["items"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
        if len(unique) >= top_n:
            break
    return unique

TYPE_ICON = {"lauk": "🍗", "karbo": "🍞", "bento": "🍱"}

def render_combo(combo, rank):
    rank_labels = ["🥇 Best Pick", "🥈 2nd Option", "🥉 3rd Option"]
    label = rank_labels[rank] if rank < 3 else f"#{rank+1}"
    rows_html = ""
    for item in combo["items"]:
        icon = TYPE_ICON.get(item["type"], "•")
        rows_html += f"""
        <div class="combo-row">
            <span class="combo-icon">{icon}</span>
            <span class="combo-name">{item['name']}</span>
            <span class="combo-price-tag">¥{int(item['price'])} · {item['protein']}g</span>
        </div>"""
    st.markdown(f"""
    <div class="combo-card">
        <div class="combo-rank-label">{label}</div>
        {rows_html}
        <div class="combo-footer">
            <div>
                <span class="combo-total-protein">{combo['total_protein']:.1f}g</span>
                <span class="combo-change-tag"> タンパク合計</span>
            </div>
            <div>
                <span class="combo-total-price">¥{int(combo['total_price'])} 合計</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === HEADER ===
st.markdown("""
<div class="app-header">
    <p class="app-sub">スミス東中野 × TTC</p>
    <h1 class="app-title">いい食事取ろう！🍱</h1>
</div>
""", unsafe_allow_html=True)

# === TABS ===
tab1, tab2 = st.tabs(["🤖 自動おすすめ", "🔍 自分で選ぶ"])

# ─────────────────────────────────────
# TAB 1: AUTO COMBO
# ─────────────────────────────────────
with tab1:
    st.markdown("<p class='section-title'>予算と構成を設定</p>", unsafe_allow_html=True)
    
    budget_auto = st.slider("予算 (¥)", 150, 800, 500, step=10, key="budget_auto")

    meal_type = st.radio(
        "食事スタイル",
        ["🍗 おかず + 🍞 主食", "🍱 弁当のみ", "🍗 おかずのみ"],
        horizontal=True,
        key="meal_type"
    )

    col1, col2 = st.columns(2)
    if meal_type == "🍗 おかず + 🍞 主食":
        with col1:
            n_lauk_auto = st.selectbox("おかず品数", [1, 2, 3], index=1, key="nl_auto")
        with col2:
            n_karbo_auto = st.selectbox("主食品数", [1, 2], index=0, key="nk_auto")
        include_bento = False
    elif meal_type == "🍱 弁当のみ":
        n_lauk_auto, n_karbo_auto = 0, 0
        include_bento = True
    else:
        with col1:
            n_lauk_auto = st.selectbox("おかず品数", [1, 2, 3], index=1, key="nl_auto2")
        n_karbo_auto = 0
        include_bento = False

    df_lauk  = df[df["grup"] == "lauk"]
    df_karbo = df[df["grup"] == "karbo"]
    df_bento = df[df["grup"] == "bento"]

    combos = find_best_combos(df_lauk, df_karbo, df_bento, budget_auto,
                               n_lauk_auto, n_karbo_auto, include_bento, top_n=3)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>おすすめ組み合わせ TOP 3</p>", unsafe_allow_html=True)

    if not combos:
        st.warning("予算内で条件を満たす組み合わせが見つかりません。予算を上げてみてください。")
    else:
        for i, combo in enumerate(combos):
            render_combo(combo, i)

# ─────────────────────────────────────
# TAB 2: MANUAL / BROWSE
# ─────────────────────────────────────
with tab2:
    st.markdown("<p class='section-title'>フィルター</p>", unsafe_allow_html=True)
    
    budget_man = st.slider("予算上限 (¥)", 100, 800, 400, step=10, key="budget_man")
    
    sort_by = st.radio("並び替え", ["タンパク量", "P/Cスコア", "値段（安い順）"],
                        horizontal=True, key="sort_man")

    def sorted_df(data):
        if sort_by == "タンパク量":
            return data.sort_values("タンパク", ascending=False).reset_index(drop=True)
        elif sort_by == "P/Cスコア":
            return data.sort_values("p/c_score", ascending=False).reset_index(drop=True)
        else:
            return data.sort_values("値段", ascending=True).reset_index(drop=True)

    df_f = df[df["値段"] <= budget_man]

    # STAT CARDS
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    count     = len(df_f)
    avg_prot  = f"{df_f['タンパク'].mean():.1f}g" if not df_f.empty else "ー"
    min_price = f"¥{int(df_f['値段'].min())}"     if not df_f.empty else "ー"
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <span class="stat-val">{count}</span>
            <span class="stat-lbl">対象品目</span>
        </div>
        <div class="stat-card">
            <span class="stat-val">{avg_prot}</span>
            <span class="stat-lbl">平均タンパク</span>
        </div>
        <div class="stat-card">
            <span class="stat-val">{min_price}</span>
            <span class="stat-lbl">最安値</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # LAUK section
    df_lauk_f = sorted_df(df_f[df_f["grup"] == "lauk"])
    st.markdown("""
    <div class="group-label">
        <span class="group-badge badge-lauk">🍗 おかず（Lauk）</span>
    </div>
    """, unsafe_allow_html=True)
    render_rank_list(df_lauk_f, max_n=5)

    # KARBO section
    df_karbo_f = sorted_df(df_f[df_f["grup"] == "karbo"])
    st.markdown("""
    <div class="group-label">
        <span class="group-badge badge-karbo">🍞 主食（Karbo）</span>
    </div>
    """, unsafe_allow_html=True)
    render_rank_list(df_karbo_f, max_n=5)

    # BENTO section
    df_bento_f = sorted_df(df_f[df_f["grup"] == "bento"])
    st.markdown("""
    <div class="group-label">
        <span class="group-badge badge-bento">🍱 弁当（単品OK）</span>
    </div>
    """, unsafe_allow_html=True)
    render_rank_list(df_bento_f, max_n=5)

    # BAR CHART
    st.markdown("<p class='section-title'>コスパ上位 — おかずのみ (g/¥100)</p>", unsafe_allow_html=True)
    if not df_lauk_f.empty:
        bar_df = df_lauk_f.head(7)[["商品名","p/c_score"]].copy()
        bar_df.columns = ["商品名","score"]
        bar_df["level"] = bar_df["score"].apply(
            lambda s: "High" if s >= 5.0 else ("Mid" if s >= 2.0 else "Low"))
        bar = (
            alt.Chart(bar_df)
            .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
            .encode(
                y=alt.Y("商品名:N", sort="-x", title=None,
                        axis=alt.Axis(labelFontSize=11, labelColor="#94A3B8")),
                x=alt.X("score:Q", title="g / ¥100",
                        axis=alt.Axis(labelFontSize=10, labelColor="#64a89f")),
                color=alt.Color("level:N",
                    scale=alt.Scale(domain=["High","Mid","Low"],
                                    range=["#0D9488","#F59E0B","#EF4444"]),
                    legend=None),
                tooltip=["商品名", alt.Tooltip("score:Q", title="P/C", format=".2f")]
            )
            .properties(height=200)
            .configure_view(strokeWidth=0, fill="#0F1923")
            .configure_axis(grid=False, domain=False)
            .configure(background="#0F1923")
        )
        st.altair_chart(bar, use_container_width=True)
