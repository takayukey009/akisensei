import re

html_path = 'c:/Users/togawa_takayuki/.gemini/antigravity/playground/exo-photon/gate-x-shizuku-proposal.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove slide-2 entirely
# It starts with <!-- ==================== SLIDE 2: WHY SHIZUKU AI ==================== -->
slide_2_pattern = re.compile(r'<!-- ==================== SLIDE 2: WHY SHIZUKU AI ==================== -->.*?</section>\n+', re.DOTALL)
content = slide_2_pattern.sub('', content)

# Function to renumber slide IDs and comments
def renumber_section(match):
    comment_num = int(match.group(1))
    title = match.group(2)
    slide_id = int(match.group(3))
    
    new_num = slide_id - 1
    return f'<!-- ==================== SLIDE {new_num}: {title} ==================== -->\n<section class="slide" id="slide-{new_num}">'

# This pattern matches slides from 3 onwards
# e.g., <!-- ==================== SLIDE 3: STRATEGY ANALYSIS ==================== -->\n<section class="slide" id="slide-3">
part1_pattern = re.compile(r'<!-- ==================== SLIDE (\d+): (.*?) ==================== -->\n<section class="slide(.*?)" id="slide-(\d+)">')

def renumber_part1(match):
    old_comment_num = int(match.group(1))
    title = match.group(2)
    classes = match.group(3)
    old_id = int(match.group(4))
    
    new_num = old_id - 1
    return f'<!-- ==================== SLIDE {new_num}: {title} ==================== -->\n<section class="slide{classes}" id="slide-{new_num}">'

content = part1_pattern.sub(renumber_part1, content)

def renumber_span(match):
    current_num = int(match.group(1))
    # If it's slide 1, it becomes 01 / 12
    # If it's slide 3, it becomes 02 / 12
    # If it's slide 13, it becomes 12 / 12
    if current_num == 1:
        new_num = 1
    else:
        new_num = current_num - 1
    return f'<span class="slide-number">{new_num:02d} / 12</span>'

span_pattern = re.compile(r'<span class="slide-number">(\d{2}) / 13</span>')
content = span_pattern.sub(renumber_span, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated HTML.')
