1. 請使用 docker-compose 建立一個包含下列服務的開發環境：
    a. Django：使用v5.2，並能啟動開發伺服器。
        i. 其餘需要安裝的相關依賴請參考附件requirements.txt
2. PostgreSQL：使用v14 作為 Django 的資料庫。
3. Redis：使用v7.4.2 作為快取使用。
4. 環境變數管理：所有機敏資訊（如 DB 密碼）需透過 .env 檔設定，並於 compose 中載入。
    a. 請將.env排除於git的管理之外，並且使用git-secret進行加密，將自己與pony加入可以解密的名單中
    b. pony public key在附檔中
5. 網路隔離：Redis 與 PostgreSQL 不能對外暴露埠，三個服務需透過自訂 bridge network 溝通。
6. 檔案同步：能夠在本機修改 Django 專案的程式碼並即時反映到容器中。
7. 確認 Django 能正確連接到 PostgreSQL 與 Redis。
    a. 你會需要修改django settings.py中的部分設定，範例連線的代碼請見附件
8. 連線成功後可以進到django的container中初始化DB
    a. 執行python manage.py migrate完成DB的初次migration