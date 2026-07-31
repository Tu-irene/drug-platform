import os
import requests
from supabase import create_client

# 讀取金鑰
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ 錯誤：未設定 SUPABASE_URL 或 SUPABASE_KEY")
    exit(1)

supabase = create_client(supabase_url, supabase_key)

print("🚀 開始抓取台灣 TFDA 藥品資料...")

# 模擬一般 Chrome 瀏覽器標頭，避免被政府 API 拒絕 (HTTP 403)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 台灣 TFDA 西藥許可證基本資料 API
url = "https://data.fda.gov.tw/opendata/export/1/JSON"

try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"📡 API 回應 HTTP 狀態碼: {response.status_code}")
    
    # 檢查是否請求成功
    response.raise_for_status()
    
    data = response.json()
    print(f"📦 成功讀取 {len(data)} 筆資料，準備寫入 Supabase...")

    records = []
    # 取前 20 筆進行寫入測試
    for item in data[:20]:
        records.append({
            "country": "台灣",
            "brand_name": item.get("中文品名") or item.get("英文品name") or item.get("英文品名") or "未命名藥品",
            "active_ingredient": item.get("有效成分") or item.get("主成分") or "詳仿單",
            "dosage_form": item.get("劑型") or "未標示",
            "strength": item.get("含量") or "未標示",
            "licence_status": item.get("通關簽審狀態") or item.get("許可證字號") or "有效",
            "official_url": "https://www.fda.gov.tw"
        })
    
    # 寫入 Supabase
    res = supabase.table("drug_approvals").insert(records).execute()
    print("✅ 成功寫入 Supabase 資料庫！")

except Exception as e:
    print(f"❌ 執行過程中發生錯誤: {e}")
