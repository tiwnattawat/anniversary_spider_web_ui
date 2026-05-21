import json
import re

with open('photos.json', 'r', encoding='utf-8') as f:
    files = json.load(f)

photos = [p for p in files if not p['img'].lower().endswith(('.mp4', '.mov'))]

photos_js = "const PHOTOS = [\n"
for p in photos:
    photos_js += f'    {{ img: "{p["img"]}", caption: "", date: "{p["date"]}" }},\n'
photos_js += "  ];"

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace PHOTOS
html = re.sub(r'const PHOTOS = \[.*?\];', photos_js, html, flags=re.DOTALL)

# Add volume slider in HTML
slider_html = '''
      <div class="music-controls" style="display: flex; align-items: center; gap: 10px;">
        <input type="range" id="volume-slider" min="0" max="1" step="0.01" value="1" oninput="changeVolume(this.value)" style="width: 80px;">
        <button class="music-btn" id="music-btn" onclick="toggleMusic(this)">
          <i class="ti ti-player-play" style="font-size:14px" aria-hidden="true"></i>
          <span>เพลง</span>
        </button>
      </div>
'''
html = re.sub(r'<button class="music-btn" onclick="toggleMusic\(this\)">.*?</button>', slider_html, html, flags=re.DOTALL)

# Modify checkPw to auto play music
# Find checkPw function
checkpw_new = '''function checkPw() {
    const v = document.getElementById('pw').value;
    if (v === PASS) {
      document.getElementById('pw-err').textContent = '';
      document.getElementById('screen-lock').classList.add('hidden');
      setTimeout(() => {
        document.getElementById('screen-web').classList.add('visible');
        initWeb();
        const audio = document.getElementById('bg-music');
        audio.play().catch(e => console.log("Audio play failed:", e));
        musicOn = true;
        updateMusicUI();
      }, 600);
    } else {'''
html = html.replace('''function checkPw() {
    const v = document.getElementById('pw').value;
    if (v === PASS) {
      document.getElementById('pw-err').textContent = '';
      document.getElementById('screen-lock').classList.add('hidden');
      setTimeout(() => {
        document.getElementById('screen-web').classList.add('visible');
        initWeb();
      }, 600);
    } else {''', checkpw_new)

# Modify toggleMusic and add updateMusicUI and changeVolume
music_js = '''let musicOn = false;

  function updateMusicUI() {
    const btn = document.getElementById('music-btn');
    const icon = btn.querySelector('i');
    const txt = btn.querySelector('span');
    if (musicOn) {
      icon.className = 'ti ti-player-pause';
      txt.textContent = 'หยุดเพลง';
      btn.style.borderColor = 'rgba(255, 105, 180, .6)';
      btn.style.boxShadow = '0 0 10px rgba(255, 105, 180, 0.4)';
    } else {
      icon.className = 'ti ti-player-play';
      txt.textContent = 'เพลง';
      btn.style.borderColor = '';
      btn.style.boxShadow = '';
    }
  }

  function toggleMusic(btn) {
    musicOn = !musicOn;
    const audio = document.getElementById('bg-music');
    
    if (musicOn) {
      audio.play().catch(e => console.log("Audio play failed:", e));
    } else {
      audio.pause();
    }
    updateMusicUI();
  }

  function changeVolume(val) {
    document.getElementById('bg-music').volume = val;
  }'''

html = re.sub(r'let musicOn = false;.*?function toggleMusic\(btn\) \{.*?\}', music_js, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
