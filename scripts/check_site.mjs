import fs from 'node:fs'
import path from 'node:path'
import { stepSequence } from '../docs/.vitepress/theme/step-model.mjs'
const root=path.resolve(import.meta.dirname,'..')
const dist=path.join(root,'docs/.vitepress/dist')
const pages=fs.readdirSync(path.join(root,'docs')).filter(f=>f.endsWith('.md')).map(f=>f.replace('.md','.html'))
const results=[]
for(const name of pages){
  const full=path.join(dist,name)
  if(!fs.existsSync(full))throw new Error('Missing rendered page '+name)
  const html=fs.readFileSync(full,'utf8')
  if(/data-mjx-error|<merror|class="mjx-merror"/.test(html))throw new Error('MathJax error in '+name)
  if(name!=='index.html'&&!/<h1[^>]*>/.test(html))throw new Error('No readable SSR content '+name)
  if(name==='03-functions.html'&&!html.includes('<mjx-container'))throw new Error('Math not rendered to SSR SVG')
  if(name==='09-unconstrained.html'&&!html.includes('误差乘数'))throw new Error('Interaction lacks SSR fallback')
  results.push(name)
}
const expected=JSON.parse(fs.readFileSync(path.join(root,'results/experiments.json'),'utf8')).steps
for(const [eta,seq]of Object.entries(expected)){
  const actual=stepSequence(Number(eta))
  actual.forEach((p,i)=>{if(Math.abs(p.x-seq[i].x)>1e-12)throw new Error('JS/Python step model mismatch')})
}
const release=JSON.parse(fs.readFileSync(path.join(dist,'release.json'),'utf8'))
fs.writeFileSync(path.join(root,'results/site-checks.json'),JSON.stringify({status:'passed',rendered_pages:results.length,math:'SSR SVG, no reported errors',js_python_agreement:true,release},null,2))
console.log('Verified '+results.length+' SSR pages, MathJax output, and JS/Python step model agreement.')
