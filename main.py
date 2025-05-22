from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/stock")
def get_stock(ticker: str):
    try:
        data = yf.download(ticker, period="7d", interval="1d", progress=False)
        latest = data.tail(1).reset_index()
        row = latest.iloc[0]

        return {
            "Ticker": ticker,
            "Date": str(row["Date"]),
            "Open": round(row["Open"], 2),
            "High": round(row["High"], 2),
            "Low": round(row["Low"], 2),
            "Close": round(row["Close"], 2),
            "Volume": int(row["Volume"])
        }
    except Exception as e:
        return {"error": str(e)}
