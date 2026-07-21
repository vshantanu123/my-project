#### PGP-Illinois Institute of Technology, Edureka ---> Capstone Project

### Setup + Install

**From Astral-CLI-------> Install uv**
```
https://docs.astral.sh/uv/getting-started/installation/#cargo
```

**From git-repository------->** 
    Clone 
        1. my-project 
        2. my-project-ui
    Optional: 
        1. my-project-extra
    
```
git clone https://github.com/vshantanu123/my-project.git
```
**And** 
```
git clone https://github.com/vshantanu123/my-project-ui.git
```
**optional for results/ files to upload/ logs to see etc.**
```
https://github.com/vshantanu123/my-project-extra.git
```
**In Terminal, change dir to project dir**
```
uv venv .venv
```
**Activate Virtual Environment**
```
.venv\Scripts\activate
```
**my-project---> Install all the dependencies**
```
uv sync
```
**my-project-ui---> Install all the dependencies**
```
npm install
```

**RUN FastAPI/Python Backend Application by (default http://localhost:8000)**
```
fastapi run main.py
```

**RUN React/Vite Front End Application by (default http://localhost:5173)**
```
npx vite
```