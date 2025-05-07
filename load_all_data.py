import os
import glob
import subprocess

backup_dir = "./backup/"
fixtures = glob.glob(os.path.join(backup_dir, '*.json'))
connected_data = []

print(f"Found fixtures: {fixtures}")

# المرحلة الأولى
for fixture in fixtures:
    print(f"Loading {fixture}...")
    try:
        subprocess.run(['python', 'manage.py', 'loaddata', fixture], check=True)
        print(f"{fixture} loaded.")
    except Exception as e:
        connected_data.append(fixture)
        print(f"{fixture} failed. Will retry later.")

# إعادة المحاولة لعدة مرات (حتى 7 مرات مثلاً)
for attempt in range(2, 8):
    if not connected_data:
        break

    print(f"\n🔁 Retry attempt {attempt}")
    failed = []

    for fixture in connected_data:
        print(f"Retrying {fixture}...")
        try:
            subprocess.run(['python', 'manage.py', 'loaddata', fixture], check=True)
            print(f"{fixture} loaded on attempt {attempt}.")
        except:
            failed.append(fixture)
            print(f"{fixture} still failing.")

    connected_data = failed

# النتيجة النهائية
print("\n📦 Fixtures remaining after retries:")
print(connected_data)
