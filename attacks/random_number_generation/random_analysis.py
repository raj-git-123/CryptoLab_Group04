import os
import math
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
from scipy.stats import chisquare, norm


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")

SIGNIFICANCE_LEVEL = 0.01

DATASETS = {
    "Linux /dev/urandom": "linux_urandom.bin",
    "OpenSSL": "openssl_rand.bin",
    "Windows CNG": "windows_cng.bin"
}


def load_data(filename):
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Generate the random data before running the analysis."
        )

    data = np.fromfile(path, dtype=np.uint8)

    if len(data) == 0:
        raise ValueError(f"Dataset is empty: {path}")

    return data


def byte_frequency(data):
    counts = np.bincount(data, minlength=256)

    expected = len(data) / 256

    statistic, p_value = chisquare(
        counts,
        f_exp=np.full(256, expected)
    )

    return counts, statistic, p_value


def bit_frequency(data):
    bits = np.unpackbits(data)

    ones = int(np.sum(bits))
    zeros = len(bits) - ones

    proportion_ones = ones / len(bits)

    statistic, p_value = chisquare(
        [zeros, ones],
        f_exp=[len(bits) / 2, len(bits) / 2]
    )

    return bits, zeros, ones, proportion_ones, statistic, p_value


def monobit_test(bits):
    n = len(bits)

    ones = int(np.sum(bits))
    zeros = n - ones

    s = ones - zeros

    s_obs = abs(s) / math.sqrt(n)

    p_value = math.erfc(s_obs / math.sqrt(2))

    return s, s_obs, p_value


def runs_test(bits):
    n = len(bits)

    ones = int(np.sum(bits))
    pi = ones / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return None, None, False

    runs = 1 + int(np.sum(bits[1:] != bits[:-1]))

    expected_runs = 2 * n * pi * (1 - pi)

    standard_deviation = (
        2 * math.sqrt(2 * n) * pi * (1 - pi)
    )

    z = abs(runs - expected_runs) / standard_deviation

    p_value = math.erfc(z / math.sqrt(2))

    return runs, p_value, True


def serial_correlation(data):
    if len(data) < 2:
        return float("nan")

    x = data[:-1].astype(np.float64)
    y = data[1:].astype(np.float64)

    correlation = np.corrcoef(x, y)[0, 1]

    return float(correlation)


def repeated_patterns(data, pattern_length):
    patterns = Counter(
        data[i:i + pattern_length].tobytes()
        for i in range(len(data) - pattern_length + 1)
    )

    distinct_repeated = sum(
        count > 1 for count in patterns.values()
    )

    extra_occurrences = sum(
        count - 1 for count in patterns.values()
        if count > 1
    )

    maximum_frequency = max(patterns.values())

    return distinct_repeated, extra_occurrences, maximum_frequency


def shannon_entropy(data):
    counts = np.bincount(data, minlength=256)

    probabilities = counts[counts > 0] / len(data)

    entropy = -np.sum(
        probabilities * np.log2(probabilities)
    )

    return float(entropy)


def analyze_dataset(name, filename):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    data = load_data(filename)

    print(f"Dataset size: {len(data):,} bytes")

    counts, chi_stat, chi_p = byte_frequency(data)

    print("\nBYTE-FREQUENCY ANALYSIS")
    print(f"Expected frequency per byte: {len(data) / 256:.2f}")
    print(f"Chi-square statistic: {chi_stat:.4f}")
    print(f"Chi-square p-value: {chi_p:.8f}")

    bits, zeros, ones, proportion, bit_stat, bit_p = (
        bit_frequency(data)
    )

    print("\nBIT-FREQUENCY ANALYSIS")
    print(f"Number of zeros: {zeros:,}")
    print(f"Number of ones: {ones:,}")
    print(f"Proportion of ones: {proportion:.8f}")
    print(f"Bit-frequency chi-square: {bit_stat:.4f}")
    print(f"Bit-frequency p-value: {bit_p:.8f}")

    s, s_obs, mono_p = monobit_test(bits)

    print("\nMONOBIT TEST")
    print(f"S_n: {s}")
    print(f"Normalized statistic: {s_obs:.8f}")
    print(f"Monobit p-value: {mono_p:.8f}")

    runs, runs_p, applicable = runs_test(bits)

    print("\nRUNS TEST")

    if applicable:
        print(f"Number of runs: {runs}")
        print(f"Runs-test p-value: {runs_p:.8f}")
    else:
        print("Test not applicable: bit proportion is too far from 0.5.")
        runs_p = float("nan")

    correlation = serial_correlation(data)

    print("\nSERIAL CORRELATION")
    print(f"Adjacent-byte correlation: {correlation:.10f}")

    print("\nREPEATED-PATTERN ANALYSIS")

    repeated_results = {}

    for length in [2, 3, 4]:
        distinct, extra, maximum = repeated_patterns(
            data, length
        )

        repeated_results[length] = distinct

        print(f"{length}-byte patterns:")
        print(f"  Distinct repeated patterns: {distinct:,}")
        print(f"  Extra occurrences: {extra:,}")
        print(f"  Maximum pattern frequency: {maximum:,}")

    entropy = shannon_entropy(data)

    print("\nSHANNON ENTROPY")
    print(f"Entropy: {entropy:.8f} bits/byte")
    print(f"Maximum possible: 8 bits/byte")

    results = {
        "name": name,
        "size": len(data),
        "byte_chi_p": chi_p,
        "bit_chi_p": bit_p,
        "monobit_p": mono_p,
        "runs_p": runs_p,
        "correlation": correlation,
        "entropy": entropy,
        "repeated_2": repeated_results[2],
        "repeated_3": repeated_results[3],
        "repeated_4": repeated_results[4],
        "byte_counts": counts,
        "proportion_ones": proportion
    }

    return results


