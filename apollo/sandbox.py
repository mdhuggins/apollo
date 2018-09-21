from playback import *
from wav import *

import time

for _ in range(60):
    print(get_play_status(), get_play_time())
    time.sleep(1)
