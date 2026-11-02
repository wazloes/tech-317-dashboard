"""Replace one §4 parent in checklist/index.html, keeping id/section/name/linear/simple from the current row."""
import json,re,sys
P='/workspace/tech-317-qa-dashboard/checklist/index.html'
def set_parent(pid,status,verdict,time,children,note=''):
    h=open(P).read()
    m=re.search(r'^TESTS\.push\((\{"id":\s*"'+re.escape(pid)+r'".*?\})\);$',h,re.M)
    assert m,pid
    cur=json.loads(m.group(1).replace('<\\/','</'))
    for c in children:
        assert c.get('method') and c.get('path') and 'see http.log' not in json.dumps(c),c.get('name')
        if c['method'].upper() in('POST','PUT','PATCH','DELETE'):
            assert c.get('db') and (c['db'].get('tables') or c['db'].get('skipped')),('db missing',c['name'])
    cur.update(status=status,verdict=verdict,time=time,children=children)
    if note: cur['note']=note
    js=json.dumps(cur,ensure_ascii=False).replace('</','<\\/')
    js=re.sub(r'(X-Amz-(?:Credential|Signature|Security-Token)=)[^&"\\\s]+',r'\1<REDACTED>',js)
    js=re.sub(r'AKIA[A-Z0-9]{16}','<REDACTED_AKID>',js)
    assert 'eyJ' not in js and not re.search(r'AKIA[A-Z0-9]{16}',js)
    h=h[:m.start()]+'TESTS.push('+js+');'+h[m.end():]
    open(P,'w').write(h)
if __name__=='__main__':
    d=json.load(open(sys.argv[1]))
    for x in d: set_parent(**x)
