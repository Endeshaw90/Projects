import os, glob

path = 'BSS_docs'
print('Abs path:', os.path.abspath(path))
print('Exists:', os.path.exists(path))

if os.path.exists(path):
    print('Dir listing:', os.listdir(path))
    pattern1 = os.path.join(path, '*.pdf')
    pattern2 = os.path.join(path, '**/*.pdf')
    print('Pattern 1:', pattern1, '->', glob.glob(pattern1))
    print('Pattern 2:', pattern2, '->', glob.glob(pattern2, recursive=True))
