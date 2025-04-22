### 常用 Git 語法

- 查看當前狀態：
    ```bash
    git status
    ```

- 切換分支：
    ```bash
    git checkout <你要的branch>
    ```
    例如：`git checkout feature/home_page`

- 將修改的文件添加到暫存區：
    ```bash
    git add .
    ```

- 提交修改：
    ```bash
    git commit -m "自己打"
    ```

- 從遠端拉取最新變更：
    ```bash
    git pull origin <分支名稱>
    ```
    例如：`git pull origin main`

- 推送本地修改到遠端分支：
    ```bash
    git push origin <你要推送的分支>
    ```

- 創建並切換到新分支：
    ```bash
    git checkout -b <新分支名稱>
    ```
### 1. 克隆專案

首先，從 GitHub 克隆專案到本地端：

```bash
git clone https://github.com/sdsfvvbn/final-project
```

### 2. 創建虛擬環境

進入專案資料夾：

```bash
cd Project
```

創建虛擬環境：

```bash
python -m venv django-venv
```

### 3. 啟動虛擬環境

- **Windows 使用者** 啟動虛擬環境：

```bash
.\venv\Scripts\activate
```

- **Mac/Linux 使用者** 啟動虛擬環境：

```bash
source venv/bin/activate
```

### 4. 安裝依賴項目

安裝所有專案所需的依賴包：

```bash
pip install -r requirements.txt
```

### 5. 遷移資料庫

如果專案有資料庫，執行以下指令進行資料庫遷移：

```bash
python manage.py migrate
```

### 6. 啟動開發伺服器

啟動 Django 開發伺服器，並在瀏覽器中訪問：

```bash
python manage.py runserver
```

預設會在 [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 運行。

