import re

with open('/workspaces/saket/extracted_text/content.txt', 'r') as file:
    lines = file.readlines()

urls_with_content = []
urls_without_content = []

i = 0
while i < len(lines):
    line = lines[i].rstrip('\n')
    # Check if current line is a URL
    if re.match(r'^https?://', line):
        # Look ahead to see if there's any subsequent content before next URL
        # We'll copy everything up to the next URL (or end of file) if there's at least one non-empty, non-URL line
        j = i + 1
        has_content = False
        # Collect lines that might belong to this URL
        block_lines = [lines[i]]
        # Scan forward until the next URL or end of file
        while j < len(lines) and not re.match(r'^https?://', lines[j]):
            # If any of these lines is non-empty, we mark that as content
            if lines[j].strip():
                has_content = True
            block_lines.append(lines[j])
            j += 1

        # If we found content, keep them; otherwise put them in nocontent
        if has_content:
            urls_with_content.extend(block_lines)
        else:
            urls_without_content.extend(block_lines)

        # Move the outer loop index
        i = j
    else:
        # Just a normal line with no preceding URL
        urls_without_content.append(lines[i])
        i += 1

# Write results with content back to content.txt
with open('/workspaces/saket/extracted_text/content.txt', 'w') as file:
    for line in urls_with_content:
        file.write(line)

# Write results without content to nocontent.txt
with open('/workspaces/saket/extracted_text/nocontent.txt', 'w') as file:
    for line in urls_without_content:
        file.write(line)