#!/usr/bin/env python3
"""
extract_D_sorted.py
────────────────────────────────────────────────────────────
blkparse 출력 파일을 인자로 받아
  • 액션 == 'D' 인 행만 추출
  • 타임스탬프(4‑번째 필드) 기준 정렬
  • 결과를  <basename>.D.sorted  로
    ─ 현재 작업 디렉터리 ─ 에 저장
----------------------------------------------------------------
Usage:
    python3 extract_D_sorted.py /path/to/conv_blktrace.output
"""

import sys
from pathlib import Path

# ─ 1. 인자 확인 ────────────────────────────────────────────
if len(sys.argv) != 2:
    print("Usage: python3 extract_D_sorted.py <blkparse_output_file>")
    sys.exit(1)

in_path = Path(sys.argv[1]).expanduser().resolve()
basename = in_path.name                     # 디렉터리 제외한 파일명
out_path = Path.cwd() / Path(basename).with_suffix(".D.sorted")

print(f"[+] Reading : {in_path}")
with in_path.open() as f:
    lines = f.readlines()

print(f"[+] Total {len(lines):,} lines — filtering ‘D’ action…")

# ─ 2. 'D' 행만 추출 + 타임스탬프 파싱 ────────────────────
d_lines = []
for ln in lines:
    parts = ln.split()
    if len(parts) > 5 and parts[5] == 'D':      # 액션 == 'D'
        try:
            ts = float(parts[3])                # 4‑번째 필드: timestamp
            d_lines.append((ts, ln))
        except ValueError:
            continue

print(f"[+] Found {len(d_lines):,} lines with action ‘D’ — sorting…")
d_lines.sort(key=lambda x: x[0])               # 타임스탬프 오름차순
sorted_only_D = [ln for _, ln in d_lines]

# ─ 3. 현재 디렉터리에 저장 ────────────────────────────────
print(f"[+] Writing : {out_path}")
with out_path.open("w") as f:
    f.writelines(sorted_only_D)

print("[+] Done.")

