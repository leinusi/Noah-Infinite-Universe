# Noah Infinite Universe Web App  
**October 2023 – December 2023**  

> “We are all scattered stardust—and Noah gathers those particles into brilliant constellations.”  
> With Noah Infinite Universe, your face becomes the ink, and the cosmos becomes the pen, painting an epic that’s uniquely yours.  
<img width="1230" alt="fec11eb453a1179a9b08b5898ba1597" src="https://github.com/user-attachments/assets/00836bef-b39e-4c91-881b-0737b37d85ce" />

---

## 🚀 Project Overview  
Noah Infinite Universe is a single-page web application (SPA) that harnesses cutting-edge AI to generate a 20-panel “comic strip” starring you. Simply upload **5 personal photos**, enter your desired story theme, and watch a Vue 3 + TypeScript frontend talk to the backend via WebSocket in real-time—then deliver a fully AI-crafted, high-fidelity narrative in images.  

## ✨ Key Features  
1. **Personalized Style Transfer**  
   - Fine-tune Stable Diffusion v1.5 with LoRA (Low-Rank Adaptation) on your 5 uploaded photos  
   - Achieve ultra-realistic face swaps using the EasyFace plugin  

2. **Real-Time Progress & Interaction**  
   - Vue 3 + TypeScript SPA communicates over WebSocket  
   - Live progress indicators for queue position, generation status, and instant previews  

3. **Scalable, Distributed Backend**  
   - **API Layer**: Django REST Framework  
   - **Data Storage**: PostgreSQL for user profiles and task metadata  
   - **Task Queue**: Celery + RabbitMQ  
   - **Cache**: Redis for intermediate results  

4. **AI Pipeline & Deployment**  
   - **Image Generation**: Dockerized EasyFace (Stable Diffusion + ControlNet)  
   - **Scripted Prompts**: GLM3 local service splits story text into 20 prompts  
   - **Reverse Proxy & Security**: Nginx + HTTPS  
   - **Monitoring**: Prometheus + Grafana for uptime and performance  

## ⚙️ Installation & Run  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/leinusi/Noah-Infinite-Universe.git
   cd Noah-Infinite-Universe
2. **Start the backend server**  
   ```bash
   cd NoahAI_web_serve
   python manage.py runserver 6006


   
