import pandas as pd
import requests # should use httpx instead


class QueryResult:
    def __init__(self, json: dict):
        self.json = json

    @property
    def df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.json["data"]["data"])
        df["produced_at"] = pd.to_datetime(df["produced_at"])
        return df


class QueryClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def query(
        self,
        signals: list[str],
        vehicle_id: str,
        trip_id: str | int | None = None,
        start: str | None = None,
        end: str | None = None,
        merge: str = "smallest",
        fill: str = "none",
        tolerance: int = 50,
        export: str = "json",
    ):
        params = {
            "token": self.token,
            "vehicle_id": vehicle_id,
            "signals": ",".join(signals),
            "merge": merge,
            "fill": fill,
            "tolerance": tolerance,
            "export": export,
        }
        if trip_id is not None:
            params["trip_id"] = str(trip_id)
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end

        resp = requests.get(f"{self.base_url}/query/signals", params=params)
        resp.raise_for_status()
        return QueryResult(resp.json())
