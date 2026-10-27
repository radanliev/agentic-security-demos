import json, collections, re, random, math, sys
import pandas as pd
import os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','raw')+os.sep
def kev(): return json.load(open(R+'kev.json'))['vulnerabilities']
def nvd(f): return json.load(open(R+f))
def sev(v):
    m=v['cve'].get('metrics',{})
    for k in ('cvssMetricV31','cvssMetricV30'):
        for x in m.get(k,[]):
            if x['type']=='Primary': return x['cvssData']['baseSeverity']
    for k in ('cvssMetricV31','cvssMetricV30'):
        if m.get(k): return m[k][0]['cvssData']['baseSeverity']+'(secondary-only)'
    return 'NONE'
def cwes(v): return sorted({d['value'] for w in v['cve'].get('weaknesses',[]) for d in w['description']})
def year(v): return v['cve']['published'][:4]
def nvd_summary(f, filt=None):
    d=nvd(f); vs=d['vulnerabilities']
    if filt: vs=[v for v in vs if filt(v)]
    kevids={k['cveID'] for k in kev()}
    return {'query':d['params'],'retrieved_utc':d['retrieved_utc'],'n':len(vs),
     'by_year':dict(sorted(collections.Counter(year(v) for v in vs).items())),
     'severity':dict(collections.Counter(sev(v) for v in vs).most_common()),
     'top_cwe':collections.Counter(c for v in vs for c in cwes(v)).most_common(10),
     'in_kev':sorted(v['cve']['id'] for v in vs if v['cve']['id'] in kevids)}
def kev_cwe(c):
    ks=[k for k in kev() if c in k.get('cwes',[])]
    return {'cwe':c,'kev_entries':len(ks),'known_ransomware':sum(k['knownRansomwareCampaignUse']=='Known' for k in ks),
            'by_year_added':dict(sorted(collections.Counter(k['dateAdded'][:4] for k in ks).items()))}
def tot(c): return json.load(open(R+f'nvd_tot_{c}.json'))['totalResults']
def ds(name):
    tr=pd.read_parquet(R+name+'_train.parquet'); te=pd.read_parquet(R+name+'_test.parquet')
    if name=='jb':
        for x in (tr,te): x['text']=x['prompt']; x['label']=(x['type']=='jailbreak').astype(int)
    return tr,te
norm=lambda s: re.sub(r'\W+',' ',s.lower()).strip()

def d03():
    out={}
    for n,lab in (('pi','deepset/prompt-injections'),('jb','jackhhao/jailbreak-classification')):
        tr,te=ds(n); trs=set(tr.text); trn=set(map(norm,tr.text))
        out[lab]={'train':len(tr),'test':len(te),'test_pos_rate':round(te.label.mean(),3),
          'test_exact_in_train':int(te.text.isin(trs).sum()),'test_normalised_in_train':int(sum(norm(t) in trn for t in te.text)),
          'train_internal_exact_duplicates':int(tr.text.duplicated().sum())}
    return out
def d04():
    s=nvd_summary('nvd_prompt_injection.json'); s['cwe_1427_tagged_total_in_nvd']=tot('CWE-1427'); return s
def d06():
    ks=kev(); edge=re.compile(r'router|firewall|vpn|gateway|switch|load balancer|edge|ssl|remote access',re.I)
    e=[k for k in ks if edge.search(k['product']+' '+k['vulnerabilityName'])]
    return {'kev_total':len(ks),'kev_catalog_version':json.load(open(R+'kev.json'))['catalogVersion'],
      'network_edge_entries_keyword_match':len(e),'share':round(len(e)/len(ks),3),
      'top_vendors_edge':collections.Counter(k['vendorProject'] for k in e).most_common(10),
      'note':'Edge classification is a keyword heuristic over product and vulnerability name; not manually verified.'}
def d07():
    ks=kev(); c=collections.Counter(k['knownRansomwareCampaignUse'] for k in ks)
    return {'kev_total':len(ks),'ransomware_use':dict(c),'ransomware_known_base_rate':round(c['Known']/len(ks),3),
      'added_by_year':dict(sorted(collections.Counter(k['dateAdded'][:4] for k in ks).items())),
      'top_cwe':collections.Counter(w for k in ks for w in k.get('cwes',[])).most_common(10)}
def d08(): return {'nvd_total_CWE-22':tot('CWE-22'),'nvd_total_CWE-98':tot('CWE-98'),'kev_CWE-22':kev_cwe('CWE-22'),'kev_CWE-98':kev_cwe('CWE-98')}
def d09(): return {'nvd_total_CWE-295':tot('CWE-295'),'kev_CWE-295':kev_cwe('CWE-295'),'kev_CWE-300':kev_cwe('CWE-300')}
def d10(): return nvd_summary('nvd_vuln_scanner.json')
def metrics(y,p):
    tp=sum(a and b for a,b in zip(y,p)); tn=sum((not a) and (not b) for a,b in zip(y,p)); fp=sum((not a) and b for a,b in zip(y,p)); fn=sum(a and not b for a,b in zip(y,p))
    acc=(tp+tn)/len(y); tpr=tp/(tp+fn) if tp+fn else 0; tnr=tn/(tn+fp) if tn+fp else 0
    prec=tp/(tp+fp) if tp+fp else 0; f1=2*prec*tpr/(prec+tpr) if prec+tpr else 0
    return {'tp':tp,'fp':fp,'tn':tn,'fn':fn,'accuracy':round(acc,3),'balanced_accuracy':round((tpr+tnr)/2,3),'f1':round(f1,3)}
