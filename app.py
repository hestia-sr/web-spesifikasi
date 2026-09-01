import os
import shutil
import subprocess
from flask import Flask, render_template

app = Flask(__name__)


def get_cpu_info():
  try:
    board = (
        subprocess.check_output(['getprop', 'ro.product.board'])
        .decode('utf-8')
        .strip()
    )
    hardware = (
        subprocess.check_output(['getprop', 'ro.hardware'])
        .decode('utf-8')
        .strip()
    )
    machine = os.uname().machine
    if board or hardware:
      return f'{hardware.upper()} / {board.upper()} ({machine})'
  except Exception:
    pass

  try:
    with open('/proc/cpuinfo', 'r') as f:
      for line in f:
        if 'Hardware' in line or 'model name' in line:
          return line.split(':')[1].strip()
  except Exception:
    pass
  return 'ARM64 Processor'


def get_storage_info():
  paths = ['/sdcard', '/storage/emulated/0']
  for path in paths:
    try:
      if os.path.exists(path):
        total, used, free = shutil.disk_usage(path)
        total_gb = total // (2**30)
        free_gb = free // (2**30)
        used_gb = used // (2**30)
        if total_gb > 0:
          return (
              f'Total: ~{total_gb} GB | Terpakai: {used_gb} GB | Sisa:'
              f' {free_gb} GB'
          )
    except Exception:
      continue
  return 'Cloud Server Storage (Render)'


@app.route('/')
def index():
  cpu_name = get_cpu_info()
  storage_info = get_storage_info()
  return render_template('index.html', cpu=cpu_name, storage=storage_info)


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
