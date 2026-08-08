import os
import zipfile
import glob

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKS_DIR = os.path.join(DATA_DIR, 'chunked_datasets')

large_files = [
    'kuairand_final_merged.csv',
    'kuairand_video_categories.csv',
    'log_stacked_master_preprocessed.csv',
    'log_random_4_22_to_5_08_pure_preprocessed.csv'
]

print("Reassembling dataset files from GitHub chunks...")

for fname in large_files:
    parts = sorted(glob.glob(os.path.join(CHUNKS_DIR, f"{fname}.zip.part*")))
    if not parts:
        print(f"No chunks found for {fname}")
        continue
    
    temp_zip = os.path.join(DATA_DIR, f"temp_{fname}.zip")
    print(f"Reassembling {fname} from {len(parts)} chunks...")
    with open(temp_zip, 'wb') as f_out:
        for p in parts:
            with open(p, 'rb') as f_in:
                f_out.write(f_in.read())
                
    print(f"Extracting {fname}...")
    with zipfile.ZipFile(temp_zip, 'r') as zf:
        zf.extractall(DATA_DIR)
        
    os.remove(temp_zip)
    print(f"Successfully restored {fname}!")

print("All datasets restored to 100% original state.")
