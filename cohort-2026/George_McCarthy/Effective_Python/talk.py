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
def _(pl):
    from sklearn.datasets import load_iris

    _iris = load_iris(as_frame=True)
    df = pl.from_pandas(_iris.frame).rename(
        lambda c: c.replace(" (cm)", "").replace(" ", "_")
    ).with_columns(
        species=pl.col("target").replace_strict(
            dict(enumerate(_iris.target_names)), return_dtype=pl.String
        )
    ).drop("target")
    df
    return (df,)


@app.cell
def _(alt, df, mo):
    chart = mo.ui.altair_chart(
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(x="petal_length", y="petal_width", color="species")
        .properties(height=300)
    )
    chart
    return (chart,)


@app.cell
def _(chart, mo):
    _sel = chart.value
    mo.vstack(
        [
            mo.md(f"**{len(_sel)} flowers selected**, species: "
                  f"{dict(_sel['species'].value_counts().iter_rows()) if len(_sel) else '-'}"),
            mo.ui.table(_sel),
        ]
    )
    return


@app.cell
def _(mo):
    min_petal = mo.ui.slider(1, 7, step=0.1, value=4, label="min petal length (cm)")
    min_petal
    return (min_petal,)


@app.cell(hide_code=True)
def _(df, min_petal, mo):
    summary = mo.sql(
        f"""
        SELECT species, COUNT(*) AS flowers
        FROM df
        WHERE petal_length >= {min_petal.value}
        GROUP BY species
        """
    )
    return


@app.cell
def _(df, mo):
    df_editor = mo.ui.dataframe(df)
    df_editor
    return (df_editor,)


@app.cell
def _(df, mo):
    mo.ui.data_explorer(df)
    return


@app.cell
def _(df, mo, pl):
    _args = mo.cli_args()
    _min = float(_args.get("min-petal", 4))
    _n = int(_args.get("n", 6))
    _report = (
        df.filter(pl.col("petal_length") >= _min)
        .group_by("species")
        .agg(pl.len().alias("n"), pl.col("sepal_length").mean().round(2).alias("mean_sepal_length"))
        .sort("species")
    )
    if mo.app_meta().mode == "script":
        print("\n=== talk.py running as a plain Python script ===")
        print(f"CLI args: {dict(_args) or '(none)'}")
        print(f"squares up to n={_n}: {[i**2 for i in range(_n)]}")
        print(f"\nIris flowers with petal length >= {_min} cm, per species:")
        print(_report)
        print("\nSame notebook, same code, no browser needed.")
    _report
    return


if __name__ == "__main__":
    app.run()
