import pandas as pd

def average_memory(filepath):
    # Đọc file với tên cột phù hợp
    df = pd.read_csv(filepath, header=None, names=["timestamp", "execs", "edges", "execs_per_s", "mem"])
    return df["mem"].mean()

def main():
    # Danh sách các file log và nhãn tương ứng
    log_files = ["pythonfuzz.txt", "dqn.txt", "ppo.txt", "grpo.txt"]
    labels = ["Pythonfuzz", "DQN_fuzz", "Rainfuzz_mod", "GRFuzz"]

    print("Average memory consumption (MB):\n")

    for file, label in zip(log_files, labels):
        try:
            avg_mem = average_memory(file)
            print(f"{label:15}: {avg_mem:.2f}")
        except Exception as e:
            print(f"{label:15}: Error reading {file} - {e}")

if __name__ == "__main__":
    main()
