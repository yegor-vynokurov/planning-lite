import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE_PLAN = Path('docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md')
AMENDMENT = Path('docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md')
CHECKER = Path('docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-ENTRY-AUTHORITY-CHECK-v1.py')
READINESS = Path('docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-FORMAL-READINESS-VERDICT-v2.md')
T01_BASELINE = Path('.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_FIFTH_PLAN_BASELINE.json')
EXECUTION = Path('.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION.json')
BASE_PLAN_SHA = 'B38B977FD6858597380DD2DB7D7685E7272BC3881776A69370C4E615E671ABEC'
PASS_VERDICT = 'PASS_INDEPENDENT_CUMULATIVE_EXECUTABLE_CAPTURE_AND_SEAL_HANDOFF_REPAIR_V6'
OLD14 = {'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CHANGE-DEFINITION-v1.md': '56DFD7C6B7610262A1DD61BCE7771B320F645DAB901EC90DB6B3B3685815611B', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-ACTIVATION-v1.md': 'F21B8DC151507EB0B937EEFE36CFD35012305808174C3067A4ABC9D0C7C1A53B', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v1.md': '2C5FFB3D1902424ACBCCA41505CF5113E6C7365AD632831B80C859795B249DA6', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v1.md': 'DA55C416AFCC4933D05F2459773C56CAA10C639242AA71D1040A7CE9C671E84B', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v2.md': 'E1D979F2E5219A2042611033455E95F0E2024B53741D048D08EBFD938FB5EABA', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v2.md': '004331DF581880BDBA57AE8FD782132EDCED2D841829E5B6BF4A08BC7E4D8A93', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md': '127F19F505527B622BF3F45D6AA83D432B8F5BE93BD5856CE516C4CEE34BE332', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-v1.md': '2CDE29CA69D29FF3FC327B82C05EAF6A3CCB54143F1B30B8953B2FC07BFAD4C7', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v1.md': 'AC012052CCCE524FD9770EEEF94D87181C320ABE0D863C2DC930928740F9B886', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v1.md': '59797EFD9F2FDDA8E7A1B4A478F7985A8E43C66956F5BFBD3420F0F7531511D4', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v2.md': '444BC880E112F070FB5A3E6B29B3ED1FDD35DDF5E637905A8AB4094D0A9AC510', 'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v2.md': '33597F3B40E1B06F8D7B6EF601764100DD7C1F7E8CC64635F03C8171759325F1', 'docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-CLOSURE-v1.md': '40D998EF9FE11EF5D56A927917208D4711FD860BA4A4121FF5573B96553973F2', 'docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CLOSURE-v1.md': '3E96782EC6F70DB5F6835CDEB90F4E2EE2AEF4E92AC8CC21F463E639CC101A6E'}
PLANNED = ['src/planning_lite/governed_executor.py', 'src/planning_lite/operation_lifecycle.py', 'src/planning_lite/context.py', 'src/planning_lite/cli.py', 'template/.planning/adapters/codex/README.md', 'tests/test_governed_executor.py', 'tests/test_operation_lifecycle.py', 'tests/test_cli.py', 'tests/test_context_resume.py', 'tests/test_run_receipts.py', 'tests/test_system_traversability.py', 'template/.planning/framework/SHA256SUMS.txt']
BASELINE_KEYS = {'schema_version','entry_head','entry_index_empty','implementation_authority_commit','authorized_paths','preexisting_dirty_paths','central_status_porcelain_v1'}
PATH_RECORD_KEYS = {'path','exists','kind','sha256','git_state','status_code'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def run_git(*args, text=True, check=True):
    cp = subprocess.run(['git', *args], text=text, capture_output=True)
    if check and cp.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return cp.stdout.strip() if text else cp.stdout


def field(text, key):
    m = re.findall(rf'(?m)^{re.escape(key)}: (.+)$', text)
    assert len(m) == 1, key
    return m[0].strip()


def block(text, start, end):
    m = re.findall(rf'(?ms)^{re.escape(start)}\n(.*?)^{re.escape(end)}$', text)
    assert len(m) == 1, start
    return m[0]


def show(commit, path):
    return run_git('show', f'{commit}:{path.as_posix()}', text=False)


def commit_parents(commit):
    parts = run_git('rev-list', '--parents', '-n', '1', commit).split()
    assert parts and parts[0] == commit
    return parts[1:]


def commit_paths(commit):
    parents = commit_parents(commit)
    assert len(parents) == 1, (commit, parents)
    return sorted(x for x in run_git('diff','--name-only',parents[0],commit).splitlines() if x)


def assert_old14_tree(commit):
    for p, expected in OLD14.items():
        assert sha(show(commit, Path(p))) == expected, p


def commit_touches_planned(commit):
    parents = commit_parents(commit)
    if not parents:
        changed = set(x for x in run_git('diff-tree','--root','--no-commit-id','--name-only','-r',commit).splitlines() if x)
        return sorted(changed.intersection(PLANNED))
    touched=set()
    for parent in parents:
        touched.update(x for x in run_git('diff','--name-only',parent,commit,'--',*PLANNED).splitlines() if x)
    return sorted(touched)


def planned_touch_history(authority_commit, entry_head):
    assert subprocess.run(['git','merge-base','--is-ancestor',authority_commit,entry_head],capture_output=True).returncode == 0
    offenders=[]
    for commit in [x for x in run_git('rev-list','--topo-order',f'{authority_commit}..{entry_head}').splitlines() if x]:
        touched=commit_touches_planned(commit)
        if touched:
            offenders.append({'commit':commit,'paths':touched})
    return offenders


def status_lines():
    cp=subprocess.run(['git','-c','core.quotepath=false','status','--porcelain=v1','--untracked-files=all'],text=True,capture_output=True)
    assert cp.returncode == 0, cp.stderr
    return [x for x in cp.stdout.splitlines() if x]


def status_path(line):
    assert len(line) >= 3, line
    p=line[3:]
    if ' -> ' in p:
        p=p.split(' -> ',1)[1]
    return p


def status_code_for(rel, lines):
    for line in lines:
        if status_path(line) == rel:
            return line[:2]
    return '  '


def planned_worktree_status():
    planned=set(PLANNED)
    return [x for x in status_lines() if status_path(x) in planned]


def assert_index_empty():
    assert subprocess.run(['git','diff','--cached','--quiet']).returncode == 0, 'index is not empty'


def read_entry(rel, lines, entry_head):
    p=Path(rel)
    code=status_code_for(rel, lines)
    if p.is_file():
        exists=True; kind='file'; digest=sha(p.read_bytes())
    elif p.is_dir():
        exists=True; kind='directory'; digest=None
    else:
        exists=False; kind='absent'; digest=None
    tracked=subprocess.run(['git','ls-files','--error-unmatch','--',rel],capture_output=True).returncode == 0
    if not exists and tracked:
        cp=subprocess.run(['git','show',f'{entry_head}:{rel}'],capture_output=True)
        if cp.returncode == 0:
            digest=sha(cp.stdout)
    if code == '??':
        git_state='untracked'
    elif code != '  ':
        git_state='tracked'
    elif tracked:
        git_state='tracked-clean'
    else:
        ignored=subprocess.run(['git','check-ignore','--quiet','--',rel],capture_output=True).returncode == 0
        git_state='ignored' if ignored else 'absent'
    return {'path':rel,'exists':exists,'kind':kind,'sha256':digest,'git_state':git_state,'status_code':code}


def parse_amendment(raw):
    text=raw.decode('utf-8').replace('\r\n','\n')
    bindings=block(text,'PLAN_AMENDMENT_BINDINGS_BEGIN','PLAN_AMENDMENT_BINDINGS_END')
    cumulative=block(text,'CANONICAL_CUMULATIVE_AMENDMENT_BEGIN','CANONICAL_CUMULATIVE_AMENDMENT_END').encode('utf-8')
    return bindings,cumulative


def parse_readiness(raw):
    text=raw.decode('utf-8').replace('\r\n','\n')
    return block(text,'READINESS_V2_BINDINGS_BEGIN','READINESS_V2_BINDINGS_END')


def verify_planning_authority(A, require_local_sources=False):
    assert re.fullmatch(r'[0-9a-f]{40}',A)
    expected=sorted([AMENDMENT.as_posix(),CHECKER.as_posix()])
    assert commit_paths(A) == expected, commit_paths(A)
    assert sha(show(A,BASE_PLAN)) == BASE_PLAN_SHA
    assert_old14_tree(A)
    amendment_raw=show(A,AMENDMENT); checker_raw=show(A,CHECKER)
    ab,cumulative=parse_amendment(amendment_raw)
    assert field(ab,'PLAN_AMENDMENT_STATUS') == 'APPROVED_BY_OWNER'
    assert field(ab,'PREDECESSOR_PLAN_SHA256') == BASE_PLAN_SHA
    assert field(ab,'CUMULATIVE_AMENDMENT_SHA256') == sha(cumulative)
    assert field(ab,'ENTRY_CHECKER_SHA256') == sha(checker_raw)
    if require_local_sources:
        candidate=Path(field(ab,'SOURCE_REPAIR_V6_CANDIDATE_PATH'))
        review=Path(field(ab,'SOURCE_REPAIR_V6_PASS_REVIEW_PATH'))
        cr=candidate.read_bytes(); rr=review.read_bytes()
        assert sha(cr) == field(ab,'SOURCE_REPAIR_V6_CANDIDATE_ORDINARY_SHA256')
        assert sha(rr) == field(ab,'SOURCE_REPAIR_V6_PASS_REVIEW_ORDINARY_SHA256')
        ct=cr.decode('utf-8').replace('\r\n','\n'); rt=rr.decode('utf-8').replace('\r\n','\n')
        source_cumulative=block(ct,'SOURCE_CUMULATIVE_AMENDMENT_BEGIN','SOURCE_CUMULATIVE_AMENDMENT_END').encode('utf-8')
        source_checker=block(ct,'SOURCE_ENTRY_CHECKER_BEGIN','SOURCE_ENTRY_CHECKER_END').encode('utf-8')
        assert source_cumulative == cumulative
        assert source_checker == checker_raw
        assert field(rt,'REVIEW_VERDICT') == PASS_VERDICT
        assert field(rt,'REVIEWED_CANDIDATE_ORDINARY_SHA256') == sha(cr)
        assert field(rt,'SOURCE_CUMULATIVE_AMENDMENT_SHA256') == sha(source_cumulative)
        assert field(rt,'SOURCE_ENTRY_CHECKER_SHA256') == sha(source_checker)
    return {'planning_authority_commit':A,'plan_amendment_sha256':sha(amendment_raw),'entry_checker_sha256':sha(checker_raw),'source_candidate_sha256':field(ab,'SOURCE_REPAIR_V6_CANDIDATE_ORDINARY_SHA256'),'source_review_sha256':field(ab,'SOURCE_REPAIR_V6_PASS_REVIEW_ORDINARY_SHA256'),'cumulative_amendment_sha256':field(ab,'CUMULATIVE_AMENDMENT_SHA256')}


def verify_readiness_worktree(A):
    assert run_git('rev-parse','HEAD') == A
    proof=verify_planning_authority(A,True)
    assert AMENDMENT.read_bytes() == show(A,AMENDMENT)
    assert CHECKER.read_bytes() == show(A,CHECKER)
    assert BASE_PLAN.read_bytes() == show(A,BASE_PLAN)
    for p,e in OLD14.items(): assert sha(Path(p).read_bytes()) == e, p
    assert_index_empty(); assert planned_worktree_status() == [], planned_worktree_status()
    rb=parse_readiness(READINESS.read_bytes())
    assert field(rb,'FORMAL_READINESS') == 'READY'
    assert field(rb,'IMPLEMENTATION_AUTHORIZED') == 'NO'
    assert field(rb,'PLANNING_AUTHORITY_COMMIT').lower() == A
    assert field(rb,'BOUND_PREDECESSOR_PLAN_SHA256') == BASE_PLAN_SHA
    assert field(rb,'BOUND_PLAN_AMENDMENT_SHA256') == proof['plan_amendment_sha256']
    assert field(rb,'BOUND_ENTRY_CHECKER_SHA256') == proof['entry_checker_sha256']
    assert field(rb,'BOUND_REPAIR_V6_CANDIDATE_ORDINARY_SHA256') == proof['source_candidate_sha256']
    assert field(rb,'BOUND_REPAIR_V6_PASS_REVIEW_ORDINARY_SHA256') == proof['source_review_sha256']
    assert field(rb,'BOUND_CUMULATIVE_AMENDMENT_SHA256') == proof['cumulative_amendment_sha256']
    assert field(rb,'MATERIAL_BLOCKER_COUNT') == '0'
    proof['readiness_sha256']=sha(READINESS.read_bytes())
    return proof


def verify_committed_authority(R):
    assert re.fullmatch(r'[0-9a-f]{40}',R)
    run_git('cat-file','-e',R+'^{commit}')
    readiness_raw=show(R,READINESS); rb=parse_readiness(readiness_raw)
    assert field(rb,'FORMAL_READINESS') == 'READY'
    assert field(rb,'IMPLEMENTATION_AUTHORIZED') == 'NO'
    A=field(rb,'PLANNING_AUTHORITY_COMMIT').lower()
    assert run_git('rev-parse',R+'^') == A
    assert commit_paths(R) == [READINESS.as_posix()]
    proof=verify_planning_authority(A,False)
    assert field(rb,'BOUND_PREDECESSOR_PLAN_SHA256') == BASE_PLAN_SHA
    assert field(rb,'BOUND_PLAN_AMENDMENT_SHA256') == proof['plan_amendment_sha256']
    assert field(rb,'BOUND_ENTRY_CHECKER_SHA256') == proof['entry_checker_sha256']
    assert field(rb,'BOUND_REPAIR_V6_CANDIDATE_ORDINARY_SHA256') == proof['source_candidate_sha256']
    assert field(rb,'BOUND_REPAIR_V6_PASS_REVIEW_ORDINARY_SHA256') == proof['source_review_sha256']
    assert field(rb,'BOUND_CUMULATIVE_AMENDMENT_SHA256') == proof['cumulative_amendment_sha256']
    assert field(rb,'MATERIAL_BLOCKER_COUNT') == '0'
    proof['readiness_sha256']=sha(readiness_raw); proof['implementation_authority_commit']=R
    return proof


def verify_entry(R, entry_head='HEAD', require_clean=True):
    R=R.lower(); entry_head=run_git('rev-parse',entry_head)
    assert subprocess.run(['git','merge-base','--is-ancestor',R,entry_head],capture_output=True).returncode == 0
    proof=verify_committed_authority(R)
    offenders=planned_touch_history(R,entry_head); assert offenders == [], offenders
    assert_index_empty()
    if require_clean:
        s=planned_worktree_status(); assert s == [], s
    assert BASE_PLAN.read_bytes() == show(R,BASE_PLAN)
    assert AMENDMENT.read_bytes() == show(R,AMENDMENT)
    assert CHECKER.read_bytes() == show(R,CHECKER)
    assert READINESS.read_bytes() == show(R,READINESS)
    for p,e in OLD14.items(): assert sha(Path(p).read_bytes()) == e, p
    proof['entry_head']=entry_head
    return proof


def capture_baseline(R, output):
    proof=verify_entry(R,'HEAD',True)
    entry_head=proof['entry_head']; lines=status_lines(); dirty=sorted({status_path(x) for x in lines})
    manifest={'schema_version':1,'entry_head':entry_head,'entry_index_empty':True,'implementation_authority_commit':R.lower(),'authorized_paths':[read_entry(p,lines,entry_head) for p in PLANNED],'preexisting_dirty_paths':[read_entry(p,lines,entry_head) for p in dirty],'central_status_porcelain_v1':lines}
    raw=(json.dumps(manifest,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8')
    output.parent.mkdir(parents=True,exist_ok=True); output.write_bytes(raw)
    reread=json.loads(output.read_text(encoding='utf-8'))
    assert reread == manifest
    seal={'schema_version':1,'implementation_authority_commit':R.lower(),'entry_head':entry_head,'t01_baseline_sha256':sha(raw)}
    return seal


def parse_seal(raw):
    seal=json.loads(raw)
    assert set(seal) == {'schema_version','implementation_authority_commit','entry_head','t01_baseline_sha256'}
    assert seal['schema_version'] == 1
    assert re.fullmatch(r'[0-9a-f]{40}',seal['implementation_authority_commit'])
    assert re.fullmatch(r'[0-9a-f]{40}',seal['entry_head'])
    assert re.fullmatch(r'[0-9A-F]{64}',seal['t01_baseline_sha256'])
    return seal


def replay_baseline(entry_seal_json):
    seal=parse_seal(entry_seal_json)
    raw=T01_BASELINE.read_bytes(); assert sha(raw) == seal['t01_baseline_sha256']
    data=json.loads(raw.decode('utf-8'))
    assert set(data) == BASELINE_KEYS
    assert data['schema_version'] == 1 and data['entry_index_empty'] is True
    assert data['implementation_authority_commit'] == seal['implementation_authority_commit']
    assert data['entry_head'] == seal['entry_head']
    assert len(data['authorized_paths']) == len(PLANNED)
    assert [x['path'] for x in data['authorized_paths']] == PLANNED
    assert all(set(x) == PATH_RECORD_KEYS for x in data['authorized_paths']+data['preexisting_dirty_paths'])
    assert run_git('rev-parse','HEAD') == seal['entry_head']
    proof=verify_entry(seal['implementation_authority_commit'],seal['entry_head'],False)
    proof['t01_baseline_sha256']=seal['t01_baseline_sha256']
    return proof,data,seal


def verify_boundary(entry_seal_json):
    proof,data,seal=replay_baseline(entry_seal_json)
    lines=status_lines(); current_dirty=sorted({status_path(x) for x in lines})
    pre=[x['path'] for x in data['preexisting_dirty_paths']]
    unknown=sorted(set(current_dirty)-set(PLANNED)-set(pre)); assert unknown == [], unknown
    after={p:read_entry(p,lines,seal['entry_head']) for p in pre}
    for before in data['preexisting_dirty_paths']:
        assert after[before['path']] == before, (before,after[before['path']])
    audit={'planned_product_path_count':len(PLANNED),'unknown_changed_paths':[],'preexisting_dirty_preserved':True,'index_empty':True}
    proof['mutation_audit']=audit; proof['preexisting_dirty_path_count']=len(pre)
    return proof,audit


def validate_receipts(items,prefix,count):
    assert len(items) == count
    for i,item in enumerate(items,1):
        ident=f'{prefix}-{i:02d}'
        key='task_id' if prefix=='T' else 'verification_id'
        assert item == {key:ident,'status':'PASS','evidence_ref':f'#/{"task_receipts" if prefix=="T" else "verification_receipts"}/{i-1}'}


def verify_final(entry_seal_json, execution):
    proof,audit=verify_boundary(entry_seal_json)
    data=json.loads(execution.read_text(encoding='utf-8'))
    assert set(data) == {'schema_version','entry_identity','authority_identity','task_receipts','verification_receipts','acceptance_result','closure_result','mutation_audit','change_boundaries','terminal'}
    assert data['schema_version'] == 1
    assert data['entry_identity'] == {'head':proof['entry_head'],'index_empty':True,'preexisting_dirty_path_count':proof['preexisting_dirty_path_count'],'t01_baseline_sha256':proof['t01_baseline_sha256']}
    assert data['authority_identity'] == {'predecessor_plan_sha256':BASE_PLAN_SHA,'plan_amendment_sha256':proof['plan_amendment_sha256'],'entry_checker_sha256':proof['entry_checker_sha256'],'planning_authority_commit':proof['planning_authority_commit'],'readiness_sha256':proof['readiness_sha256'],'implementation_authority_commit':proof['implementation_authority_commit']}
    validate_receipts(data['task_receipts'],'T',12); validate_receipts(data['verification_receipts'],'V',26)
    assert data['acceptance_result'] == {'total':52,'mapped':52,'unmapped':0,'weak':0}
    assert data['closure_result'] == {'total':20,'mapped':20,'unmapped':0,'weak':0,'v2_overlays':9}
    assert data['mutation_audit'] == audit
    assert data['change_boundaries'] == {'change_2':'BLOCKED / VALID / PAUSED','change_3':'NOT_ABSORBED','major_pl09_next_slice_gate':'PRESERVED / UNCONSUMED'}
    assert data['terminal'] == {'verdict':'PASS_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION','implementation':'COMPLETE','formal_readiness_rerun_during_implementation':False}
    proof['execution_receipt_sha256']=sha(execution.read_bytes())
    return proof


def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='mode',required=True)
    p=sub.add_parser('readiness'); p.add_argument('--planning-authority-commit',required=True)
    p=sub.add_parser('entry'); p.add_argument('--authority-commit',required=True); p.add_argument('--entry-head',default='HEAD')
    p=sub.add_parser('capture'); p.add_argument('--authority-commit',required=True); p.add_argument('--output',default=T01_BASELINE.as_posix())
    p=sub.add_parser('boundary'); p.add_argument('--entry-seal-json',required=True)
    p=sub.add_parser('final'); p.add_argument('--entry-seal-json',required=True); p.add_argument('--execution',default=EXECUTION.as_posix())
    ns=ap.parse_args()
    if ns.mode=='readiness': result=verify_readiness_worktree(ns.planning_authority_commit.lower())
    elif ns.mode=='entry': result=verify_entry(ns.authority_commit.lower(),ns.entry_head,True)
    elif ns.mode=='capture': result=capture_baseline(ns.authority_commit.lower(),Path(ns.output))
    elif ns.mode=='boundary': result=verify_boundary(ns.entry_seal_json)[0]
    else: result=verify_final(ns.entry_seal_json,Path(ns.execution))
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__': main()
