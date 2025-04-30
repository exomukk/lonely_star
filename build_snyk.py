import os
import re
import subprocess
import json


def print_logo():
    # In logo ASCII
    logo = """                           
 _____                        _   
|   __| _ _  ___  _____  _ _ | |_ 
|   __||_'_|| . ||     || | || '_| 
|_____||_,_||___||_|_|_||___||_,_|                   
    """
    print(logo)


def run_snyk_scan():
    snyk_token = input("Nhập Snyk API Token của bạn: ")

    # Lưu token vào biến môi trường
    os.environ["SNYK_TOKEN"] = snyk_token
    print("Token đã được lưu vào biến môi trường.\n")
    print("Đang quét mã nguồn bằng Snyk...\n")

    try:
        # Chạy Docker build với biến môi trường SNYK_TOKEN
        result = subprocess.run(
            ["docker", "build", "--build-arg", f"SNYK_TOKEN={snyk_token}", "-t", "snyk-flask-dashboard", "."],
            text=True, capture_output=True, encoding='utf-8', errors='replace'  # Sử dụng utf-8 và errors='replace'
        )

        # Kiểm tra stderr
        # if result.stderr:
        #     print("Error in stderr:", result.stderr)

        # Lọc kết quả #12 trong stderr nếu có
        if result.stderr:  # Chỉ thực hiện splitlines nếu stderr có dữ liệu
            filtered_result = []
            for line in result.stderr.splitlines():
                if "#12" in line:
                    cleaned_line = re.sub(r'^#\d+\s+\d+\.\d+\s+', '', line)
                    filtered_result.append(cleaned_line)
                # if filtered_result:
                # print("Filtered output from stderr:")
                # print("\n".join(filtered_result))
            docker_output = "\n".join(filtered_result)

            cleaned_output = re.sub(r'^#\d+\s+\d+\.\d+\s+', '', docker_output)

            print('cleaned_output: ', cleaned_output)

            # Tìm kiếm phần JSON trong output (bắt đầu từ '{' và kết thúc ở '}')
            json_match = re.search(r'({.*})', cleaned_output, re.DOTALL)  # Dùng result.stdout thay vì result
            # json_match_err = re.search(r'({.*})', cleaned_output, re.DOTALL)

            # if json_match_err:
            #     # json_data = json_match.group(0)  # Lấy phần JSON từ output
            #
            #     # Chuyển đổi chuỗi JSON thành đối tượng Python
            #     result_json = json.loads(json_match_err.group(1))
            #     with open('snyk_results.json', 'w') as json_file:
            #         json.dump(result_json, json_file, indent=2)
            #
            #     with open("docker_build_result.txt", "w", encoding="utf-8") as file:
            #         file.write("\n".join(result_json))
            #
            #     print('Result JSON: ', result_json)

            if json_match:
                try:
                    # Load the matched JSON string into a dictionary
                    json_data = json.loads(json_match.group(1))

                    # Save the extracted JSON to a file
                    with open('snyk_results.json', 'w') as json_file:
                        json.dump(json_data, json_file, indent=2)

                    print("JSON content extracted and saved to 'snyk_results.json'")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

        # Hiển thị thông tin quá trình build
        print("Docker image đã được build thành công!")
        print("Docker image đã được gắn thẻ là 'snyk-flask-dashboard'.\n")

        #
        #     # Ghi kết quả lọc vào file txt
        #     with open("docker_build_result.txt", "w", encoding="utf-8") as file:
        #         file.write("\n".join(filtered_result))  # Ghi kết quả vào file

        # # Ghi kết quả JSON vào file json
        # if 'result_json' in locals():  # Kiểm tra nếu result_json đã được tạo
        #     with open("snyk_results.json", "w", encoding="utf-8") as json_file:
        #         json.dump(result_json, json_file, ensure_ascii=False, indent=4)  # Ghi file JSON

    except subprocess.CalledProcessError as e:
        # Xử lý lỗi nếu build Docker thất bại
        print("Lỗi khi build Docker image:")
        print(e.stderr)  # In lỗi stderr để người dùng dễ dàng hiểu nguyên nhân

    except UnicodeDecodeError as e:
        print("Lỗi mã hóa ký tự:")
        print(e)  # In lỗi mã hóa ký tự, có thể thử thêm một số mã hóa khác

    except Exception as e:
        # Xử lý bất kỳ lỗi không mong muốn nào
        print("Đã xảy ra lỗi ngoài dự đoán:")
        print(str(e))

    # Cung cấp hướng dẫn tiếp theo
    print("\nNếu không có lỗi, bạn có thể tiếp tục với các bước sau:")
    print("1. Chạy Docker container: docker run -p 8080:8080 snyk-flask-dashboard")
    print("2. Truy cập vào dashboard web tại http://localhost:5000")
    choice = input("Nhập lựa chọn của bạn:")

    if choice == "1":
        print_logo()

    elif choice == "2":
        subprocess.run(["python", "snyk.py"])


def check_docker_image():
    print("Kiểm tra bảo mật Docker Image...\n")
    docker_image = input("Nhập tên Docker image bạn muốn kiểm tra (ví dụ: my_image:latest): ")

    snyk_token = input("Nhập Snyk API Token của bạn: ")

    # Lưu token vào biến môi trường
    os.environ["SNYK_TOKEN"] = snyk_token
    print("Token đã được lưu vào biến môi trường.\n")

    try:
        # Chạy lệnh Snyk để kiểm tra bảo mật trong Docker image
        result = subprocess.run(
            ["snyk", "container", "test", docker_image, "--json"],
            text=True, capture_output=True, encoding='utf-8', errors='replace'
        )

        # Lọc và xử lý kết quả
        if result.stderr:
            filtered_result = []
            for line in result.stderr.splitlines():
                if "#12" in line:
                    cleaned_line = re.sub(r'^#\d+\s+\d+\.\d+\s+', '', line)
                    filtered_result.append(cleaned_line)

            docker_output = "\n".join(filtered_result)

            # Xử lý phần JSON từ output
            json_match = re.search(r'({.*})', docker_output, re.DOTALL)
            if json_match:
                try:
                    json_data = json.loads(json_match.group(1))

                    # Lưu kết quả vào file
                    with open('docker_scan_results.json', 'w') as json_file:
                        json.dump(json_data, json_file, indent=2)

                    print("Docker image scan results saved to 'docker_scan_results.json'")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

    except subprocess.CalledProcessError as e:
        print("Lỗi khi kiểm tra Docker image:")
        print(e.stderr)

    except Exception as e:
        print("Đã xảy ra lỗi ngoài dự đoán:")
        print(str(e))


def main():
    print_logo()
    print("Chào mừng bạn đến với công cụ tự động hóa Docker và Snyk!")
    print("Chọn một trong hai lựa chọn sau:")
    print("1. Đọc lỗi mã nguồn (Snyk)")
    print("2. Kiểm tra bảo mật Docker image")

    choice = input("Nhập lựa chọn (1 hoặc 2): ")

    if choice == '1':
        run_snyk_scan()
    elif choice == '2':
        check_docker_image()
    else:
        print("Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    main()
