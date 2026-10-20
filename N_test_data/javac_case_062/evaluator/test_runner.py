"""Run protected direct control and target binding in separate JVMs."""
import json
import subprocess
import sys
from pathlib import Path
repo,out=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()
out.mkdir(parents=True,exist_ok=True)
source=repo/'modules/lwjgl/llvm/src/test/java/org/lwjgl/llvm/ClangCStringRegressionTest.java'
cp=':'.join(str(repo/p) for p in ('bin/classes/lwjgl/core','bin/classes/lwjgl/llvm','bin/libs/java/*'))
classes=repo/'bin/classes/test'
classes.mkdir(parents=True,exist_ok=True)
with (out/'test-compilation.private.log').open('wb') as f:
    c=subprocess.run(['javac','--release','11','-cp',cp,'-d',str(classes),str(source)],cwd=repo,stdout=f,stderr=subprocess.STDOUT)
if c.returncode:
    print(json.dumps({'phase':'test_compilation','exit_code':c.returncode,'infrastructure_error':False,'tests':{}}))
    sys.exit(1)
native=repo/'bin/libs/native'
compiled=native/'linux/x64'
if not (compiled/'org/lwjgl/liblwjgl.so').is_file() or not (compiled/'org/lwjgl/llvm/liblwjgl_llvm.so').is_file():
    print(json.dumps({'phase':'native_preflight','infrastructure_error':True,'tests':{}}))
    sys.exit(2)
results={}
for mode in ('direct','binding'):
    cmd=['java','-XX:ErrorFile='+str(out/'hs_err-%p.log'),'-Dorg.lwjgl.librarypath='+str(native),'-Dorg.lwjgl.llvm.clang.libname=/usr/lib/llvm-14/lib/libclang.so','-cp',str(classes)+':'+cp,'org.lwjgl.llvm.ClangCStringRegressionTest',mode]
    with (out/(mode+'.private.log')).open('wb') as f:
        try: process=subprocess.run(cmd,cwd=repo,stdout=f,stderr=subprocess.STDOUT,timeout=120)
        except subprocess.TimeoutExpired:
            print(json.dumps({'phase':'call','category':'timeout','infrastructure_error':True,'tests':results}))
            sys.exit(2)
    status='passed' if process.returncode==0 else 'failed' if process.returncode==1 else 'error'
    results['org.lwjgl.llvm.ClangCStringRegressionTest::'+mode]={'status':status,'exit_code':process.returncode}
report={'oracle_type':'runtime_behavior','phase':'call','infrastructure_error':any(v['status']=='error' for v in results.values()),'tests':results}
(out/'sanitized_results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
sys.exit(2 if report['infrastructure_error'] else 0 if all(v['status']=='passed' for v in results.values()) else 1)
