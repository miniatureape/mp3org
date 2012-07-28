import os
import re
import shutil
import eyeD3


DRY_RUN = False

pattern = r"[^a-zA-Z0-9&_-]"

def slug(name):
    name = name.replace(' ', '-')
    name = re.sub(pattern, '', name)
    return name

input_path = "/media/LACIE/Music/MP3 Player"
output_path = "/media/LACIE/Music/mp3-organized"

files = os.listdir(input_path)
tag = eyeD3.Tag()

for f in files:
    if not os.path.splitext(f)[1] == '.mp3':
        continue

    mp3file = os.path.join(input_path, f)
    tag.link(mp3file)

    artist = slug(tag.getArtist())
    if not artist: artist = "Unknown Artist"

    album = slug(tag.getAlbum())
    if not album: album = "Unknown Album"

    artist_dir = os.path.join(output_path, artist)
    album_dir = os.path.join(output_path, artist, album)

    if not os.path.exists(album_dir):
        os.makedirs(album_dir)

    try:
        copied = os.path.join(album_dir, f)
    except UnicodeDecodeError:
        print "Unicode decode error for %s" % (f,)
        continue

    if DRY_RUN:
        if os.path.exists(copied):
            print "duplicate: %s,%s" % (mp3file, copied)
        else:
            print "copying: %s,%s" % (mp3file, copied)
    else:
        if os.path.exists(copied):
            print "duplicate: %s,%s" % (mp3file, copied)
        else:
            shutil.copy(mp3file, copied)
