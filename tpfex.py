from struct import unpack
import sys

def main (file):
    MAGIC_KEY = 0x31
    with open (file, 'rb') as f:
        magic, count, unk0, unk1, size, unk2 = unpack ('<HHIIII', f.read (20))
        if magic != MAGIC_KEY:
            print (f'magic {magic} != {MAGIC_KEY}')
            return
        
        entries = []
        for i in range (count):
            entry = {}
            entry['name'] = f.read (16).decode ('utf8').replace ('\0', '')
            entry['size'], entry['offset'] = unpack ('<II', f.read (8))
            entries.append (entry)

        data = f.tell ();
        for entry in entries:
            print (f'name {entry["name"]} size {entry["size"]} offset {entry["offset"]}')

            with open (entry['name'], 'wb') as out:
                f.seek (data, 0)
                f.seek (entry['offset'], 1)
                out.write (f.read (entry['size']))
            
if __name__ == '__main__':
    main (sys.argv[1])
        
