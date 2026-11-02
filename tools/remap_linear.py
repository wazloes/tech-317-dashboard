# Remap checklist parents 1:1 with Linear TECH-317 top-level checkboxes.
import json,re
L=json.load(open('/workspace/tech-317-qa/linear_items.json'))
T={t['id']:t for t in json.load(open('/tmp/tests.json'))}
CH={c['id']:c for t in T.values() for c in t.get('children',[])}
P=lambda *ids:[c['id'] for i in ids for c in T[i].get('children',[])]
# section -> (prefix, [(short name, [old parent ids for meta], [child ids])...]) in Linear order
M={
'jwt':('J1',[('Admin login + GET /user',['J1-01'],P('J1-01')),('Contractor + worker login',['J1-02'],P('J1-02')),
 ('Wrong-app login rejected',['J1-03'],P('J1-03')),('Unconfirmed account → 403',['J1-04'],P('J1-04')),
 ('Bad password ×8 (no throttle)',['J1-05'],P('J1-05')),('No token → token_not_provided',['J1-06'],P('J1-06')),
 ('Garbage token → token_invalid',['J1-07'],P('J1-07')),('Expired token refresh-in-header',['J1-08'],P('J1-08')),
 ('Past refresh window → 401 token_expired',['J1-14'],P('J1-14')),('Token refresh, old token blacklisted',['J1-09'],P('J1-09')),
 ('Logout then reuse → 401',['J1-10'],P('J1-10')),('Deleted user → 404',['J1-15'],P('J1-15')),
 ('Admin token_version on double login',['J1-11'],P('J1-11')),('Cross-host token 5.7 → staging5',['J1-16'],P('J1-16')),
 ('Role middleware (BUG-55)',['J1-12'],P('J1-12')),('Existing (bcrypt) passwords still verify',['J1-13'],P('J1-13'))]),
'otp':('S2',[('Send OTP happy path (SMS arrives)',['S2-01'],P('S2-01')),('Resend cooldown (429 + positive retry_after)',['S2-02'],P('S2-02')),
 ('After 60s resend 200, old code invalidated',['S2-03'],P('S2-03')),('Unsupported country / malformed number',['S2-04'],P('S2-04')),
 ('Missing / blank / fake captcha',['S2-05'],P('S2-05')),('Wrong verify code → 400',['S2-06'],P('S2-06')),
 ('3 wrong codes → 429 lockout',['S2-07'],P('S2-07')),('6 wrong codes → 423 locked',['S2-17'],P('S2-17')),
 ('Expired code (>15 min) → 400',[],[]),('0 users → signup',['S2-08'],P('S2-08')),('1 user → done',['S2-09'],P('S2-09')),
 ('2+ users → email_password_required',['S2-10'],P('S2-10')),('Flow token reuse / expiry',['S2-11'],P('S2-11')),
 ('Flow token from 5.7 staging',[],[]),('Wrong-app OTP message',['S2-12'],P('S2-12')),('Email availability check',['S2-13'],P('S2-13')),
 ('Send verification email (copy-paste link)',['S2-14'],P('S2-14')),('Password reset v2 forgot → verify → reset',['S2-15'],P('S2-15')),
 ('Legacy v1 register / confirm / resend code',['S2-16'],['S2-16a','S2-16c','S2-16b']),('Legacy v1 forgot / reset password',['S2-16'],['S2-16d','S2-16e'])]),
'stripe':('S3',[('Customer adds a card',[],[]),('Admin adds a card',['S3-03'],P('S3-03')),('Admin list company cards + user (BUG-44)',['S3-01'],P('S3-01')),
 ('Pay an invoice with 4242 (admin + customer)',['S3-04','S3-05'],P('S3-04','S3-05')),('Decline cards 0002 / 9995 / 0341',['S3-08'],P('S3-08')),
 ('3DS card 3155',['S3-09'],P('S3-09')),('No card for invoice country',['S3-07'],P('S3-07')),('Double-click / retry pay',['S3-06'],P('S3-06')),
 ('Stripe-Notice header',[],[]),('Webhook signature (unsigned + signed)',['S3-02'],P('S3-02')),('php artisan not needed (don\'t run UpdateCreditCardExpiry)',[],[])]),
'hours':('S4',[(T['S4-%02d'%i]['name'],['S4-%02d'%i],P('S4-%02d'%i)) for i in range(1,17)]),
'pay':('S5',[('Generate worker payment draft',['S5-01'],P('S5-01')),('Payment list + line items',['S5-02'],P('S5-02')),
 ('Export payment CSV + weekly pay CSV',['S5-03','S5-04'],P('S5-03','S5-04')),('Refresh worker pay owed',['S5-05'],P('S5-05')),
 ('Pay workers (VoPay, only if P4)',['S5-10'],P('S5-10')),('Cancel / cancel money transfers / mark-paid',['S5-06','S5-14'],P('S5-06','S5-14')),
 ('VoPay webhook',['S5-07'],P('S5-07')),('Trolley (sandbox): bank widget, payment rails, work permit',['S5-08','S5-15','S5-16'],P('S5-08','S5-15','S5-16')),
 ('Quick Pay',['S5-09','S5-11','S5-12','S5-13'],P('S5-09','S5-11','S5-12','S5-13'))]),
'invoice':('S6',[('Generate / save / preview / store invoices',['S6-01','S6-02'],P('S6-01')+['S6-10a','S6-10b']+P('S6-02')),
 ('Tax by site province',['S6-04'],P('S6-04')),('Tax rounding',['S6-03'],P('S6-03')),('Overtime rounded on PDF',['S6-15'],P('S6-15')),
 ('PDF download (customer + admin)',['S6-05'],P('S6-05')),('PDF stored on S3 after send (BUG-4)',[],[]),
 ('Timesheet PDF email (BUG-4)',['S6-06'],['S6-06b','S6-06c']),('Send invoice email with PDF',['S6-06'],['S6-06a']),
 ('Invoice number / mark-paid / mark-unpaid + list/view',['S6-07','S6-08'],P('S6-07')+['S6-08a','S6-08b','S6-08c','S6-08d','S6-08f']),
 ('Export-multiple zip + stats',['S6-09'],P('S6-09')+['S6-08e']),('Destroy draft invoice',['S6-10'],['S6-10c','S6-10d','S6-10e']),
 ('PO CRUD customer + admin',['S6-11'],P('S6-11')),('Projects without PO number',['S6-12'],['S6-12a','S6-12b']),
 ('External add-PO page',['S6-12'],['S6-12c']),('PO reminder email with PDF (BUG-99 / BUG-8)',['S6-13'],P('S6-13')),
 ('No duplicate "PO number updated" (BUG-1)',[],[]),('Company permissions (BUG-55)',['S6-14'],P('S6-14'))]),
'reg':('S7',[(T['S7-%02d'%i]['name'],['S7-%02d'%i],P('S7-%02d'%i)) for i in range(1,8)]),
}
def clean(s): return re.sub(r'<pull-request[^>]*>(.*?)</pull-request>',r'\1',s).replace('**','').replace('\\~','~').replace('\\[','[').replace('\\]',']').replace('`','')
def status(i,sec,n):
  a=i['text']+' '+' '.join(i['sub']); ic=re.findall('✅|❌|⛔|⏭',a)
  if sec=='stripe' and n==11: return 'skip'
  if i['checked']: return 'fail' if ic and ic[-1]=='❌' else 'pass'
  for k,v in (('❌','fail'),('⛔','blocked'),('⏭','skip'),('✅','warn')):
    if k in ic: return v
  return 'todo'
