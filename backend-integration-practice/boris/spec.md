# 購物車後端API專案挑戰
## 專案目標
建立一個完整的購物車後端API系統，提供用戶認證、商品管理、購物車操作和訂單處理等RESTful API服務。
## 技術要求
*   **主框架**: Django + Django REST Framework
*   **認證**: JWT Token
*   **快取**: Redis
*   **資料庫**: PostgreSQL
*   **異步任務**: Celery
*   Message Queue: RabbitMQ
## 核心功能需求
### 1\. 用戶系統
*   提供用戶註冊API
*   提供用戶登入API並返回JWT Token
*   提供查看及更新個人資料API
*   提供Token刷新API
**提示**: 使用 `djangorestframework-simplejwt` 套件
### 2\. 商品系統
*   提供商品列表API
*   提供商品詳細資料API
*   支援基本的過濾功能
**快取挑戰**: 將商品列表快取到Redis中，提升查詢效能
### 3\. 購物車系統
*   提供加入商品到購物車API
*   提供查看購物車內容API (需包含總金額)
*   提供修改商品數量API
*   提供移除商品API
**快取挑戰**: 將購物車資料存放在Redis中
### 4\. 訂單系統
*   提供建立訂單API (從購物車建立)
*   提供查看訂單列表API
*   提供查看訂單詳情API
*   提供取消訂單API
**異步任務挑戰**: 使用Celery定期生成銷售統計報表
## 資料模型設計挑戰
請自行設計所需的資料模型，思考各模型之間的關聯性。
## API端點規劃
請設計RESTful API架構，規劃適當的端點和HTTP方法。
## 進階挑戰
### 快取策略
*   商品列表快取
### 異步任務
*   定期統計報表生成
### 效能優化
*   減少不必要的資料庫查詢
*   適當使用資料庫索引
## 學習目標
完成這個專案後，你將學會:
1. Django REST Framework的完整應用
2. JWT認證機制的實作
3. Redis快取的基本應用
4. Celery異步任務的基本應用
5. RESTful API設計原則
## 開發建議
1. 先從基本的CRUD API開始
2. 逐步加入JWT認證功能
3. 再整合Redis快取和Celery異步任務
4. 最後進行API測試 (可使用Postman或類似工具)
祝你開發順利！記住，遇到問題時要善用Django和DRF的官方文檔。可以使用Postman、curl或其他API測試工具來驗證你的API功能。
###   

## 備註 :
1. 先整體了解什麼是後端
2. 了解資料庫，快取的作用
3. 了解如何設計一個符合需求的資料庫
    1. 練習使用MERMAID先畫出ERD，確認資料表的結構再實作
4. 學習Django
    1. 了解如何將Django連線到資料庫, 快取, 訊息佇列等服務
    2. 了解如何把ERD的規劃實際寫成models
    3. 了解Django如何與實際資料庫進行同步
    4. 了解ORM怎麼使用
    5. 了解如何routing url到指定的function
    6. 了解如何做基本的CRUD
    7. 了解如何回傳資料
5. 學習DRF
    1. 了解什麼是api\_view
    2. (重要)了解什麼是ViewSet, Serializer, 以及各種mixin
6. 學習快取(Redis)
    1. 了解如何設置快取
    2. 了解如何將資料從快取中取出
    3. 了解如何設置過期時間
    4. 了解如何設置fallback策略