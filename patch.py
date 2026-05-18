import re

with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. replace saveAll
saveAll_old = "function saveAll(silent){state.editable=captureEditable();state.socials=captureSocials();try{localStorage.setItem(SK,JSON.stringify(state));if(!silent)toast('All changes saved!','success')}catch(e){toast('Save failed - storage quota exceeded.','error')}}"
saveAll_new = """async function saveAll(silent){
  state.editable=captureEditable();state.socials=captureSocials();
  try{
    const res = await fetch('/api/data', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + sessionStorage.getItem('token') },
      body: JSON.stringify(state)
    });
    if(res.ok) { if(!silent) toast('All changes saved!','success'); }
    else { if(!silent) toast('Failed to save. Unauthorized?','error'); }
  }catch(e){ toast('Save failed.','error'); }
}"""
content = content.replace(saveAll_old, saveAll_new)

# 2. replace loadSaved
loadSaved_old = "function loadSaved(){try{const r=localStorage.getItem(SK);if(!r)return;state=Object.assign(JSON.parse(JSON.stringify(D)),JSON.parse(r))}catch(e){}}"
loadSaved_new = """async function loadSaved(){
  try{
    const res = await fetch('/api/data');
    if(res.ok) {
      const data = await res.json();
      state = Object.assign(JSON.parse(JSON.stringify(D)), data);
    }
  }catch(e){ console.error(e); }
}"""
content = content.replace(loadSaved_old, loadSaved_new)

# 3. Add uploadFiles
fileToData_old = "function fileToDataUrl(file){return new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(file)})}"
fileToData_new = """function fileToDataUrl(file){return new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(file)})}
async function uploadFiles(files) {
  const fd = new FormData();
  for(let f of files) fd.append('files', f);
  const res = await fetch('/api/upload', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') },
    body: fd
  });
  if(res.ok) {
    const data = await res.json();
    return data.urls;
  }
  throw new Error('Upload failed');
}"""
content = content.replace(fileToData_old, fileToData_new)

# 4. replace loginForm
login_old = """$('#loginForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const h=await sha256(pw.value);
  if(h===PH){
    ov.classList.remove('open');
    setAdminMode(true);
    toast('Welcome back. Edit mode enabled.','success');
    renderAll();
  } else {
    er.classList.add('vis');
    md.classList.remove('shake');
    void md.offsetWidth;
    md.classList.add('shake');
  }
});"""
login_new = """$('#loginForm').addEventListener('submit',async e=>{
  e.preventDefault();
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pw.value })
    });
    if(res.ok) {
      const data = await res.json();
      sessionStorage.setItem('token', data.token);
      ov.classList.remove('open');
      setAdminMode(true);
      toast('Welcome back. Edit mode enabled.','success');
      renderAll();
    } else { throw new Error(); }
  } catch(e) {
    er.classList.add('vis');
    md.classList.remove('shake');
    void md.offsetWidth;
    md.classList.add('shake');
  }
});"""
content = content.replace(login_old, login_new)

# 5. replace btnLogout
logout_old = "$('#btnLogout').addEventListener('click',async()=>{if(!(await confirmAction('Logout?','Unsaved changes will be lost.')))return;setAdminMode(false);location.reload()});"
logout_new = "$('#btnLogout').addEventListener('click',async()=>{if(!(await confirmAction('Logout?','Unsaved changes will be lost.')))return;setAdminMode(false);sessionStorage.removeItem('token');location.reload()});"
content = content.replace(logout_old, logout_new)

# 6. replace photoInput
photo_old = "$('#photoInput').addEventListener('change',async e=>{const file=e.target.files&&e.target.files[0];if(!file)return;state.profilePhoto=await fileToDataUrl(file);applyPhoto();toast('Photo updated','info')});"
photo_new = "$('#photoInput').addEventListener('change',async e=>{const file=e.target.files&&e.target.files[0];if(!file)return;try{const urls=await uploadFiles([file]);state.profilePhoto=urls[0];applyPhoto();toast('Photo updated. Click Save to persist.','info')}catch(e){toast('Failed','error')}});"
content = content.replace(photo_old, photo_new)

# 7. replace galleryInput
gallery_old = "$('#galleryInput').addEventListener('change',async e=>{const files=[...e.target.files||[]];for(const f of files){state.gallery.push({src:await fileToDataUrl(f),caption:f.name.replace(/\.[^.]+$/,'')})}renderGallery();if(files.length)toast(files.length+' photo(s) added','info')});"
gallery_new = "$('#galleryInput').addEventListener('change',async e=>{const files=[...e.target.files||[]];if(!files.length)return;try{const urls=await uploadFiles(files);urls.forEach((u,i)=>state.gallery.push({src:u,caption:files[i].name.replace(/\.[^.]+$/,'')}));renderGallery();toast(files.length+' photo(s) added','info')}catch(e){toast('Failed','error')}});"
content = content.replace(gallery_old, gallery_new)

# 8. replace contactForm
contact_old = "$('#contactForm').addEventListener('submit',e=>{e.preventDefault();toast('Thank you! Message queued (prototype).','success');e.target.reset()});"
contact_new = """$('#contactForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const d = { name: $('#cName').value, email: $('#cEmail').value, subject: $('#cSubject').value, message: $('#cMsg').value };
  try{
    const res = await fetch('/api/contact', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(d) });
    if(res.ok) { toast('Message sent successfully!','success'); e.target.reset(); }
    else toast('Failed to send','error');
  } catch(e) { toast('Failed to send','error'); }
});"""
content = content.replace(contact_old, contact_new)

# 9. replace init()
init_old = """function init(){
$('#ftYear').textContent=new Date().getFullYear();
loadSaved();"""
init_new = """async function init(){
$('#ftYear').textContent=new Date().getFullYear();
await loadSaved();"""
content = content.replace(init_old, init_new)

with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patch applied successfully.")
