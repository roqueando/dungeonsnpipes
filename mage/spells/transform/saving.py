import pyarrow.parquet as pq
import pyarrow as pa


def save_to_parquet(batch: list) -> None:
    table = pa.Table.from_batches(batch)
    print(table)
