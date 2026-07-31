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

try:
    url = "https://data.fda.gov.tw/opendata/export/1/JSON"
    response = requests.get(url, timeout=30)
    data = response.json()

    print(f"📦 成功讀取 {len(data)} 筆資料，準備寫入 Supabase...")

    # 取前 20 筆資料寫入
    records = []
    for item in data[:20]:
        records.append({
            "country": "台灣",
            "brand_name": item.get("中文品名") or item.get("英文品名") or "未命名",
            "active_ingredient": item.get("有效成分") or "未標示",
            "dosage_form": item.get("劑型") or "未標示",
            "strength": item.get("含量") or "未標示",
            "licence_status": item.get("通關簽審狀態") or "有效",
            "official_url": "https://www.fda.gov.tw"
        })
    
    # 使用 insert 直接寫入
    res = supabase.table("drug_approvals").insert(records).execute()
    print("✅ 成功寫入資料庫！傳回結果：", res)

except Exception as e:
    print(f"❌ 寫入發生錯誤: {e}")