used=set();OUT=[];report=[]
for sec,(pre,rows) in M.items():
  items=L[sec]; assert len(items)==len(rows),(sec,len(items),len(rows))
  for n,(i,(name,olds,cids)) in enumerate(zip(items,rows),1):
    pid=f'{pre}-{n:02d}'; full=clean(i['text']); notes=[clean(x) for x in [i['text']]+i['sub'] if re.search('✅|❌|⛔|⏭',x)]
    # verdict = result text from Linear (from first result emoji onward)
    vs=[]
    for x in notes:
      m=re.search('(✅|❌|⛔|⏭).*',x); vs.append(m.group(0) if m else x)
    o=[T[x] for x in olds]
    st=status(i,sec,n)
    verdict=' '.join(vs) or ' '.join(t.get('verdict','') for t in o).strip() or ('Not run yet — no result in Linear.' if st=='todo' else ('Info only — Linear says this is not needed; intentionally not run.' if st=='skip' else 'Checked in Linear.'))
    tm=re.findall(r'2026-10-29 ~?(\d{1,2}:\d{2}(?: PM)?) MST',' '.join(vs))
    time=('2026-10-29 '+tm[-1]+' MST') if tm else (o[0].get('time','') if o else '')
    kids=[]
    for k,cid in enumerate(cids):
      c=dict(CH[cid]); used.add(cid); c['id']=pid+'abcdefghijklmnopqrstuvwxyz'[k]; c['parentId']=pid; kids.append(c)
    short=re.split(r'(?:✅|❌|⛔|⏭)',full)[0].strip()
    t={'id':pid,'section':sec,'name':name,'linear':f'§{list(M).index(sec)+1} · {short}','simple':(o[0].get('simple') if o else short),
       'status':st,'verdict':verdict,'time':time,'children':kids}
    if olds: t['note']='Was '+' + '.join(dict.fromkeys(olds))+' before the Linear 1:1 remap.'
    if not kids: report.append(f'{pid} {name} [{st}]')
    OUT.append(t)
allc=set(CH)-{c['id'] for t in T.values() if t['section']=='pre' for c in t.get('children',[])}
print('unplaced children:',sorted(allc-used))
print('no call captures:',*report,sep='\n  ')

CAP='/workspace/tech-317-qa/checklist-captures/s3-stripe/'
def capc(pid,suf,name,f,req,verdict):
  na={"label":"OLD \u00b7 not run","url":"\u2014","status":"N/A","headers":{},"body":"(not run)","reqHeaders":{},"reqBody":None,"at":"\u2014"}
  nw={"label":"NEW \u00b7 staging5","url":"https://staging5.faberconnect.com/company/credit-card/stripe","status":int(open(CAP+f+'.status').read().strip()),
      "headers":{},"body":open(CAP+f+'.body').read().strip(),"reqHeaders":{"Accept":"application/json","Authorization":"Bearer <REDACTED_JWT>"},"reqBody":req,"at":"2026-10-29 13:40 MST"}
  return {"id":pid+suf,"parentId":pid,"name":name,"method":"POST","path":"/company/credit-card/stripe","status":"fail","verdict":verdict,"diffs":[],"note":"Capture: s3-stripe/"+f,"time":"2026-10-29 13:40 MST","old":na,"new":nw}
c=[t for t in OUT if t['id']=='S3-01'][0]
c['children']=[capc('S3-01','a','Customer add tok_visa','new_cx_tok_visa','{"token_id": "tok_visa"}','Fail — 500 Server Error. Customer path not re-hit after the 15:28 admin retest.'),
 capc('S3-01','b','Customer add pm_card_visa','new_cx_pm_card_visa','{"token_id": "pm_card_visa"}','Fail — 400 "could not be verified" (pm_ ids are not tokens).')]
json.dump(OUT,open('/tmp/out.json','w'),ensure_ascii=False)
