import io

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('st.markdown("<div class=\'glass-card\'>", unsafe_allow_html=True)', 'with st.container(border=True):')
content = content.replace('st.markdown("</div>", unsafe_allow_html=True)', '# end container')

# Also handle the empty matches crash
content = content.replace('''            # Target role roadmap compiler data
            top_match = matches[0]''', '''            # Target role roadmap compiler data
            if not matches:
                st.warning("No matches found to generate a report for.")
                st.stop()
            top_match = matches[0]''')


with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
