from pathlib import Path
import sys,json,datetime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'tmp/lab-deps'))
import paramiko
def connect():
    c=paramiko.SSHClient()
    known=ROOT/'infra/private/known_hosts'
    if known.exists(): c.load_host_keys(str(known))
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect('127.0.0.1',port=22022,username='andrey',key_filename=str(ROOT/'infra/private/id_ed25519'),look_for_keys=False,allow_agent=False,timeout=15)
    c.save_host_keys(str(known)); return c
def run(c,cmd):
    _,out,err=c.exec_command(cmd,timeout=180)
    result=out.read().decode(errors='replace')+err.read().decode(errors='replace')
    code=out.channel.recv_exit_status()
    return {'command':cmd,'exit_code':code,'output':result,'timestamp':datetime.datetime.now().astimezone().isoformat()}
if __name__=='__main__':
    c=connect()
    try:
        r=run(c,sys.argv[1] if len(sys.argv)>1 else 'hostnamectl; cloud-init status')
        print(json.dumps(r,ensure_ascii=False,indent=2))
    finally:c.close()
