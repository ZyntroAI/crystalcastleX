# AI Layer

ชั้น abstraction ของ AI — ออกแบบให้ **provider-neutral** โค้ดธุรกิจไม่ผูกกับเจ้าของโมเดลรายใด

| โฟลเดอร์ | หน้าที่ |
| --- | --- |
| `prompts/` | เทมเพลต prompt ที่ใช้ซ้ำได้ |
| `pipelines/` | ลำดับขั้นการประมวลผล (เช่น storyboard → video) |
| `providers/` | adapter ต่อผู้ให้บริการ (OpenAI / Gemini / Groq / FAL / RunwayML …) |

> 📌 โครงนี้ถูกกำหนดเป็นเป้าหมายเชิงสถาปัตยกรรม — โค้ดจริงทยอยย้ายเข้ามา
