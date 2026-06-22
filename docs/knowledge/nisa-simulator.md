# NISA Investment Simulator

## Location
Present on all homepage variants (`index.html`, `en/index.html`, etc.)

## Configuration
- **Start year**: 2021 (hardcoded in JS `state['nisa-start']`)
- **Year selector buttons**: Removed (previously had 2020/2022 chips on non-JA pages)
- **Context**: "Since Rakuten Mobile launched (4 years ago)"

## Heading per Language
| Lang | Heading |
|------|---------|
| JA | もしも楽天モバイル開始時（4年前）から、この節約額をNISAで積立投資していたら？ |
| EN | What if you'd invested these savings in NISA since Rakuten Mobile launched (4 years ago)? |
| zh-tw | 如果從樂天Mobile開始時（4年前）就把省下的錢投入NISA呢？ |
| vi | Nếu bạn đầu tư tiền tiết kiệm vào NISA từ khi Rakuten Mobile ra mắt (4 năm trước)? |
| my | Rakuten Mobile စတင်ချိန် (၄ နှစ်အကြာ) ကတည်းက ချွေတာငွေကို NISA မှာ ရင်းနှီးမြှုပ်နှံခဲ့ရင်? |
| th | ถ้าคุณลงทุนเงินออมใน NISA ตั้งแต่ Rakuten Mobile เปิดตัว (4 ปีที่แล้ว)? |

## ETF Price Data (in JS)
```
VT:   2020:80, 2021:93, 2022:107, 2023:88, 2024:107, 2025:125, 2026:135
SPY:  2020:323, 2021:375, 2022:477, 2023:390, 2024:475, 2025:595, 2026:634
QQQ:  2020:212, 2021:315, 2022:398, 2023:270, 2024:408, 2025:525, 2026:563
N225: 2020:23200, 2021:27400, 2022:28800, 2023:26000, 2024:33500, 2025:39800, 2026:37000
```

## Credit Cards Page NISA
The credit cards page (`credit-cards/index.html`) has a separate Points→NISA simulator using `ANNUAL_RETURNS` data starting from 2022. This was NOT changed in the April 2026 updates.
