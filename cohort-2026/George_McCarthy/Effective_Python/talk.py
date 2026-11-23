import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="6 cool things in marimo")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import polars as pl
    import altair as alt

    return alt, mo, np, pl


@app.cell
def _(mo):
    mo.md("""
    # 6 cool things you can do in marimo

    A reactive Python notebook that is stored as a plain `.py` file.

    1. Reactive execution: no hidden state
    2. UI widgets with no callbacks
    3. Select points in a chart and get the data back in Python
    4. SQL cells that query your dataframes
    5. Explore and transform dataframes live, with no code
    6. It's just a Python file: git, scripts, apps, and the browser
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 1. Reactive execution

    marimo reads which variables each cell defines and which it uses, and builds a
    dependency graph. Change a cell and everything that depends on it reruns.
    Delete a cell and its variables disappear. Run order is never "whatever you
    clicked last", so the notebook always matches what's on screen.

    **Demo:** change `n` below and watch the next cell update.
    """)
    return


@app.cell
def _():
    n = 10
    return (n,)


@app.cell
def _(n):
    squares = [i**2 for i in range(n)]
    squares
    return


@app.cell
def _(mo):
    mo.md("""
    Each variable can be defined in only one cell, which is what makes the graph
    possible. Try defining `n` again in a new cell and marimo will flag it.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. UI widgets with no callbacks

    A widget is just a variable. When you move it, every cell that reads
    `.value` reruns, with no callbacks or event handlers.
    """)
    return


@app.cell
def _(mo):
    freq = mo.ui.slider(0.5, 10, step=0.5, value=2, label="frequency")
    amp = mo.ui.slider(0.1, 3, step=0.1, value=1, label="amplitude")
    noise = mo.ui.switch(label="add noise")
    mo.hstack([freq, amp, noise])
    return amp, freq, noise


@app.cell
def _(alt, amp, freq, noise, np, pl):
    _x = np.linspace(0, 2 * np.pi, 400)
    _y = amp.value * np.sin(freq.value * _x)
    if noise.value:
        _y = _y + np.random.default_rng(0).normal(0, 0.15, _x.size)
    alt.Chart(pl.DataFrame({"x": _x, "y": _y})).mark_line().encode(
        x="x", y=alt.Y("y", scale=alt.Scale(domain=[-3.5, 3.5]))
    ).properties(width="container", height=250)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 3. Select points in a chart and get the data back in Python

    Wrap an Altair chart in `mo.ui.altair_chart` and your brush selection
    becomes a dataframe that the rest of the notebook can use.

    **Demo:** drag a box over some points.
    """)
    return


@app.cell
def _(np, pl):
    _rng = np.random.default_rng(42)
    _k = 300
    _cluster = _rng.integers(0, 3, _k)
    _centres = np.array([[0, 0], [4, 1], [1, 4]])
    _pts = _centres[_cluster] + _rng.normal(0, 0.8, (_k, 2))
    df = pl.DataFrame(
        {
            "x": _pts[:, 0],
            "y": _pts[:, 1],
            "cluster": [f"c{c}" for c in _cluster],
            "score": _rng.uniform(0, 1, _k).round(3),
        }
    )
    return (df,)


@app.cell
def _(alt, df, mo):
    chart = mo.ui.altair_chart(
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(x="x", y="y", color="cluster")
        .properties(height=300)
    )
    chart
    return (chart,)


@app.cell
def _(chart, mo):
    _sel = chart.value
    mo.vstack(
        [
            mo.md(f"**{len(_sel)} points selected**, mean score "
                  f"{_sel['score'].mean() if len(_sel) else float('nan'):.3f}"),
            mo.ui.table(_sel),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4. SQL cells that query your dataframes

    `mo.sql` runs DuckDB over any dataframe in scope, and the result is
    another dataframe. SQL cells are reactive too, and can use widget values.
    """)
    return


@app.cell
def _(mo):
    min_score = mo.ui.slider(0, 1, step=0.05, value=0.5, label="min score")
    min_score
    return (min_score,)


@app.cell
def _(df, min_score, mo):
    summary = mo.sql(
        f"""
        SELECT cluster,
               COUNT(*)              AS n,
               ROUND(AVG(score), 3)  AS mean_score,
               ROUND(AVG(x), 2)      AS mean_x,
               ROUND(AVG(y), 2)      AS mean_y
        FROM df
        WHERE score >= {min_score.value}
        GROUP BY cluster
        ORDER BY cluster
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## 5. Explore and transform dataframes live

    `mo.ui.dataframe` wraps any dataframe in a point-and-click editor. You can
    filter, group, aggregate, sort and select columns, and it **writes the
    Polars code for you** (see the "Python code" tab). The result is a normal
    dataframe in `.value`, so downstream cells react to it.

    **Demo:** add a filter `score > 0.5`, then group by `cluster` and take the
    mean, and watch the cell below update.
    """)
    return


@app.cell
def _(df, mo):
    df_editor = mo.ui.dataframe(df)
    df_editor
    return (df_editor,)


@app.cell
def _(df_editor, mo):
    _out = df_editor.value
    mo.md(f"Downstream cell sees **{_out.height} rows x {_out.width} columns**: "
          f"`{', '.join(_out.columns)}`")
    return


@app.cell
def _(mo):
    mo.md("""
    For quick visual exploration, `mo.ui.data_explorer` lets you drag columns
    onto x, y, colour and size and suggests charts.
    """)
    return


@app.cell
def _(df, mo):
    mo.ui.data_explorer(df)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 6. It's just a Python file

    Open `talk.py` in an editor and you'll see plain Python with each cell as a
    function. That means:

    | What you want | Command |
    |---|---|
    | Clean git diffs and code review | it's a `.py` file |
    | Run it as a script | `python talk.py` |
    | Serve it as an app (code hidden) | `marimo run talk.py` |
    | Pin dependencies inside the file | `marimo edit --sandbox talk.py` |
    | Run it in the browser with no server (WebAssembly) | `marimo export html-wasm talk.py -o site` |
    | Edit it with AI | `marimo edit` has built-in AI cell generation |

    No more `.ipynb` JSON merge conflicts, and no "restart and run all" before
    sharing.
    """)
    return


if __name__ == "__main__":
    app.run()
