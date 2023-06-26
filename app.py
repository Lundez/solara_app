import solara
import pandas as pd
import polars as pl

@solara.component
def Page():
    file, set_file = solara.use_state(None)
    solara.FileDrop(on_file=set_file, lazy=False)
    solara.Text(f"Hello World!")
    Page2(file)

@solara.component
def Page2(file):

    if file is not None:
        solara.Text(f"File")
        df = pl.read_csv(file["data"])
        solara.Text("WOOOW")
        solara.DataFrame(df.to_pandas())
    else:
        solara.Text("No file, please upload one.")

