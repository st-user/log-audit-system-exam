# プログラミング問題

## 実行環境

 - python3 (推奨 3.9以上)

## 実行方法

### 事前準備

```bash
python -m venv venv
source ./venv/bin/activate
```


### 設問1

```bash
FILE_PATH=./sample_files/question_1.txt
python question_1_and_2.py ${FILE_PATH}
```
[テストデータと結果](./tests/Question_1.md)

### 設問2

```bash
FILE_PATH=./sample_files/question_2.txt
python question_1_and_2.py -n 2 ${FILE_PATH}
```

[テストデータと結果](./tests/Question_2.md)

### 設問3

```bash
FILE_PATH=./sample_files/question_3.txt
python question_3.py -m 3 -t 10 ${FILE_PATH}
```

[テストデータと結果](./tests/Question_3.md)

### 設問4

```bash
FILE_PATH=./sample_files/question_4.txt
python question_4.py -n 2 ${FILE_PATH}
```

[テストデータと結果](./tests/Question_4.md)