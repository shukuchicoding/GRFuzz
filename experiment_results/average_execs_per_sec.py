import pandas as pd

def average_execs_per_sec(filepath, duration_seconds=21600):
    # Đọc file, cột thứ 2 là số executions tích lũy
    df = pd.read_csv(filepath, header=None, names=["timestamp", "execs", "edges", "execs_per_s", "mem"])
    total_execs = df["execs"].max()  # lấy tổng executions cuối cùng
    return total_execs / duration_seconds

def main():
    # Danh sách file và nhãn tương ứng
    log_files = ["pythonfuzz.txt", "dqn.txt", "ppo.txt", "grpo.txt"]
    labels = ["Pythonfuzz", "DQN_fuzz", "Rainfuzz_mod", "GRFuzz"]

    print("Average execs/s over 6 hours (21600 seconds):\n")

    for file, label in zip(log_files, labels):
        try:
            avg_execs = average_execs_per_sec(file)
            print(f"{label:15}: {avg_execs:.2f} execs/s")
        except Exception as e:
            print(f"{label:15}: Error reading {file} - {e}")

if __name__ == "__main__":
    main()