def plot_byte_frequencies(results):
    plt.figure(figsize=(14, 6))

    for result in results:
        counts = result["byte_counts"]

        plt.plot(
            range(256),
            counts,
            linewidth=1,
            label=result["name"]
        )

    plt.axhline(
        y=results[0]["size"] / 256,
        linestyle="--",
        label="Expected frequency"
    )

    plt.xlabel("Byte value")
    plt.ylabel("Frequency")
    plt.title("Byte-Frequency Distribution")
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        RESULTS_DIR, "byte_frequency.png"
    )

    plt.savefig(path, dpi=300)
    plt.close()

    print(f"\nSaved plot: {path}")


def plot_bit_distribution(results):
    names = [r["name"] for r in results]

    proportions = [
        r["proportion_ones"] for r in results
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(names, proportions)

    plt.axhline(
        y=0.5,
        linestyle="--",
        label="Expected proportion"
    )

    plt.ylabel("Proportion of 1-bits")
    plt.title("Bit-Frequency Comparison")
    plt.ylim(0.49, 0.51)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(
        RESULTS_DIR, "bit_distribution.png"
    )

    plt.savefig(path, dpi=300)
    plt.close()

    print(f"Saved plot: {path}")


def plot_serial_correlation(results):
    names = [r["name"] for r in results]

    correlations = [
        r["correlation"] for r in results
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(names, correlations)

    plt.axhline(
        y=0,
        linestyle="--"
    )

    plt.ylabel("Correlation coefficient")
    plt.title("Serial Correlation Comparison")
    plt.tight_layout()

    path = os.path.join(
        RESULTS_DIR, "serial_correlation.png"
    )

    plt.savefig(path, dpi=300)
    plt.close()

    print(f"Saved plot: {path}")


def print_comparison(results):
    print("\n" + "=" * 100)
    print("COMPARATIVE RESULTS")
    print("=" * 100)

    headers = [
        "Generator",
        "Byte p-value",
        "Bit p-value",
        "Monobit p",
        "Runs p",
        "Correlation",
        "Entropy"
    ]

    print(
        f"{headers[0]:<22}"
        f"{headers[1]:>14}"
        f"{headers[2]:>14}"
        f"{headers[3]:>14}"
        f"{headers[4]:>14}"
        f"{headers[5]:>16}"
        f"{headers[6]:>12}"
    )

    for r in results:
        print(
            f"{r['name']:<22}"
            f"{r['byte_chi_p']:>14.6f}"
            f"{r['bit_chi_p']:>14.6f}"
            f"{r['monobit_p']:>14.6f}"
            f"{r['runs_p']:>14.6f}"
            f"{r['correlation']:>16.8f}"
            f"{r['entropy']:>12.6f}"
        )


def interpret_results(results):
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)

    alpha = SIGNIFICANCE_LEVEL

    for r in results:
        print(f"\n{r['name']}:")

        tests = {
            "Byte-frequency test": r["byte_chi_p"],
            "Bit-frequency test": r["bit_chi_p"],
            "Monobit test": r["monobit_p"],
            "Runs test": r["runs_p"]
        }

        for test_name, p_value in tests.items():
            if np.isnan(p_value):
                print(f"  {test_name}: Not applicable")
            elif p_value < alpha:
                print(
                    f"  {test_name}: Reject null hypothesis "
                    f"(p = {p_value:.6f})"
                )
            else:
                print(
                    f"  {test_name}: Fail to reject null hypothesis "
                    f"(p = {p_value:.6f})"
                )

        print(
            f"  Serial correlation: {r['correlation']:.8f}"
        )

        print(
            f"  Shannon entropy: {r['entropy']:.6f} bits/byte"
        )

    print("\nIMPORTANT:")
    print(
        "Passing statistical tests does not prove "
        "cryptographic security."
    )


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    results = []

    for name, filename in DATASETS.items():
        result = analyze_dataset(name, filename)
        results.append(result)

    plot_byte_frequencies(results)
    plot_bit_distribution(results)
    plot_serial_correlation(results)

    print_comparison(results)
    interpret_results(results)


if __name__ == "__main__":
    main()
