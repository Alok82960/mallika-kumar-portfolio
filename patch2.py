import re

with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update saveAll fetch
saveAll_old = "'Authorization': 'Bearer ' + sessionStorage.getItem('token')"
saveAll_new = "'Content-Type': 'application/json'"
js = js.replace(saveAll_old, saveAll_new)
js = js.replace("body: JSON.stringify(state)", "body: JSON.stringify(state),\n      credentials: 'include'")

# 2. Update uploadFiles fetch
upload_old = "headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') }"
upload_new = "credentials: 'include'"
js = js.replace(upload_old, upload_new)

# 3. Update login fetch
login_old = """if(res.ok) {
      const data = await res.json();
      sessionStorage.setItem('token', data.token);"""
login_new = """if(res.ok) {"""
js = js.replace(login_old, login_new)

# 4. Update logout logic
logout_old = "sessionStorage.removeItem('token');location.reload()"
logout_new = "await fetch('/api/logout', { method: 'POST', credentials: 'include' }); location.reload()"
js = js.replace(logout_old, logout_new)

with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\main.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Patched main.js")
