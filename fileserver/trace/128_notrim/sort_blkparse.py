#!/usr/bin/env python3
"""
sort_blkparse.py
──────────────────────────────────────────────────────────
blkparse 텍스트(conv_blktrace.output 등)에서

  • 디바이스번호  CPU  Seq  <TIMESTAMP> …

형식(4‑번째 필드가 초.나노초 숫자)인 행들만
타임스탬프 오름차순으로 정렬한다.

그 외 형식이 맞지 않는 행(요약/헤더/빈 줄 등)은
정렬하지 않고 원본 순서 그대로 파일 맨 뒤에 유지.

▶ 사용
    python3 sort_blkparse.py conv_blktrace.output
    # → conv_blktrace.sorted  생성
"""

import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python3 sort_blkparse.py <blkparse_output_file>")
    sys.exit(1)

in_path  = Path(sys.argv[1]).expanduser().resolve()
out_path = in_path.with_suffix(".sorted")

print(f"[+] Reading : {in_path}")
with in_path.open() as f:
    lines = f.readlines()
print(f"[+] Total {len(lines):,} lines read — separating…")

sortable, unsortable = [], []   # (ts, line) / line

for line in lines:
    parts = line.split()
    try:
        ts = float(parts[3])         # 4‑번째 필드
        sortable.append((ts, line))
    except (IndexError, ValueError):
        unsortable.append(line)      # 형식이 다르면 그대로 보관

print(f"[+] Sortable lines   : {len(sortable):,}")
print(f"[+] Unsortable lines : {len(unsortable):,}")

sortable.sort(key=lambda x: x[0])   # 타임스탬프 기준 정렬
sorted_lines = [ln for _, ln in sortable] + unsortable   # 뒤에 그대로 붙임

print(f"[+] Writing  : {out_path}")
with out_path.open("w") as f:
    f.writelines(sorted_lines)

print("[+] Done.")