def d11():
    tr,te=ds('pi'); y=list(te.label.astype(bool)); maj=bool(tr.label.mean()>=0.5); rnd=random.Random(42)
    kw=re.compile(r'ignore|forget|disregard|vergiss|ignoriere|previous instructions|system prompt',re.I)
    return {'dataset':'deepset/prompt-injections test','n':len(y),'positives':sum(y),
      'baselines':{'always_allow(no defence)':metrics(y,[False]*len(y)),'always_block':metrics(y,[True]*len(y)),
       'majority_class_from_train':metrics(y,[maj]*len(y)),'random_p0.5_seed42':metrics(y,[rnd.random()<0.5 for _ in y]),
       'keyword_rule':metrics(y,[bool(kw.search(t)) for t in te.text])}}
def d12(): return nvd_summary('nvd_calendar_injection.json',lambda v:'calendar' in v['cve']['descriptions'][0]['value'].lower())
def d13():
    vs=nvd('nvd_prompt_injection.json')['vulnerabilities']; pairs=[]
    for v in vs:
        m=v['cve'].get('metrics',{}).get('cvssMetricV31',[])
        p=[x['cvssData']['baseSeverity'] for x in m if x['type']=='Primary']; s=[x['cvssData']['baseSeverity'] for x in m if x['type']=='Secondary']
        if p and s: pairs.append((p[0],s[0]))
    n=len(pairs); agree=sum(a==b for a,b in pairs)/n if n else 0
    ca=collections.Counter(a for a,_ in pairs); cb=collections.Counter(b for _,b in pairs)
    pe=sum(ca[k]*cb[k] for k in set(ca)|set(cb))/(n*n) if n else 0
    return {'set':'NVD CVEs matching "prompt injection" with both NVD (Primary) and CNA (Secondary) CVSS v3.1','n_pairs':n,
      'raw_agreement':round(agree,3),'cohens_kappa':round((agree-pe)/(1-pe),3) if n and pe<1 else None,
      'confusion':collections.Counter(f'{a}->{b}' for a,b in pairs).most_common()}
def model(tr):
    from sklearn.feature_extraction.text import TfidfVectorizer; from sklearn.linear_model import LogisticRegression; from sklearn.pipeline import make_pipeline
    return make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True),LogisticRegression(max_iter=2000)).fit(tr.text,tr.label)
def d14(alpha=0.30):
    import numpy as np
    tr,te=ds('pi'); _,jte=ds('jb'); tr=tr.sample(frac=1,random_state=42); cut=int(len(tr)*0.7)
    m=model(tr.iloc[:cut]); cal=tr.iloc[cut:]
    s=m.predict_proba(cal.text)[:,1]; mal=np.sort(s[cal.label.values==1]); k=len(mal)
    # gate: execute iff score < t. risk = P(execute | malicious). choose t = conformal quantile so that risk<=alpha
    idx=int(math.floor(alpha*(k+1)))-1; t=float(mal[max(idx,0)]) if k else 0.5
    def ev(df):
        sc=m.predict_proba(df.text)[:,1]; mm=df.label.values==1
        return {'n':int(len(df)),'malicious':int(mm.sum()),'risk_malicious_executed':round(float((sc[mm]<t).mean()),3),'benign_blocked_rate':round(float((sc[~mm]>=t).mean()),3)}
    return {'alpha':alpha,'calibration_malicious_n':k,'threshold':round(t,4),'scorer':'TF-IDF(1-2gram)+logistic regression, seed 42',
      'same_distribution_test(deepset test)':ev(te),'shifted_test(jackhhao jailbreak test)':ev(jte)}
def d15(th=0.55):
    tr,te=ds('jb'); _,pte=ds('pi'); m=model(tr)
    def ev(df):
        p=m.predict_proba(df.text)[:,1]>=th; return metrics(list(df.label.astype(bool)),list(p))
    return {'threshold':th,'probe':'black-box text proxy (TF-IDF+LR on prompt text); NOT a white-box activation probe','in_distribution(jackhhao test)':ev(te),'cross_dataset(deepset test)':ev(pte)}

if __name__=='__main__':
    out=d12()
    p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','results','real_data_results.json')
    json.dump(out,open(p,'w'),indent=1,default=str); print(json.dumps(out,indent=1,default=str))
