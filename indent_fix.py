with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
indent_level = 0
for line in lines:
    stripped = line.lstrip()
    # Check if this line is the end container marker
    if stripped.startswith("# end container"):
        if indent_level > 0:
            indent_level -= 4
        continue # skip the marker line entirely
        
    # Apply current extra indentation (only to non-empty lines)
    if stripped and indent_level > 0:
        line = (" " * indent_level) + line
        
    new_lines.append(line)
    
    # Check if this line starts a container
    if "with st.container(border=True):" in line:
        indent_level += 4

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
