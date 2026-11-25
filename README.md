# Python Algorithm Visualizers

**ภาษาไทย** | [English](README.en.md)

แอปพลิเคชันเดสก์ท็อป 2 ตัวที่เปลี่ยนอัลกอริทึมพื้นฐานให้ดูการทำงานและโต้ตอบได้ เขียนด้วย Python และ Tkinter

| โปรเจกต์ | ทำอะไร | อัลกอริทึมหลัก | ประเภท |
|---|---|---|---|
| [EV Eco-Routing](ev-eco-routing/README.md) | หาเส้นทางที่ใช้แบตเตอรี่น้อยที่สุดระหว่าง 7 จังหวัดภาคใต้ตอนล่าง และตรวจว่าแบตที่มีพอเดินทางหรือไม่ | Dijkstra's shortest path ด้วย priority queue (`heapq`) | งานเดี่ยวในรายวิชา (2569) |
| [Algorithms Visualizer](algorithms-visualizer/README.md) | แสดงการเรียงลำดับและค้นหาข้อมูลทีละขั้นเป็นแอนิเมชัน ใส่ข้อมูลเองหรือสุ่มได้ ปรับความเร็วได้ และนับจำนวนการเปรียบเทียบ | Bubble, Selection, Insertion, Merge Sort · Sequential และ Binary Search | มินิโปรเจกต์กลุ่ม (2568) |

![EV Eco-Routing: เส้นทางที่ใช้แบตน้อยที่สุดจากตรังไปนราธิวาส](docs/ev-route-trang-narathiwat.png)

*EV Eco-Routing: เส้นทางที่ใช้แบตน้อยที่สุดจากตรังไปนราธิวาส (70%) ผ่านสตูล สงขลา และปัตตานี*

## เริ่มต้นใช้งาน

ต้องใช้ Python 3.10 ขึ้นไปที่มี Tkinter (มาพร้อมตัวติดตั้งมาตรฐานของ Windows และ macOS)

```bash
git clone https://github.com/nazhan0-dev/python-algorithm-visualizers.git
cd python-algorithm-visualizers
pip install -r requirements.txt

python ev-eco-routing/ev_eco_routing.py
python algorithms-visualizer/algorithms_visualizer.py
```

บน Ubuntu/Debian ให้ติดตั้ง Tkinter ก่อนด้วยคำสั่ง `sudo apt install python3-tk`

## โครงสร้าง repo

```
python-algorithm-visualizers/
├── ev-eco-routing/          # โปรแกรมวางแผนเส้นทางด้วย Dijkstra (Tkinter + Matplotlib)
├── algorithms-visualizer/   # แอนิเมชันการเรียงลำดับและค้นหา (Tkinter)
├── docs/                    # ภาพหน้าจอที่ใช้ใน README
└── requirements.txt
```

## ที่มา

ทั้งสองโปรเจกต์มาจากรายวิชาโครงสร้างข้อมูลและอัลกอริทึม หลักสูตรวิทยาการคอมพิวเตอร์ มหาวิทยาลัยราชภัฏสงขลา หน้าจอโปรแกรมเป็นภาษาไทย
