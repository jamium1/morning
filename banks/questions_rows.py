"""Turn a brief's data.json into rows for the 'Questions' tab of the Revision log.
Usage: python3 questions_rows.py data.json  -> prints a JSON array of rows
Columns: QID | Date | Subject | Kind | Source | Question | Model answer / marking notes | Markable
"""
import json, re, sys, html as H

def text(s):
    if not s: return ''
    s = re.sub(r'<\s*br\s*/?>', '\n', s)
    s = re.sub(r'</(p|li|div|h\d)>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = H.unescape(s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()

d = json.load(open(sys.argv[1]))
date = d['date_iso']
rows = []
for b in d['revision']['blocks']:
    for q in b['questions']:
        parts = []
        if q.get('latin'): parts.append(text(q['latin']))
        if q.get('stimulus_text'): parts.append(text(q['stimulus_text']))
        parts.append(text(q.get('prompt')))
        model = text(q.get('answer_html') or q.get('answer_text') or '')
        model = re.sub(r'^Your translation:', 'Reference translation (from your doc):', model)
        m = q.get('mark') or {}
        notes = text(m.get('context') or '')
        notes = re.split(r'\n\s*Full text:', notes)[0].strip()
        core = re.sub(r"^(Reference solution|Student's own reference translation):\s*", '', notes)
        if notes and (not model or (core not in model and model not in notes)):
            model = (model + '\n\nMarking notes: ' + notes).strip()
        rows.append([f"{date}:{q['id']}", date, b['subject'], text(q.get('kind_label')),
                     text(q.get('source')), '\n\n'.join(p for p in parts if p), model, 'Yes'])
if d.get('journal_prompt'):
    rows.append([f"journal-{date}", date, 'Journal', 'Journal entry', '', d['journal_prompt'], '', 'No'])
print(json.dumps(rows, ensure_ascii=False))
