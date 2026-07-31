import os
import requests
from supabase import create_client

# 從 GitHub Secrets 讀取連線資訊
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ 錯誤：未設定 SUPABASE_URL 或 SUPABASE_KEY")
    exit(1)

supabase = create_client(supabase_url, supabase_key)

print("🚀 開始抓取台灣 TFDA 藥品資料...")

try:
    # 抓取台灣 TFDA 西藥許可證開放資料 API (範例)
    url = "https://data.fda.gov.tw/opendata/export/1/JSON"
    response = requests.get(url, timeout=30)
    data = response.json()

    print(f"📦 成功讀取 {len(data)} 筆資料，準備寫入 Supabase...")

    # 取前 20 筆作為測試寫入
    for item in data[:20]:
        payload = {
            "country": "台灣",
            "brand_name": item.get("中文品名") or item.get("英文品名"),
            "active_ingredient": item.get("有效成分"),
            "dosage_form": item.get("劑型"),
            "strength": item.get("含量"),
            "licence_status": item.get("通關簽審狀態") or "有效",
            "official_url": "https://www.fda.gov.tw"
        }
        
        # 寫入或更新 Supabase 的 drug_approvals 資料表
        supabase.table("drug_approvals").upsert(payload).execute()

    print("✅ 資料處理與寫入完成！")

except Exception as e:
    print(f"❌ 執行過程中發生錯誤: {e}")
