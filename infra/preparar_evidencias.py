from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1];dest=root/'evidencias'
results=json.loads((dest/'resultados.json').read_text(encoding='utf-8'))
for r in results:
    output=r['output'].replace('\r','').replace('🖴','[VM]')
    page='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Registro de ejecución SSH</title><style>
body{margin:0;padding:34px 60px;background:#edf0f2;color:#192631;font-family:Arial,sans-serif}header{border-top:6px solid #702726;padding-top:18px;display:flex;justify-content:space-between}h1{font-size:26px;margin:10px 0}p{font-size:13px;color:#55616b}.badge{padding:7px 13px;background:#dcebdc;color:#23482a;font-size:12px;border-radius:4px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;border:1px solid #d1d8dc;border-radius:6px;padding:24px;font:14px/1.45 Consolas,monospace;margin-top:22px}footer{font-size:12px;color:#55616b;margin-top:15px}details{font-size:12px;margin-top:15px}code{display:block;white-space:pre-wrap;padding:15px;background:white}
</style><header><div><p>LABORATORIO UNMSM / UBUNTU SERVER</p><h1>'''+html.escape(r['title'])+'''</h1></div><div><span class="badge">EJECUTADO · CÓDIGO '''+str(r['exit_code'])+'''</span></div></header><p>Origen: sesión SSH de andrey@web-unmsm · '''+html.escape(r['timestamp'])+'''</p><details><summary>Ver comando ejecutado</summary><code>'''+html.escape(r['command'])+'''</code></details><pre>'''+html.escape(output)+'''</pre><footer>Visor de transcripción real guardada en resultados.json. No es una consola interactiva.</footer></html>'''
    (dest/(r['slug']+'.html')).write_text(page,encoding='utf-8')
print('Ocho transcripciones listas para capturar en el navegador.')
