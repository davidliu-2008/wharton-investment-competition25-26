from pathlib import Path
import time

import yfinance as yf

#TICKERS = [
#    "ASML", "BEP", "CSCO", "CWEN", "EBS", "EVO", "EVTC", "FSLR",
#    "GOOG", "JNJ", "KO", "LYFT", "MRK", "NEE", "NVDA", "STX",
#    "TSM", "WMT",
#]

TICKERS = [
    "LYFT", "AGG", "BND", "BNDX", "DGRO", "ESGD", "ESGV", "PAVE",
    "QUAL", "SCHD", "USMV", "VCIT", "VEU", "VIG", "VTV", "XLU",
    "XLP",
]

START = "2020-01-01"
END = None  # set to e.g. "2025-01-01" for a fixed end (Yahoo end is exclusive)
OUT_DIR = Path("data")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def download_one(ticker: str, retries: int = 1):
    for attempt in range(retries + 1):
        df = yf.download(
            ticker,
            start=START,
            end=END,
            auto_adjust=True,
            progress=False,
            threads=False,
        )
        if not df.empty:
            return df
        if attempt < retries:
            time.sleep(1)
    return df


def main():
    for ticker in TICKERS:
        df = download_one(ticker)
        if df.empty:
            print(f"{ticker}: failed (no data)")
            continue
        out_path = OUT_DIR / f"{ticker}.csv"
        df.to_csv(out_path, index=True)
        print(f"{ticker}: saved {len(df)} rows -> {out_path}")


if __name__ == "__main__":
    main()
