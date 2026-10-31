"""Verify the separate recovery study and generate its manuscript assets."""
from __future__ import annotations
import csv,hashlib,json,re
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/meta-routing/intellisys2027'
PAPER=ROOT/'papers/meta-routing/intellisys2027'
def rows(name):
    with (OUT/name).open(newline='') as f:return list(csv.DictReader(f))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name,caption,label,spec,head,body):
    (PAPER/f'{name}.tex').write_text('\n'.join([r'\begin{table}[!htbp]',r'\caption{'+caption+'}',r'\label{'+label+'}',r'\centering\small',r'\begin{tabular}{'+spec+'}',r'\toprule',head+r' \\',r'\midrule',*[r+r' \\' for r in body],r'\bottomrule',r'\end{tabular}',r'\end{table}'])+'\n')
def main():
    fit=json.loads((OUT/'frozen_config.json').read_text())
    for path,sha in fit['source_sha256'].items():assert digest(ROOT/path)==sha,path
    assert fit['test_policy_tuning'] is False
    for n,sha in fit['raw_sha256'].items():assert digest(ROOT/f'benchmarks/recovery2027/raw/{n}.zip')==sha
    for tracefile,summaryfile in [('traces.jsonl','summary.csv'),('collision_traces.jsonl','collision_summary.csv')]:
        agg=defaultdict(lambda:np.zeros(5));counts=defaultdict(int)
        schedule={}
        with (OUT/tracefile).open() as f:
            for line in f:
                r=json.loads(line);key=(r['regime'],r['budget'],r['policy']);counts[key]+=1
                assert r['calls']==len(r['steps'])<=r['budget']
                assert r['correct']+r['wrong']+r['abstain']==1
                agg[key]+=np.array([r[m] for m in ['correct','wrong','abstain','calls','utility']])
                for step in r['steps']:
                    sk=(r['query_id'],r['regime'],r['seed'],step['engine'],step['attempt'])
                    value=(step['status'],step['value'],step['injected_fault'])
                    if sk in schedule:assert schedule[sk]==value
                    else:schedule[sk]=value
        for r in rows(summaryfile):
            key=r['regime'],int(r['budget']),r['policy']
            expected=agg[key]/counts[key]
            assert counts[key]==720
            assert np.allclose(expected,[float(r[m]) for m in ['correct','wrong','abstain','calls','utility']])
    summaries=rows('summary.csv')+rows('collision_summary.csv')
    index={(r['regime'],int(r['budget']),r['policy']):r for r in summaries}
    table('regime_table','Main fault interventions; labels are hidden from controllers.','tab:regimes','p{.20\\textwidth}p{.71\\textwidth}',r'Regime & Intervention',[
        r'Clean & No injection; each engine executes its ordinary computation.',
        r'Transient & SQLite first attempt raises an exception; a retry can succeed.',
        r'Persistent & Every SQLite attempt raises an exception; alternatives work.',
        r'Independent & Family-dependent, persistent per-engine corruption; distinct wrong offsets.',
        r'Shifted & Independent corruption probabilities doubled; offsets unchanged.',
        r'Correlated & One shared event adds the same offset to every engine response.'])
    labels=[('dev_fixed','Selected single engine'),('retry','Retry / switch / SQLite'),('agreement','Agreement / fitted gate'),('majority','Fixed majority')]
    body=[]
    for regime,display in [('independent','Independent'),('shifted','Doubled')]:
        for policy,label in labels:
            r=index[regime,3,policy]
            vals=[f"{100*float(r[m]):.1f}" for m in ['correct','wrong','abstain']]+[f"{float(r['calls']):.3f}"]
            body.append(' & '.join([display,label]+vals))
    table('main_table','Three-call results: percentages of correct, wrong, and abstained episodes.','tab:main','llrrrr',r'Faults & Policy & Correct & Wrong & Abstain & Calls',body)
    body=[]
    for regime,display in [('independent','M: Distinct, nominal'),('independent_collision','E: Colliding, nominal'),('shifted','M: Distinct, doubled'),('shifted_collision','E: Colliding, doubled'),('correlated','M: Shared event')]:
        a=index[regime,3,'agreement'];s=index[regime,3,'dev_fixed']
        vals=[f"{100*float(a[m]):.1f}" for m in ['correct','wrong','abstain']]+[f"{100*float(s['wrong']):.1f}"]
        body.append(' & '.join([display]+vals))
    table('collision_table','Agreement outcomes: main (M) versus exploratory (E) analyses.','tab:collision','lrrrr',r'Error model & Correct & Wrong & Abstain & Single wrong',body)
    # Bibliography is local to this study; no companion-paper dependency.
    bib=(PAPER/'references.bib').read_text()
    # Design at approximately the final Springer text width (4.8 inches),
    # so nominal figure fonts remain readable after inclusion in the paper.
    for font in Path('/System/Library/Fonts/Supplemental').glob('Times New Roman*.ttf'):
        font_manager.fontManager.addfont(str(font))
    available={f.name for f in font_manager.fontManager.ttflist}
    family='Times New Roman' if 'Times New Roman' in available else 'serif'
    plt.rcParams.update({'font.family':family,'font.size':10,'pdf.fonttype':42,
                         'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,1,figsize=(4.8,4.9),sharex=True,sharey=True,layout='constrained')
    for ax,regime,title in zip(axes,['independent','shifted'],['(a) Nominal independent faults','(b) Doubled independent faults']):
        for p,label,color in [('agreement','Agreement','#24649b'),('dev_fixed','Selected single','#b65d21')]:
            for metric,style in [('correct','o-'),('wrong','s--')]:
                ax.plot([1,2,3],[float(index[regime,k,p][metric]) for k in (1,2,3)],style,color=color,lw=1.6,markersize=5,label=label+': '+metric)
        ax.set(title=title,xticks=[1,2,3],ylim=(-.03,1.03),ylabel='Episode fraction')
        ax.grid(axis='y',alpha=.2)
    axes[1].set_xlabel('Hard invocation budget (K)')
    handles,legend_labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,legend_labels,ncol=2,fontsize=9,frameon=False,loc='outside lower center')
    fig.savefig(PAPER/'figures/budget_outcomes.pdf',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(4.8,3.7))
    fig.subplots_adjust(left=.12,right=.99,bottom=.29,top=.86)
    regimes=['independent','independent_collision','shifted','shifted_collision','correlated']
    for i,regime in enumerate(regimes):
        for j,p in enumerate(['agreement','dev_fixed']):
            r=index[regime,3,p];bottom=0
            for metric,color,label in [('correct','#45917b','Correct'),('wrong','#b84c42','Wrong'),('abstain','#c0c5cb','Abstained')]:
                value=float(r[metric]);ax.bar(i+(j-.5)*.32,value,width=.29,bottom=bottom,color=color,label=label if i==0 and j==0 else None)
                bottom+=value
    ax.set(xticks=range(5),xticklabels=['Distinct\nM','Colliding\nE','Distinct x2\nM','Colliding x2\nE','Shared\nM'],ylim=(0,1.05),ylabel='Episode fraction')
    ax.tick_params(axis='x',labelsize=9)
    ax.legend(ncol=3,frameon=False,fontsize=9,loc='lower center',bbox_to_anchor=(.5,1.01))
    fig.text(.53,.055,'Pairs: agreement (left), selected single (right).\nM: prospective main; E: exploratory extension.',ha='center',fontsize=9,linespacing=1.5)
    fig.savefig(PAPER/'figures/error_structure.pdf',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(4.8,2.55));ax.set(xlim=(0,10),ylim=(0,4.5));ax.axis('off')
    boxes=[(.1,2.45,2.35,1.5,'Controller','Query + budget'),(3.25,2.45,3.,1.5,'Real engines','SQLite / Python /\nNumPy'),(7.05,2.45,2.8,1.5,'Response','Status + value')]
    for x,y,w,h,title,sub in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.06',edgecolor='#28638d',facecolor='#f6f8fa'))
        ax.text(x+w/2,y+1.04,title,ha='center',fontsize=10,weight='bold')
        ax.text(x+w/2,y+.43,sub,ha='center',va='center',fontsize=9,linespacing=1.3)
    for start,end in [((2.55,3.2),(3.13,3.2)),((6.36,3.2),(6.93,3.2))]:
        ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','lw':1.1})
    ax.plot([8.4,8.4,1.25],[2.35,1.35,1.35],color='#333333',lw=1)
    ax.annotate('',xy=(1.25,2.35),xytext=(1.25,1.35),arrowprops={'arrowstyle':'->','lw':1.1})
    ax.text(5.,1.65,'Observed response history',ha='center',fontsize=9)
    ax.text(5.,.35,'Hidden: fault state and offline Decimal reference',ha='center',fontsize=9,color='#8b3c32')
    fig.savefig(PAPER/'figures/recovery_contract.pdf',bbox_inches='tight');plt.close(fig)
    main=(PAPER/'main.tex').read_text()
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\keywords',main,re.S).group(1)
    count=len(abstract.split());assert 150<=count<=250,count
    keys={k for block in re.findall(r'\\cite\{([^}]+)\}',main) for k in block.split(',')}
    bibkeys=set(re.findall(r'@\w+\{([^,]+),',bib));assert keys==bibkeys,(keys,bibkeys)
    assert '75.9' not in main and 'aaai2027' not in main
    report={'abstract_words':count,'references':len(keys),'main_episodes':116640,'extension_episodes':38880,'test_queries':72,'dev_queries':72,'new_study':True,'original_results_reused':False,'frozen_config_sha256':digest(OUT/'frozen_config.json'),'verified_summary_files':['summary.csv','collision_summary.csv']}
    (PAPER/'evidence_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified paired schedules, budgets, trace-derived tables and reference coverage:',report)
if __name__=='__main__':main()
