# Hướng dẫn sử dụng công cụ kiểm thử

Dưới đây là hướng dẫn chạy các chế độ và cách thu thập, biểu diễn kết quả.

## Mục lục
- [Cấu trúc mã nguồn](#cấu-trúc-mã-nguồn)
- [0. Chuẩn bị](#0-chuẩn-bị)
- [1. Kiểm thử đơn tiến trình](#1-kiểm-thử-đơn-tiến-trình)
- [2. Kiểm thử hai tiến trình](#2-kiểm-thử-hai-tiến-trình)
- [3. Công bố khoa học](#3-công-bố-khoa-học)
- [Trích dẫn](#trích-dẫn)

---

## Cấu trúc mã nguồn

Mã nguồn gồm các thư mục nhằm những mục đích khác nhau.

Các thư mục
```pythonfuzz```, ```pythonfuzz_with_dqn```, ```pythonfuzz_with_ppo```, ```pythonfuzz_with_grpo``` chứa mã nguồn của các kịch bản thực nghiệm đơn tiến trình.

Các thư mục với tiền tố ```colabmode_``` chứa mã nguồn của các kịch bản thực nghiệm hai tiến trình.

Thư mục ```experiment_results``` chứa các tệp phân tích, bao gồm tính tốc độ thực thi trung bình, bộ nhớ tiêu thụ trung bình và biểu diễn độ bao phủ theo thời gian thành đồ thị.

Thư mục ```targets``` chứa các chương trình mục tiêu. Các tệp trong thư mục này có dạng ```libraryName_fuzz```, trong đó ```libraryName``` là thư viện cần kiểm thử.

## 0. Chuẩn bị

Trước khi kiểm thử, đảm bảo thư viện cần kiểm thử đã được cài đặt.

```bash
pip/pip3 install libraryName
```

Tạo một tệp chương trình mục tiêu để kiểm thử, đặt tên là ```libraryName_fuzz.py```.

Sao chép thư mục ```targets``` vào thư mục chứa kịch bản cần chạy.

Xóa tệp nhật ký ```libraryName_log.py``` trong thư mục kịch bản nếu tồn tại.

---

## 1. Kiểm thử đơn tiến trình

Chế độ này dành cho việc chạy kiểm thử bằng một tiến trình duy nhất.

Giả sử kịch bản cần kiểm thử tên ```scenario```.

### Bước thực hiện:

```bash
cd scenario
python/python3 main.py libraryName_fuzz
```

Có thể thêm ```timeout``` để kiểm thử trong thời gian xác định.

Ví dụ, nếu cần kiểm thử trong một ngày, thực hiện lệnh 

```bash
timeout 86400s python/python3 main.py libraryName_fuzz
```

Tệp nhật ký được ghi trong ```libraryName_log.txt```.

Sao chép tệp này vào thư mục ```experiment_results``` để xử lý kết quả.

## 2. Kiểm thử hai tiến trình

Chế độ này dành cho việc chạy kiểm thử kết hợp hai tiến trình.

Giả sử ta chạy song song ```colabmode_scenario_1``` và ```colabmode_scenario_2```.

### Bước thực hiện:

Bật terminal 1:

```bash
cd colabmode_scenario_1
python/python3 main.py libraryName_fuzz ../shared_seeds_queue
```

Bật terminal 2:

```bash
cd colabmode_scenario_2
python/python3 main.py libraryName_fuzz ../shared_seeds_queue
```

Các bước xử lý kết quả thực hiện tương tự [Kiểm thử đơn tiến trình](#1-kiểm-thử-đơn-tiến-trình), trong đó tệp được xử lý sẽ lấy từ tiến trình thu được độ bao phủ cuối cùng cao nhất.

Ta cũng có thể sử dụng ```timeout``` để giới hạn thời gian kiểm thử.

## 3. Công bố khoa học

```GRFuzz``` được công bố trong hội nghị IEEE IRI 2025.

## Trích dẫn
