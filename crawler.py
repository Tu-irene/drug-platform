import os
from supabase import create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

print(f"🔑 檢查 URL: {supabase_url[:20] if supabase_url else 'NONE'}...")

try:
    supabase = create_client(supabase_url, supabase_key)

    # 構造一筆測試資料
    test_data = [{
        "country": "測試國家",
        "brand_name": "測試藥品-吉利達",
        "active_ingredient": "Pembrolizumab",
        "dosage_form": "注射劑",
        "strength": "100mg/4mL",
        "licence_status": "有效",
        "official_url": "https://example.com"
    }]

    print("📤 正在嘗試寫入 Supabase...")
    res = supabase.table("drug_approvals").insert(test_data).execute()
    print("🎉 寫入成功！回傳資料：", res)

except Exception as e:
    print(f"❌ 寫入失敗，詳細原因: {e}")
