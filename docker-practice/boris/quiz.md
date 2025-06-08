1. 請撰寫一個 Dockerfile 來建立一個 Docker 映像與容器，並實現以下需求：
    a. 在容器中安裝 Django 5.2 及其相關依賴。
        i. 相關依賴請參考requirements.txt
    b. 支援本機與容器的檔案同步（即修改本地檔案時，容器內會同步更新）。
    c. 啟動一個 Django 開發伺服器。
    d. 本機可以透過 localhost 連線至容器中的 Django 服務。