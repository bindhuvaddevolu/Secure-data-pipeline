
import time
import json
import tracemalloc
from pathlib import Path

from src.data_generator import generate_dataset
from src.validation import validate_data
from src.masking import get_secret_key, apply_privacy_transformations
from src.minimization import minimize_data
from src.publishing import publish_data


def run_performance_test():
    root = Path(__file__).resolve().parent.parent

    # Start memory monitoring
    tracemalloc.start()

    print("Generating 100,000 records...")
    start = time.perf_counter()

    df, _ = generate_dataset(
        num_records=100_000,
        seed=42,
        include_edge_cases=False
    )

    generation_time = time.perf_counter() - start

    print("Validating records...")
    start = time.perf_counter()

    valid_df, rejected_df, report = validate_data(df)

    validation_time = time.perf_counter() - start

    print("Applying privacy transformations...")
    start = time.perf_counter()

    masked_df = apply_privacy_transformations(
        df=valid_df,
        secret_key=get_secret_key()
    )

    masking_time = time.perf_counter() - start

    print("Minimizing data...")
    start = time.perf_counter()

    analytical_df = minimize_data(masked_df)

    minimization_time = time.perf_counter() - start

    print("Publishing to SQLite...")
    start = time.perf_counter()

    database = root / "data" / "output" / "performance.db"
    published_count = publish_data(analytical_df, database)

    publishing_time = time.perf_counter() - start

    total_time = (
        generation_time
        + validation_time
        + masking_time
        + minimization_time
        + publishing_time
    )

    # Get peak Python-tracked memory usage
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_memory_mb = peak_memory / (1024 * 1024)

    # Calculate processing throughput
    throughput = (
        len(df) / total_time if total_time > 0 else 0
    )

    print("\n========== PERFORMANCE REPORT ==========")
    print(f"Generated records: {len(df)}")
    print(f"Valid records: {len(valid_df)}")
    print(f"Rejected records: {len(rejected_df)}")
    print(f"Published records: {published_count}")

    print("\nExecution Times:")
    print(f"Generation: {generation_time:.2f} seconds")
    print(f"Validation: {validation_time:.2f} seconds")
    print(f"Masking: {masking_time:.2f} seconds")
    print(f"Minimization: {minimization_time:.2f} seconds")
    print(f"Publishing: {publishing_time:.2f} seconds")
    print(f"Total time: {total_time:.2f} seconds")

    print("\nResource Metrics:")
    print(f"Peak Python-tracked memory: {peak_memory_mb:.2f} MB")
    print(f"Processing throughput: {throughput:.2f} records/second")

    performance_report = {
        "generated_records": len(df),
        "valid_records": len(valid_df),
        "rejected_records": len(rejected_df),
        "published_records": published_count,
        "generation_time_seconds": round(generation_time, 2),
        "validation_time_seconds": round(validation_time, 2),
        "masking_time_seconds": round(masking_time, 2),
        "minimization_time_seconds": round(minimization_time, 2),
        "publishing_time_seconds": round(publishing_time, 2),
        "total_time_seconds": round(total_time, 2),
        "peak_python_memory_mb": round(peak_memory_mb, 2),
        "throughput_records_per_second": round(throughput, 2)
    }

    report_path = root / "reports" / "performance_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(performance_report, file, indent=4)

    print(f"\nPerformance report saved: {report_path}")


if __name__ == "__main__":
    run_performance_test()
