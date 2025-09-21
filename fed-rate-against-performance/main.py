import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fredapi import Fred
import yfinance as yf

def get_fred_data(series_id, api_key):
    fred = Fred(api_key=api_key)
    data = fred.get_series(series_id)
    data = pd.DataFrame(data, columns=[series_id])
    return data

fig = make_subplots(specs=[[{"secondary_y": True}]])
sp500 = yf.download("^GSPC", start='2000-01-01')['Close'].rename(columns={'^GSPC': 'SP500'})
fed_rate = get_fred_data("FEDFUNDS", "2661922b82963fc69da3796653138901").reset_index().rename(columns={'index': 'Date'})
combined_df = pd.merge(fed_rate, sp500, on='Date', how='inner')

fig.add_trace(
    go.Scatter(x=combined_df["Date"], y=combined_df["FEDFUNDS"], name="Fed Rate"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=combined_df["Date"], y=combined_df["SP500"], name="S&P 500"),
    secondary_y=True,
)

fig.update_yaxes(title_text="Federal Funds Rate (%)", secondary_y=False)
fig.update_yaxes(title_text="S&P 500 Index", secondary_y=True)

fig.update_layout(title_text="Fed Rate vs S&P 500")
fig.show()
